# [미국 증시 매크로 중심 뉴스 선별 및 스케줄 배포 계획] (v0.6.1)

본 계획서는 미국 현지 외신 뉴스 중 개별 기업의 지엽적인 기술/제품 단신(예: Apple Siri 업데이트, 단순 기능 출시 등)을 배제하고, 미국 증시 전체의 시황 및 거시 경제(CPI, 연준 금리, 국채 금리, 자금 로테이션 등)를 대변하는 핵심 뉴스 위주로 수집하고 분석할 수 있도록 수집 필터와 AI 요약 가이드라인을 고도화(v0.6.1)하고, GitHub Actions 실행 시간을 한국 시간 오전 06시 정각으로 맞추어 최종 배포하는 작업을 다룹니다.

## User Review Required

> [!IMPORTANT]
> **주요 설계 변경 사항**:
> - **수집 단계 필터 강화 및 밸런스 조정**: `config/config.json`의 `us_exclude_keywords`에서 굵직한 발표를 가릴 수 있는 단어들(`update`, `launch`, `unveil`, `features` 등)을 제외하고, 순수 지엽적/루머성 단어(`hands-on`, `review`, `case leak`, `spec leak`, `giveaway` 등)만 제외하도록 필터를 조정하여 대형 기업의 핵심 비즈니스 소식 수집을 보장합니다.
> - **급등락 주요 종목 핀포인트 뉴스 수집 자동화**: `market_data` 분석을 통해 절대값 5% 이상 급등락한 주요 기술주가 감지될 경우, 해당 종목명 및 티커를 기준으로 실적/시황 뉴스(`Oracle earnings` 등)를 구글 뉴스 RSS에서 핀포인트로 추가 수집(1~2개)하여 뉴스 리스트 최상단에 강제 병합합니다. 이를 통해 오라클 폭락 요인 등 시장의 가장 뜨거운 개별 종목 핵심 시황이 누락 없이 100% 수집되도록 보장합니다.
> - **TQQQ 및 SOXL 지수 표 이동 배치**: 사용자의 요청에 따라 TQQQ와 SOXL을 개별 주식 목록에서 제외하고, 지수 테이블(`indices`)의 S&P 500과 NASDAQ 바로 다음 순서로 노출되도록 재배치합니다.
> - **주요 빅테크 및 반도체 5개사 추가 및 시총순 정렬**: 사용자의 요청에 따라 `Oracle`(`ORCL`), `Palantir`(`PLTR`), `SanDisk`(`SNDK`), `AMAT`(`AMAT`), `LRCX`(`LRCX`) 종목 데이터를 `stocks` 목록에 추가하고, **모든 종목을 2026년 현재 기준 글로벌 시가총액 내림차순(MSFT, AAPL, NVDA, GOOGL, AMZN, META 등)으로 정밀 정렬**하여 리포트의 가독성을 고도화합니다.
> - **WTI 및 BTC 출력 명칭 정제**: 사용자의 요청에 따라 텔레그램 표에 출력되는 티커 명칭을 `CL=F` -> `WTI`, `BTC-USD` -> `BTC`로 치환하여 모바일 화면에서 표가 슬림하고 컴팩트하게 노출되도록 개선합니다.
> - **배포 시간 점검 및 승인**: `.github/workflows/daily_report.yml`의 cron 스케줄이 한국 시간 오전 6시(KST)로 올바르게 설정되어 있음을 확인하고, 모든 수정이 완료된 후 유저의 컨폼을 받아 GitHub에 푸시(push)를 실행합니다.

## Open Questions

> [!NOTE]
> - 혹시 제외하고 싶으신 추가적인 단신 키워드가 있거나, 더 강조하고 싶으신 거시 경제 키워드가 있다면 언제든 말씀해 주세요.

## Proposed Changes

### 1. 설정 및 버전 관리 업데이트

