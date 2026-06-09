# Global Tech & Macro Daily Report

매일 아침 미국 시장 지수, 나스닥 TOP 10 및 주요 반도체 기업들의 주가 현황과 최신 반도체 업황 뉴스를 한국어로 번역 및 요약하여 사용자의 텔레그램으로 자동 전송하는 시스템입니다.

GitHub Actions를 통해 서버 비용 없이, 그리고 개인 PC 전원을 켜놓지 않아도 자동으로 매일 아침 전송받을 수 있도록 구성되어 있습니다.

---

## 🛠️ 시스템 구성 구조
```
Global_Tech_Macro/
├── .github/
│   └── workflows/
│       └── daily_report.yml  # GitHub Actions 자동 실행 스케줄러 (매일 아침 06:30 KST)
├── config/
│   ├── config.json           # 모니터링할 시장 지수 및 기업 주식 목록
│   └── version.json          # 프로그램 버전 정보
├── DOCS/
│   ├── implementation_plan.md  # 시스템 설계 및 계획 문서
│   └── task.md               # 작업 관리 체크리스트
├── Debug/
│   └── (NNN.debug_test.py)   # 로컬 디버깅 및 기능 테스트 파일들
├── src/
│   ├── collector.py          # Yahoo Finance 주가 및 Google News RSS 뉴스 수집
│   ├── summarizer.py         # Gemini API 기반 번역 및 한국어 핵심 요약
│   ├── telegram_sender.py    # 텔레그램 봇 API를 통한 메시지 전송
│   └── main.py               # 전체 실행 조율 진입점
└── requirements.txt          # 파이썬 라이브러리 의존성
```

---

## ⚙️ 설정 및 연동 가이드

이 시스템을 완벽하게 자동 가동시키려면 아래 3가지 설정값을 획득하고 GitHub Secrets에 등록해야 합니다.

### 1. 텔레그램 봇 생성 및 정보 획득
1. 텔레그램 앱에서 [@BotFather](https://t.me/BotFather)를 검색하여 대화를 시작합니다.
2. `/newbot` 명령어를 전송한 후, 안내에 따라 봇 이름과 사용자 이름(username)을 지정하여 생성합니다.
3. 생성이 완료되면 제공되는 **봇 토큰(HTTP API Token)**을 안전하게 메모해 둡니다. (`TELEGRAM_BOT_TOKEN`)
4. 텔레그램에서 생성된 봇에게 아무 메시지나 보냅니다.
5. [@userinfobot](https://t.me/userinfobot)을 검색하여 대화를 시작하고, 자신의 **Chat ID** 값을 확인하여 저장해 둡니다. (`TELEGRAM_CHAT_ID`)

### 2. Gemini API 키 발급 (무료)
1. [Google AI Studio](https://aistudio.google.com/)에 구글 계정으로 로그인합니다.
2. **"Get API key"** 버튼을 클릭하여 새로운 API Key를 발급받고 저장해 둡니다. (`GEMINI_API_KEY`)
   - 무료 등급(Free Tier)으로도 매일 아침 1회 요약을 수행하기에는 차고 넘치는 처리량을 제공합니다.

### 3. GitHub Actions 자동화 및 Secrets 등록
1. 이 프로젝트 코드를 사용자 본인의 개인 **GitHub Repository**에 푸시(Push)합니다.
2. 생성한 GitHub Repository 페이지의 상단 탭에서 **Settings** -> 좌측 메뉴에서 **Secrets and variables** -> **Actions**를 차례로 클릭합니다.
3. **New repository secret** 버튼을 눌러 아래 세 가지 비밀 값들을 등록합니다.

| Name | Secret Value | 설명 |
| :--- | :--- | :--- |
| `TELEGRAM_BOT_TOKEN` | *123456:ABC-DEF...* | 1번에서 발급받은 텔레그램 봇 토큰 |
| `TELEGRAM_CHAT_ID` | *987654321* | 1번에서 확인한 사용자의 텔레그램 챗 ID |
| `GEMINI_API_KEY` | *AIzaSy...* | 2번에서 발급받은 Gemini API 키 |

4. 등록이 완료되면, 매일 아침 6시 30분(KST)마다 GitHub Actions가 자동으로 실행되어 텔레그램 보고서를 발송합니다.
5. 테스트를 위해 수동으로 동작시키려면 GitHub Repository의 **Actions** 탭 -> `Daily Tech & Macro Report` 워크플로우 선택 -> **Run workflow** 버튼을 클릭하여 즉시 실행할 수 있습니다.

---

## 💻 로컬에서 직접 실행/테스트하는 방법

로컬 PC에서 테스트하거나 수동 실행을 원하는 경우 다음 절차를 따릅니다.

1. **필요 패키지 설치**
   ```bash
   pip install -r requirements.txt
   ```

2. **환경 변수 임시 설정 (Windows PowerShell)**
   ```powershell
   $env:TELEGRAM_BOT_TOKEN="사용자_봇_토큰"
   $env:TELEGRAM_CHAT_ID="사용자_챗_ID"
   $env:GEMINI_API_KEY="사용자_Gemini_API키"
   ```

3. **로컬 실행**
   ```bash
   python src/main.py
   ```

4. **디버그 테스트 실행**
   `Debug/` 폴더에 마련된 단위 테스트를 수행하여 결과를 검증할 수 있습니다.
   ```bash
   python Debug/001.debug_test.py  # 수집 기능 확인
   python Debug/002.debug_test.py  # 요약 기능 확인
   python Debug/003.debug_test.py  # 통합 및 발송 기능 확인
   ```

---

## 📈 수집 종목 및 지수 변경하기
수집 대상을 추가하거나 변경하려면 `config/config.json` 파일을 수정하면 됩니다.
- `"indices"`: 야후 파이낸스(Yahoo Finance) 지수 티커 매핑
- `"stocks"`: 야후 파이낸스 개별 기업 주식 티커 매핑
- `"news_keywords"`: 구글 뉴스 RSS 수집용 키워드 (OR 연산자로 자동 결합됨)
