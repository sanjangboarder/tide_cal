#!/usr/bin/env python3
"""
2027년 서해안 7물때식 구글 캘린더 (.ics) 생성기
- 서해안 7물때식 (1물~13물, 조금, 무시)
- 음력 기준 계산
- 구글 캘린더 / 애플 캘린더 표준 iCalendar (RFC 5545) 포맷 준수
"""

import datetime
from korean_lunar_calendar import KoreanLunarCalendar
from icalendar import Calendar, Event

# 서해 7물때 매핑 (음력 일자 -> 물때 정보)
# 음력 1일: 7물(사리), 8일: 조금, 9일: 무시, 10일: 1물 ... 15일: 6물, 16일: 7물(사리)
TIDE_MAP_7 = {
    1: {"name": "7물 (사리)", "desc": "조수간만의 차가 가장 크고 조류가 빠른 시기 (해루질 최적기)", "badge": "🌊 7물 (사리)"},
    2: {"name": "8물", "desc": "조류가 매우 빠르고 수위 변화가 큰 시기", "badge": "🌊 8물"},
    3: {"name": "9물", "desc": "조류가 빠르고 물살이 거센 시기", "badge": "🌊 9물"},
    4: {"name": "10물", "desc": "사리 이후 물살이 점차 잦아드는 시기", "badge": "🌊 10물"},
    5: {"name": "11물", "desc": "조류가 완만해지기 시작하는 시기", "badge": "🌊 11물"},
    6: {"name": "12물", "desc": "물살이 차분해지는 시기", "badge": "🌊 12물"},
    7: {"name": "13물", "desc": "조류가 약해지며 조금으로 가는 길목", "badge": "🌊 13물"},
    8: {"name": "조금", "desc": "조수간만의 차가 가장 작고 조류가 가장 약한 시기 (초보 낚시 적합)", "badge": "⚓ 조금"},
    9: {"name": "무시", "desc": "조금 다음날, 물의 흐름이 거의 정체된 시기", "badge": "⚓ 무시"},
    10: {"name": "1물", "desc": "물이 서서히 살아나기 시작하는 시기", "badge": "🌊 1물"},
    11: {"name": "2물", "desc": "물살이 조금씩 살아나는 시기", "badge": "🌊 2물"},
    12: {"name": "3물", "desc": "조류가 적당히 흐르기 시작하는 시기 (생활 낚시 추천)", "badge": "🌊 3물"},
    13: {"name": "4물", "desc": "물살이 활발해지기 시작하는 시기", "badge": "🌊 4물"},
    14: {"name": "5물", "desc": "조류가 힘차게 살아나는 시기", "badge": "🌊 5물"},
    15: {"name": "6물", "desc": "사리를 앞두고 조류가 매우 활발해지는 시기", "badge": "🌊 6물"},
    
    16: {"name": "7물 (사리)", "desc": "보름 사리 - 조수간만의 차가 최대이며 조류가 가장 빠른 시기 (해루질 최적기)", "badge": "🌊 7물 (사리)"},
    17: {"name": "8물", "desc": "조류가 매우 빠르고 수위 변화가 큰 시기", "badge": "🌊 8물"},
    18: {"name": "9물", "desc": "조류가 빠르고 물살이 거센 시기", "badge": "🌊 9물"},
    19: {"name": "10물", "desc": "사리 이후 물살이 점차 잦아드는 시기", "badge": "🌊 10물"},
    20: {"name": "11물", "desc": "조류가 완만해지기 시작하는 시기", "badge": "🌊 11물"},
    21: {"name": "12물", "desc": "물살이 차분해지는 시기", "badge": "🌊 12물"},
    22: {"name": "13물", "desc": "조류가 약해지며 조금으로 가는 길목", "badge": "🌊 13물"},
    23: {"name": "조금", "desc": "조수간만의 차가 가장 작고 조류가 가장 약한 시기 (초보 낚시 적합)", "badge": "⚓ 조금"},
    24: {"name": "무시", "desc": "조금 다음날, 물의 흐름이 거의 정체된 시기", "badge": "⚓ 무시"},
    25: {"name": "1물", "desc": "물이 서서히 살아나기 시작하는 시기", "badge": "🌊 1물"},
    26: {"name": "2물", "desc": "물살이 조금씩 살아나는 시기", "badge": "🌊 2물"},
    27: {"name": "3물", "desc": "조류가 적당히 흐르기 시작하는 시기 (생활 낚시 추천)", "badge": "🌊 3물"},
    28: {"name": "4물", "desc": "물살이 활발해지기 시작하는 시기", "badge": "🌊 4물"},
    29: {"name": "5물", "desc": "조류가 힘차게 살아나는 시기", "badge": "🌊 5물"},
    30: {"name": "6물", "desc": "사리를 앞두고 조류가 매우 활발해지는 시기", "badge": "🌊 6물"},
}