#### [MODIFY] [config.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/config.json)
- `us_exclude_keywords`에서 `update`, `launch`, `unveil`, `features`, `redesign`을 제거하고, `hands-on`, `review`, `case leak`, `spec leak`, `giveaway`, `unboxing` 등을 대신 배치하여 대형 기업의 비즈니스 관련 핵심 뉴스(출시, 공개 등)가 정상적으로 수집되도록 합니다.
- `us_news_keywords`에 주요 개별 종목명 및 실적/급락 관련 핵심 키워드(`Oracle stock`, `Tesla stock`, `NVIDIA stock`, `Apple stock`, `tech earnings report`, `stock plunge`)를 추가로 보강하여, 오라클 실적 폭락 등과 같이 증시에 지대한 영향을 미친 대형 종목 시황 뉴스가 반드시 누락 없이 수집되도록 쿼리를 고도화합니다.
- `TQQQ`와 `SOXL`을 `stocks` 목록에서 제거하고, `indices` 목록의 `S&P 500`, `Nasdaq` 바로 다음 순서로 이동시켜 주요 지수 표에 먼저 표시되도록 순서를 조정합니다.
- 주요 빅테크 및 반도체 기업 목록(`stocks`)에 `Oracle`(`ORCL`), `Palantir`(`PLTR`), `SanDisk`(`SNDK`), `AMAT`(`AMAT`), `LRCX`(`LRCX`) 5개 종목을 추가하고, **모든 종목을 글로벌 시가총액 순서(MSFT, AAPL, NVDA, GOOGL, AMZN, META 등)로 정밀하게 재정렬**하여 시인성을 고도화합니다.

#### [MODIFY] [version.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/version.json)
- 프로그램 버전을 `0.6.1`로 업데이트하고 매크로 중심의 뉴스 선별 고도화, TQQQ/SOXL 지수 표 이동, 주요 빅테크/반도체 5개사 추가 및 시총순 재배치, WTI/BTC 티커 표기 정제 내역을 히스토리에 반영합니다.

---

### 2. 소스 코드 수정 (뉴스 필터링 및 프롬프트 고도화)

#### [MODIFY] [main.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/main.py)
- `market_data` 분석을 통해 ±5.0% 이상 변동한 급등락 기술주를 감지할 경우, 해당 종목에 관한 핀포인트 뉴스(`Oracle stock` 등)를 즉각 수집해 기존 뉴스 리스트의 최상단에 삽입하는 동적 핀포인트 수집 로직을 연동합니다.

#### [MODIFY] [summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py)
- `INDEX_NAME_MAP` 사전에 `"TQQQ": "TQQQ"`, `"SOXL": "SOXL"` 매핑을 추가하여 지수 테이블 렌더링에 올바르게 반영되도록 합니다.
- `STOCK_NAME_MAP` 사전을 추가하여 **`CL=F` -> `WTI`, `BTC-USD` -> `BTC`**로 치환되도록 정제 로직을 구현합니다.
- `summarize_news_with_gemini` 함수 내의 Gemini 프롬프트를 보완합니다:
  - 개별 기업의 지엽적 단신(케이스 유출, 단순 리뷰, 단기 루머 등)은 요약 대상에서 배제하되, 시장에 큰 파장을 줄 수 있는 대형 기술 발표(예: 애플 인텔리전스, 엔비디아 신형 아키텍처 칩셋 공개), 대규모 M&A, 주요 기업 실적 및 가이던스 변화 등 **기업 및 섹터 전반에 중대한 변동을 초래하는 핵심 기업 뉴스는 절대 누락되지 않고 선별되어 매크로 시황과 밸런스 있게 요약되도록 지침을 조정**합니다.

---

### 3. 워크플로우 확인

#### [MODIFY] [.github/workflows/daily_report.yml](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/.github/workflows/daily_report.yml)
- GitHub Actions의 실행 시간이 매일 오전 6시(KST)로 동작할 수 있도록 cron 스케줄이 `'00 21 * * *'` (UTC 21시)로 되어 있는 상태를 검증하고, 최종 커밋에 포함합니다.

---

## Verification Plan

### Automated Tests
- **`Debug/019.debug_test.py` [NEW]**
   - 파일 상단에 해당 파일의 테스트 목적인 "수집 필터 보강 및 매크로 위주 요약 가이드라인 고도화 검증" 주석을 명시합니다.
   - 실제로 변경된 제외 키워드와 프롬프트를 바탕으로 미국 시황 뉴스를 수집 및 요약하여 텔레그램 실발송을 통해 요약 퀄리티를 최종 검증합니다.

### Manual Verification
- 발송된 텔레그램 리포트에서 지엽적인 단신(예: Siri 개인화 등)이 사라지고, 미국 매크로 시황 및 증시 전체의 마켓 드라이버를 조명하는 리포트가 정상 구성되는지 최종 모니터링합니다.
- Git push 전, 유저에게 변경 세부 사항을 명확히 한글로 설명하고 명시적 승인을 얻어 `git push`를 진행합니다.

