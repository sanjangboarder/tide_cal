#!/usr/bin/env python3
"""
서해 주요 9개 거점 항구 조석 데이터 수집 및 iCalendar (.ics) 생성기
- 2027년 전체 일자별 만조/간조 시각, 수위(조위), 조차(고저차), 일출몰 정보 수집
- 캐시 기능 지원 (중복 다운로드 방지)
- 표준 iCalendar (RFC 5545) 생성
"""

import os
import json
import time
import re
import datetime
import urllib.request
from bs4 import BeautifulSoup
from icalendar import Calendar, Event

PORTS = [
    {"id": 158, "code": "incheon", "name": "인천", "base_max": 900},
    {"id": 149, "code": "pyeongtaek", "name": "평택", "base_max": 900},
    {"id": 132, "code": "sinjindo", "name": "신진도", "base_max": 650},
    {"id": 1400, "code": "mageompo", "name": "마검포", "base_max": 700},
    {"id": 353, "code": "wonsando", "name": "원산도", "base_max": 700},
    {"id": 236, "code": "muchangpo", "name": "무창포", "base_max": 700},
    {"id": 523, "code": "hongwon", "name": "홍원항", "base_max": 700},
    {"id": 120, "code": "gunsan", "name": "군산", "base_max": 700},
    {"id": 105, "code": "mokpo", "name": "목포", "base_max": 500},
]

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "calendars")

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

MONTHLY_TARGETS = {
    1: {"primary": None, "others": []},
    2: {"primary": None, "others": []},
    3: {"primary": "우럭", "others": ["노래미", "도다리"]},
    4: {"primary": "광어", "others": ["우럭", "도다리"]},
    5: {"primary": "광어", "others": ["우럭", "참돔"]},
    6: {"primary": "참돔", "others": ["광어", "우럭", "농어"]},
    7: {"primary": "농어", "others": ["참돔", "백조기", "광어"]},
    8: {"primary": "백조기", "others": ["농어", "참돔", "광어"]},
    9: {"primary": "쭈꾸미", "others": ["갑오징어", "광어", "우럭"]},
    10: {"primary": "갑오징어", "others": ["쭈꾸미", "광어", "우럭"]},
    11: {"primary": "쭈꾸미", "others": ["갑오징어", "광어", "우럭"]},
    12: {"primary": "광어", "others": ["우럭"]},
}

FISH_ABBR = {
    "쭈꾸미": "쭈",
    "갑오징어": "갑",
    "참돔": "참",
    "광어": "광",
    "우럭": "우",
    "농어": "농",
    "백조기": "백",
    "도다리": "도",
    "노래미": "노",
}

