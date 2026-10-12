# 🌊 2027년 서해 물때표 구글 캘린더 (Tide Calendar)

2027년 서해안 주요 거점의 **일별 물때(7물때식)**와 **고저차 비율 및 조석표(만조/간조 시각, 수위, 일출/일몰)**를 구글 캘린더 및 애플 캘린더에서 바로 구독할 수 있는 프로젝트입니다.

---

## 📌 주요 특징 및 표기 방식

### 1. 서해 전역 기본 물때표
* **제목 표기**: `13물/음 1월30일`, `7물 (사리)/음 1월16일`, `조금/음 1월8일`
* 한눈에 서해 7물때와 해당 음력 날짜를 확인할 수 있는 가장 간결한 캘린더입니다.

### 2. 지역별 상세 조석 캘린더 (9개 거점)
* **제목 표기**: **`지역물때-(일평균고저차cm)비율%`**
  - 예시: **`인천5물-(544)60%`**, **`신진도7물-(457)70%`**, **`무창포8물-(518)74%`**, **`목포8물-(340)68%`**
* **계산 기준**:
  - 일평균 고저차 = (하루 만조 평균 수위) - (하루 간조 평균 수위)
  - 비율(%) = 지역별 연간 대표 최대 고저차 대비 당일 고저차 비율
* **지역별 최대 기준값 (분모)**:
  - 인천: `900` / 평택: `900`
  - 신진도: `650`
  - 마검포 / 원산도 / 무창포 / 홍원항 / 군산: `700`
  - 목포: `500`

---

## 🔗 구글 캘린더 구독 링크 (URL로 추가)

> ⚠️ **구글 캘린더 캐시 주의사항**:  
> 구글 캘린더는 한번 등록된 URL의 내용을 즉시 갱신하지 않고 8~24시간 동안 자체 캐시를 유지합니다.  
> 따라서 **기존에 등록하셨던 물때 캘린더를 설정에서 '구독 취소(삭제)'**하신 후, 아래의 **`?v=2`가 포함된 링크**로 다시 추가하시면 즉시 변경된 형식으로 표시됩니다!

| 거점 항구 / 포인트 | 캘린더 명칭 | 구글 캘린더 등록용 최신 URL (캐시 무효화 적용) |
| :--- | :--- | :--- |
| **🌊 서해 전역 (기본)** | 서해 7물때표 (물때/음력) | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/tides_west_2027.ics?v=2` |
| **인천** | 2027 서해 물때표 [인천] | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/calendars/tides_incheon_2027.ics?v=2` |
| **평택** | 2027 서해 물때표 [평택] | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/calendars/tides_pyeongtaek_2027.ics?v=2` |
| **신진도 (안흥)** | 2027 서해 물때표 [신진도] | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/calendars/tides_sinjindo_2027.ics?v=2` |
| **마검포 (태안)** | 2027 서해 물때표 [마검포] | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/calendars/tides_mageompo_2027.ics?v=2` |
| **원산도 (보령)** | 2027 서해 물때표 [원산도] | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/calendars/tides_wonsando_2027.ics?v=2` |
| **무창포 (보령)** | 2027 서해 물때표 [무창포] | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/calendars/tides_muchangpo_2027.ics?v=2` |
| **홍원항 (서천)** | 2027 서해 물때표 [홍원항] | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/calendars/tides_hongwon_2027.ics?v=2` |
| **군산** | 2027 서해 물때표 [군산] | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/calendars/tides_gunsan_2027.ics?v=2` |
| **목포** | 2027 서해 물때표 [목포] | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/calendars/tides_mokpo_2027.ics?v=2` |

---

## 📱 캘린더 등록 방법 가이드

1. [Google Calendar](https://calendar.google.com) 접속
2. 좌측 메뉴 **다른 캘린더** 옆의 **`+`** 클릭 → **`URL로 추가`** 선택
3. 위 표에서 원하시는 지역의 URL을 복사하여 붙여넣기
4. **`캘린더 추가`** 버튼 클릭
5. 2027년 캘린더로 이동하면 `인천5물-(544)60%` 형태로 즉시 표시됩니다.

### 일정 클릭 시 상세 내용 (본문)
```text
📍 관측지점: 서해 인천
📅 양력: 2027년 01월 01일 (금)
🌙 음력/월령: 11.24
🌊 물때: 무시
📏 일일 평균 고저차: 436 cm (48% / 기준 900cm)
📏 일일 최대 고저차: 486 cm

🔻 [간조/저조 - 물 빠질 때]:
  • 04:53 : 수위 183cm (▼-515)
  • 17:20 : 수위 257cm (▼-412)

🌊 [만조/고조 - 물 찰 때]:
  • 11:11 : 수위 669cm (▲+486)
  • 23:24 : 수위 642cm (▲+385)

☀️ 일출/일몰: 07:48/17:26
🌕 월출/월몰: 01:42/12:36

🤿 해루질 팁: 최저 간조 시각 2시간 전부터 진입 권장
※ 기상 및 바람에 따라 실제 조위와 시각은 약간의 오차가 있을 수 있습니다.
```

---

## 💻 프로젝트 스크립트 실행 방법

```bash
# 가상환경 생성 및 의존성 설치
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# 1. 서해 전역 7물때 기본 캘린더 생성 (물때/음력 포맷)
./venv/bin/python generate_tides_2027.py

# 2. 9개 주요 거점 상세 조석 캘린더 일괄 수집 및 생성 (고저차 % 포맷)
./venv/bin/python fetch_port_tides.py
```
