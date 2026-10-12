# 🌊 2027년 서해 물때표 구글 캘린더 (Tide Calendar)

2027년 서해안 주요 거점의 **일별 물때(7물때식)**와 **상세 조석표(만조/간조 시각, 수위, 최대 조차, 일출/일몰)**를 구글 캘린더 및 애플 캘린더에서 바로 구독할 수 있는 프로젝트입니다.

---

## 📌 주요 특징
1. **서해 7물때식 완벽 적용**: 조금, 무시, 1~13물, 7물(사리) 등 서해 전통 물때 기준
2. **상세 조석 데이터 탑재**: 
   - 🔻 하루 2회 간조(저조) 시각 및 물높이(cm)
   - 🌊 하루 2회 만조(고조) 시각 및 물높이(cm)
   - 📏 일일 최대 고저차(조차 cm) 자동 계산
   - 🤿 해루질 / 갯벌체험 적정 진입 시간 안내
   - ☀️ 일출/일몰 및 월출/월몰 시각
3. **캘린더 최적화**: 종일 투명(`TRANSPARENT`) 일정으로 등록되어 기존 개인 일정(회의, 약속 등)에 방해되지 않고 독립적으로 ON/OFF 가능

---

## 🔗 구글 캘린더 즉시 구독 링크 (URL로 추가)

구글 캘린더 좌측 **다른 캘린더** 옆의 **`+`** → **`URL로 추가`** 메뉴에서 아래 링크를 복사하여 등록하세요.

| 거점 항구 / 포인트 | 캘린더 명칭 | 구글 캘린더 구독 URL (Raw 링크) |
| :--- | :--- | :--- |
| **🌊 서해 전역 (기본)** | 서해 7물때표 (물때명만) | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/tides_west_2027.ics` |
| **인천** | 2027 서해 물때표 [인천] | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/calendars/tides_incheon_2027.ics` |
| **평택** | 2027 서해 물때표 [평택] | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/calendars/tides_pyeongtaek_2027.ics` |
| **신진도 (안흥)** | 2027 서해 물때표 [신진도] | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/calendars/tides_sinjindo_2027.ics` |
| **마검포 (태안)** | 2027 서해 물때표 [마검포] | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/calendars/tides_mageompo_2027.ics` |
| **원산도 (보령)** | 2027 서해 물때표 [원산도] | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/calendars/tides_wonsando_2027.ics` |
| **무창포 (보령)** | 2027 서해 물때표 [무창포] | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/calendars/tides_muchangpo_2027.ics` |
| **홍원항 (서천)** | 2027 서해 물때표 [홍원항] | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/calendars/tides_hongwon_2027.ics` |
| **군산** | 2027 서해 물때표 [군산] | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/calendars/tides_gunsan_2027.ics` |
| **목포** | 2027 서해 물때표 [목포] | `https://raw.githubusercontent.com/sanjangboarder/tide_cal/main/calendars/tides_mokpo_2027.ics` |

---

## 📱 캘린더 표시 예시

### 1) 캘린더 월간/주간 뷰 (제목)
- `[인천 8물] 🔻간 12:21(-51) 🌊만 18:34(916)`
- `[신진도 7물] 🔻간 11:34(42) 🌊만 17:51(612)`

### 2) 일정 클릭 시 상세 내용 (본문)
```text
📍 관측지점: 서해 신진도
📅 양력: 2027년 01월 23일 (토)
🌙 음력/월령: 12.16
🌊 물때: 7물

📏 일일 최대 고저차(조차): 570 cm

🔻 [간조/저조 - 물 빠질 때]:
  • 11:34 : 수위 42cm (▼-528)
  • 23:51 : 수위 60cm (▼-552)

🌊 [만조/고조 - 물 찰 때]:
  • 05:22 : 수위 570cm (▲+510)
  • 17:51 : 수위 612cm (▲+570)

☀️ 일출/일몰: 07:44/17:49
🌕 월출/월몰: 18:32/08:10

🤿 해루질 팁: 최저 간조 시각 2시간 전부터 진입 권장
※ 기상 및 바람에 따라 실제 조위와 시각은 약간의 오차가 있을 수 있습니다.
```

---

## 💻 프로젝트 스크립트 실행 방법

```bash
# 가상환경 생성 및 의존성 설치
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# 1. 서해 전역 7물때 기본 캘린더 생성
./venv/bin/python generate_tides_2027.py

# 2. 9개 주요 거점 상세 조석 캘린더 일괄 수집 및 생성
./venv/bin/python fetch_port_tides.py
```