def get_tide_info(lunar_day: int):
    # 만약 음력 30일이 없는 달(29일 소월)인 경우 29일은 5물, 다음날은 1일 7물이 됨.
    return TIDE_MAP_7.get(lunar_day, {"name": f"{lunar_day}물", "desc": "", "badge": f"{lunar_day}물"})

def generate_calendar(year: int = 2027, output_path: str = "tides_west_2027.ics"):
    cal = Calendar()
    cal.add('prodid', '-//Korean West Coast 7-Tide Calendar//KO')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', f'{year} 서해 물때표 (7물때)')
    cal.add('x-wr-timezone', 'Asia/Seoul')
    cal.add('x-wr-caldesc', f'{year}년 서해안 7물때식(조금, 무시, 1~13물, 사리) 일별 물때 캘린더')

    lunar_cal = KoreanLunarCalendar()
    
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    current_date = start_date
    delta = datetime.timedelta(days=1)

    event_count = 0
    now_utc = datetime.datetime.now(datetime.timezone.utc)

    while current_date <= end_date:
        lunar_cal.setSolarDate(current_date.year, current_date.month, current_date.day)
        l_year = lunar_cal.lunarYear
        l_month = lunar_cal.lunarMonth
        l_day = lunar_cal.lunarDay
        is_leap = lunar_cal.isIntercalation

        tide_info = get_tide_info(l_day)
        
        event = Event()
        event.add('uid', f'tide-{year}-{current_date.strftime("%Y%m%d")}@westcoast-tides')
        event.add('dtstamp', now_utc)
        
        # 종일 일정: DTSTART는 해당일, DTEND는 다음날이어야 함
        event.add('dtstart', current_date)
        event.add('dtend', current_date + delta)
        
        leap_prefix = "윤" if is_leap else ""
        lunar_date_str = f"음 {leap_prefix}{l_month}월{l_day}일"
        summary = f"{tide_info['name']}/{lunar_date_str}"
        event.add('summary', summary)

        leap_str = " (윤달)" if is_leap else ""
        description = (
            f"📅 양력: {current_date.strftime('%Y년 %m월 %d일')}\n"
            f"🌙 음력: {l_year}년 {l_month}월 {l_day}일{leap_str}\n"
            f"🌊 물때: 서해 7물때식 - {tide_info['name']}\n"
            f"💡 특성: {tide_info['desc']}\n\n"
            f"※ 서해안 기준 물때이며, 특정 항구의 상세 만조/간조 시각은 바다타임 또는 국립해양조사원을 참조하세요."
        )
        event.add('description', description)
        
        # 투명도: 투명(TRANSPARENT) 설정하여 사용자 캘린더의 바쁨/한가함 상태에 영향을 주지 않음
        event.add('transp', 'TRANSPARENT')
        event.add('status', 'CONFIRMED')
        
        cal.add_component(event)
        event_count += 1
        current_date += delta

    with open(output_path, 'wb') as f:
        f.write(cal.to_ical())

    print(f"✅ {year}년 물때 캘린더 생성 완료: {output_path} (총 {event_count}일 등록)")

if __name__ == "__main__":
    generate_calendar(2027, "tides_west_2027.ics")