def calc_fish_score(fish: str, pct: int):
    """
    고저차 비율(%)에 따른 어종별 출조 점수(1~5점) 및 가이드 반환
    70% 이상을 사리 급류 최악(🔴) 기준으로 적용
    """
    if fish == "쭈꾸미":
        if pct <= 38:
            return 5, "최적의 조류! 봉돌 10~12호 가볍게 운용"
        elif pct <= 50:
            return 4, "양호한 조류! 봉돌 12~14호 추천"
        elif pct <= 69:
            return 3, "보통 조류, 봉돌 14~18호 운용 가능"
        else:
            return 1, "70% 이상 사리 급류 주의 (바닥 찍기 어려움)"
    elif fish == "갑오징어":
        if 45 <= pct <= 65:
            return 5, "갑오징어 최적 조류! 에기 액션 및 배 흘림 최상"
        elif (38 <= pct < 45) or (66 <= pct <= 69):
            return 4, "양호한 조류, 갑오징어 입질 활발 (봉돌 12~16호)"
        elif 30 <= pct < 38:
            return 3, "조류 다소 약함 (에기 가볍게 운용)"
        elif pct < 30:
            return 2, "조류 부족 (에기 액션 저조, 물 정체)"
        else:
            return 1, "70% 이상 사리 급류 주의 (채비 날림)"
    elif fish == "백조기":
        if pct <= 42:
            return 5, "최적의 소조기! 바닥 입질 매우 편함"
        elif pct <= 55:
            return 4, "양호한 조류, 채비 안정적"
        elif pct <= 69:
            return 3, "보통 조류, 봉돌 35~40호"
        else:
            return 1, "70% 이상 조류 강함, 채비 굴러감"
    elif fish == "우럭":
        if 35 <= pct <= 55:
            return 5, "어초/침선 최적의 황금 물때"
        elif 56 <= pct <= 69:
            return 4, "양호한 입질, 봉돌 40~50호"
        elif pct < 35:
            return 3, "조류 다소 정체, 활성도 보통"
        else:
            return 1, "70% 이상 사리 물때, 조류 너무 세서 비추"
    elif fish == "광어":
        if 45 <= pct <= 65:
            return 5, "다운샷 최적 조류! 배 흘림 최상"
        elif (38 <= pct < 45) or (66 <= pct <= 69):
            return 4, "양호한 배 흘림 조류"
        elif 30 <= pct < 38:
            return 3, "조류 다소 완만"
        elif pct < 30:
            return 2, "조류 부족 (배 정체)"
        else:
            return 1, "70% 이상 급류 (바닥 안착 어려움)"
    elif fish == "참돔":
        if 55 <= pct <= 75:
            return 5, "타이라바 최적 조류! 넥타이 액션 최상"
        elif (45 <= pct < 55) or (76 <= pct <= 85):
            return 4, "양호한 조류, 타이라바 추천"
        elif 38 <= pct < 45:
            return 3, "조류 다소 완만"
        else:
            return 2, "조류 부족 또는 대사리 급류"
    elif fish == "농어":
        if 55 <= pct <= 80:
            return 5, "외수질 최적 조류! 먹이활동 극대화"
        elif (45 <= pct < 55) or (81 <= pct <= 90):
            return 4, "양호한 조류, 활성도 좋음"
        elif 38 <= pct < 45:
            return 3, "보통 수준"
        else:
            return 2, "조류 부족 또는 극대사리"
    elif fish in ["도다리", "노래미"]:
        if pct <= 50:
            return 4, "봄철 원투/바닥 채비 무난"
        else:
            return 3, "물살 다소 있음"
    return 3, "보통 수준"

def fetch_month_data(port_id: int, year: int, month: int):
    """특정 항구의 특정 연/월 데이터를 가져와 파싱 (캐시 우선)"""
    cache_file = os.path.join(CACHE_DIR, f"{port_id}_{year}_{month:02d}.json")
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    url = f"https://www.badatime.com/{port_id}-{year}-{month:02d}-01.html"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  ❌ 에러 ({port_id}, {year}-{month:02d}): {e}")
        return []

    soup = BeautifulSoup(html, "lxml")
    tables = soup.find_all("table")
    target_trs = None
    for t in tables:
        if "만조시각" in t.text and "간조시각" in t.text and "월령" in t.text:
            trs = [tr for tr in t.find_all("tr", recursive=False)]
            if len(trs) > 20:
                target_trs = trs
                break

    if not target_trs:
        print(f"  ⚠️ 테이블 파싱 실패 ({port_id}, {year}-{month:02d})")
        return []

    month_results = []

    for tr in target_trs:
        tds = [td.get_text(separator=" ", strip=True) for td in tr.find_all("td", recursive=False)]
        if not tds:
            continue
        # 첫 번째 셀이 요일인지 확인
        if tds[0] in ["월", "화", "수", "목", "금", "토", "일"]:
            day_of_week = tds[0]
            day_match = re.search(r"^(\d+)", tds[1])
            if not day_match:
                continue
            day_num = int(day_match.group(1))

            # 음력/월령 (앞의 날짜 숫자만 제거)
            lunar_info = re.sub(r'^\d+\s*', '', tds[1]).strip()

            tide_name = re.sub(r'\s+', '', tds[3]) if len(tds) > 3 else ""
            high_tide_raw = tds[5] if len(tds) > 5 else ""
            low_tide_raw = tds[6] if len(tds) > 6 else ""
            sun_raw = tds[7] if len(tds) > 7 else ""
            moon_raw = tds[8] if len(tds) > 8 else ""

            # 만조/간조 상세 분리 파싱
            high_tides = parse_tide_entries(high_tide_raw)
            low_tides = parse_tide_entries(low_tide_raw)

            entry = {
                "year": year,
                "month": month,
                "day": day_num,
                "day_of_week": day_of_week,
                "lunar_info": lunar_info,
                "tide_name": tide_name,
                "high_tides": high_tides,
                "low_tides": low_tides,
                "sun": sun_raw,
                "moon": moon_raw,
            }
            month_results.append(entry)

    # 캐시 저장
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(month_results, f, ensure_ascii=False, indent=2)

    return month_results

def parse_tide_entries(raw_text: str):
    """
    '11:11 (669) ▲+486 23:24 (642) ▲+385' 형태에서
    각 조석 시각, 수위(cm), 변동값(cm) 추출
    """
    entries = []
    # 정규식 패턴: 시:분 (수위) [▲▼변동]
    pattern = r"(\d{2}:\d{2})\s*\(([-+]?\s*\d+)\)(?:\s*([▲▼][-+]?\d+))?"
    matches = re.finditer(pattern, raw_text)
    for m in matches:
        t_time = m.group(1)
        level_str = m.group(2).replace(" ", "")
        level = int(level_str) if level_str else None
        diff = m.group(3) if m.group(3) else ""
        entries.append({
            "time": t_time,
            "level": level,
            "diff": diff
        })
    return entries

def build_port_calendar(port: dict, year: int = 2027):
    """한 항구의 1년치 조석 데이터로 .ics 생성"""
    port_name = port["name"]
    port_code = port["code"]
    port_id = port["id"]

    print(f"\n🌊 [{port_name}] (코드: {port_code}, ID: {port_id}) 데이터 수집 시작...")
    year_data = []

    for m in range(1, 13):
        m_data = fetch_month_data(port_id, year, m)
        year_data.extend(m_data)
        time.sleep(0.1) # 서버 부하 방지

    if not year_data:
        print(f"❌ [{port_name}] 데이터가 없습니다.")
        return None

    cal = Calendar()
    cal.add('prodid', f'-//Korean West Coast Tide Calendar - {port_name}//KO')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', f'{year} 서해 물때표 [{port_name}]')
    cal.add('x-wr-timezone', 'Asia/Seoul')
    cal.add('x-wr-caldesc', f'{year}년 {port_name} 조석표(만조, 간조, 조위, 물때) 일별 캘린더')

    delta = datetime.timedelta(days=1)
    now_utc = datetime.datetime.now(datetime.timezone.utc)

    base_max = port.get("base_max", 700)

    for item in year_data:
        event = Event()
        c_date = datetime.date(item["year"], item["month"], item["day"])
        event.add('uid', f'tide-{port_code}-{year}-{c_date.strftime("%Y%m%d")}@westcoast-tides')
        event.add('dtstamp', now_utc)
        event.add('dtstart', c_date)
        event.add('dtend', c_date + delta)

        tide_name = item["tide_name"] or "물때"

        # 일평균 고저차 계산: (만조 수위 평균) - (간조 수위 평균)
        high_levels = [e["level"] for e in item["high_tides"] if e.get("level") is not None]
        low_levels = [e["level"] for e in item["low_tides"] if e.get("level") is not None]

        if high_levels and low_levels:
            avg_high = sum(high_levels) / len(high_levels)
            avg_low = sum(low_levels) / len(low_levels)
            avg_range = round(avg_high - avg_low)
            pct = round((avg_range / base_max) * 100)
        else:
            avg_range = 0
            pct = 0

        month = item["month"]
        targets = MONTHLY_TARGETS.get(month, {"primary": None, "others": []})
        primary_fish = targets.get("primary")
        other_fishes = targets.get("others", [])

        fish_section = ""
        if primary_fish:
            score, tip = calc_fish_score(primary_fish, pct)
            stars = "★" * score + "☆" * (5 - score)
            badge = "🟢" if score == 5 else ("🟡" if score == 4 else ("⚪" if score == 3 else "🔴"))
            fish_char = FISH_ABBR.get(primary_fish, primary_fish[0])
            summary = f"{badge}{port_name}{tide_name}-({avg_range}){pct}%[{fish_char}]"

            f_lines = [f"🎯 [{month}월 주요 어종별 출조 적합도]:"]
            f_lines.append(f"  • {primary_fish} (주력) : {stars} {badge} ({tip})")
            for o_fish in other_fishes:
                o_score, o_tip = calc_fish_score(o_fish, pct)
                o_stars = "★" * o_score + "☆" * (5 - o_score)
                o_badge = "🟢" if o_score == 5 else ("🟡" if o_score == 4 else ("⚪" if o_score == 3 else "🔴"))
                f_lines.append(f"  • {o_fish} : {o_stars} {o_badge} ({o_tip})")
            fish_section = "\n".join(f_lines) + "\n\n"
        else:
            summary = f"{port_name}{tide_name}-({avg_range}){pct}%"

        event.add('summary', summary)

        # 상세 설명 본문
        low_details = "\n".join([f"  • {e['time']} : 수위 {e['level']}cm ({e['diff']})" for e in item["low_tides"]]) or "  (정보 없음)"
        high_details = "\n".join([f"  • {e['time']} : 수위 {e['level']}cm ({e['diff']})" for e in item["high_tides"]]) or "  (정보 없음)"

        diff_str = f"📏 일일 평균 고저차: {avg_range} cm ({pct}% / 기준 {base_max}cm)"
        if high_levels and low_levels:
            max_day_range = max(high_levels) - min(low_levels)
            diff_str += f"\n📏 일일 최대 고저차: {max_day_range} cm"

        desc_text = (
            f"📍 관측지점: 서해 {port_name}\n"
            f"📅 양력: {c_date.strftime('%Y년 %m월 %d일')} ({item['day_of_week']})\n"
            f"🌙 음력/월령: {item['lunar_info']}\n"
            f"🌊 물때: {tide_name}\n"
            f"{diff_str}\n\n"
            f"{fish_section}"
            f"🔻 [간조/저조 - 물 빠질 때]:\n{low_details}\n\n"
            f"🌊 [만조/고조 - 물 찰 때]:\n{high_details}\n\n"
            f"☀️ 일출/일몰: {item['sun']}\n"
            f"🌕 월출/월몰: {item['moon']}\n\n"
            f"🤿 해루질 팁: 최저 간조 시각 2시간 전부터 진입 권장\n"
            f"※ 기상 및 바람에 따라 실제 조위와 시각은 약간의 오차가 있을 수 있습니다."
        )
        event.add('description', desc_text)
        event.add('transp', 'TRANSPARENT')
        event.add('status', 'CONFIRMED')

        cal.add_component(event)

    out_file = os.path.join(OUTPUT_DIR, f"tides_{port_code}_{year}.ics")
    with open(out_file, "wb") as f:
        f.write(cal.to_ical())

    print(f"✅ [{port_name}] 캘린더 생성 완료: {out_file} (총 {len(year_data)}일)")
    return out_file

if __name__ == "__main__":
    import sys
    year = 2027
    print(f"🌟 2027년 서해 주요 9개 거점 항구 조석 캘린더 일괄 생성 시작 (총 {len(PORTS)}개 거점)")
    for p in PORTS:
        build_port_calendar(p, year)
    print("\n🎉 모든 항구의 2027년 물때 캘린더가 성공적으로 생성되었습니다!")
