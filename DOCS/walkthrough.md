# 통합 작업 히스토리 (Walkthrough)

## 📅 2026-06-11
### 미국 증시 매크로 뉴스 선별 밸런스 최적화(급등락 기술주 핀포인트 수집 자동화), TQQQ/SOXL 지수화, 신규 5개 종목(Oracle, Palantir, SanDisk, AMAT, LRCX) 추가 및 시총순 정렬 완료 (v0.6.1)

미국 현지 금융 뉴스 중 시장 가치가 없거나 지엽적인 단순 기기 리뷰/소프트웨어 업데이트 단신(unboxing, hands-on, case leak 등)은 완벽히 제거하되, **오라클의 실적 폭락, 인텔의 업그레이드 급등, 애플/엔비디아의 핵심 발표 등 미국 증시 판도와 주가 수급에 지대한 영향을 주는 굵직한 주요 기업 핵심 비즈니스 뉴스는 요약에서 누락되지 않도록 수집 파이프라인과 AI 선별 규칙의 밸런스를 고도화**했습니다. 이를 위해 ±5.0% 이상 변동이 큰 주요 기술주가 감지될 경우 관련 뉴스를 핀포인트로 즉각 추가 수집하는 로직을 도입했습니다. 또한 사용자의 요구에 맞춰 레버리지 지수 ETF인 `TQQQ`/`SOXL`을 주요 시장 지수(`indices`) 테이블의 S&P 500, NASDAQ 직후로 이동 배치하고, WTI/BTC 출력 명칭 정제(WTI, BTC) 및 주요 빅테크 21개 종목의 시총순 정렬을 완료했습니다.

#### 1. 구현된 주요 변경 사항
- **급등락 주요 종목 핀포인트 뉴스 수집 자동화**:
  - [src/main.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/main.py): 주가 데이터를 수집한 뒤, 절대값 5.0% 이상 급등락한 주요 기술주가 감지될 경우 해당 종목의 실적/시황 뉴스(예: `Oracle stock`, `Oracle earnings`)를 구글 뉴스 RSS에서 핀포인트로 추가 수집하여 뉴스 목록 최상단에 강제 병합시키는 로직을 신설했습니다.
- **수집 단계 필터 밸런스 정밀 조정**:
  - [config/config.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/config.json): `us_exclude_keywords`에서 `update`, `launch`, `unveil`, `features` 등 굵직한 기업 발표에 빈번히 쓰이는 핵심 단어를 제외시켰습니다. 대신에 정보 가치가 낮은 `hands-on`, `review`, `unboxing`, `giveaway`, `spec leak`, `case leak` 등 순수 단신/리뷰성 단어들만 남겨두어 핵심 비즈니스 뉴스의 차단을 방지했습니다.
  - `us_news_keywords`에 `Oracle stock`, `Tesla stock`, `tech earnings report`, `stock plunge` 등의 키워드를 보강해 수집 쿼리를 고도화했습니다.
- **TQQQ 및 SOXL 지수 테이블 재배치**:
  - [config/config.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/config.json): `stocks` 목록에 있던 `TQQQ`와 `SOXL`을 `indices`로 이동시키고, `S&P 500`과 `Nasdaq` 바로 다음에 오도록 순서를 조정했습니다.
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py): `INDEX_NAME_MAP` 사전에 TQQQ와 SOXL을 정식 추가하여 지수 테이블 렌더링에 반영했습니다.
- **주요 빅테크 및 반도체 21개사 추가 및 시총순 정렬**:
  - [config/config.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/config.json): `Oracle`(`ORCL`), `Palantir`(`PLTR`), `SanDisk`(`SNDK`), `AMAT`(`AMAT`), `LRCX`(`LRCX`) 5개 종목을 추가하고, **모든 종목을 글로벌 시가총액 내림차순(MSFT, AAPL, NVDA, GOOGL, AMZN, META, TSM, TSLA, AVGO, ASML ... PLTR, SNDK)으로 정밀하게 정렬**했습니다.
- **WTI 및 BTC 출력 명칭 정제**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py): `STOCK_NAME_MAP` 사전을 신설하여 `CL=F` -> `WTI`, `BTC-USD` -> `BTC`로 치환 출력하여 가로 정렬 너비를 슬림하게 최적화했습니다.
- **AI 요약 뉴스 밸런스 고도화**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py): Gemini API 프롬프트의 지침을 보강하여, 사소한 단신(unboxing 등)은 필터링하되 기업의 실적이나 주가, 시장 수급에 큰 파급력을 주는 대규모 비즈니스 발표(M&A, 대형 IPO, CAPEX 설비투자, 어닝 쇼크/서프라이즈 등)는 거시 시황 분석과 함께 균형 있게 선별 요약하도록 가이드라인을 최적화했습니다.
- **버전 및 문서 동기화**:
  - [config/version.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/version.json): 버전을 `0.6.1`로 상향하고 히스토리를 갱신했습니다.
  - [Debug/019.debug_test.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/Debug/019.debug_test.py): 실시간 주가 변동 연동 및 동적 핀포인트 뉴스 병합 검증을 추가하여 최종 텔레그램 실발송을 검증했습니다.

#### 2. 검증 결과
- **디버그 테스트 실발송 검증 (`Debug/019.debug_test.py`)** -> **성공**
  - **급등락 기술주 핀포인트 수집 검증**: 오라클 주가 급락(-11.83%) 및 인텔 급등(+5.49%) 등 마켓 임팩트가 큰 주가 변동을 코드가 자동 감지하여 `Oracle stock`, `Oracle earnings` 관련 뉴스를 핀포인트로 정확히 수집 및 병합해 오는 것을 콘솔 출력을 통해 실증했습니다.
  - **뉴스 밸런스 검증**: AI가 오라클의 인프라 CapEx 지출 급증 우려 및 채권 발행 우려로 인한 급락 요인을 정확하게 포착하고, 인텔의 BofA 더블 상향 조정 호재 소식과 매크로 지표(CPI, 국채금리)를 아주 조화롭고 완성도 높게 요약 카드 및 💡 주요 요인으로 텔레그램에 전송했습니다.
  - **시총순 정렬 및 티커 치환 검증**: 주가 목록 테이블에 추가된 AMAT, LRCX, SNDK, ORCL, PLTR을 포함한 21개 종목이 시총 내림차순으로 완벽히 정렬되었으며, `WTI`, `BTC` 명칭 치환에 의해 세로 컬럼 정렬이 소수점 한 자리 오차도 없이 수직 칼정렬(🔴/🔵) 렌더링되었습니다.

---

## 📅 2026-06-10
### AI·반도체·하이퍼스케일러·실적 발표 수집 강화 및 🔴/🔵 등락 이모지 단독 개편 완료 (v0.6.0)

미국 현지 금융 시황 분석의 깊이를 끌어올리고 최신 핵심 업황을 정확하게 짚기 위해 AI 기술, 반도체 공급망, 하이퍼스케일러의 인프라 투자(설비투자/CAPEX), 그리고 주요 기업들의 분기 실적 발표(Earnings) 관련 기사의 수집 및 분석 가이드라인을 대대적으로 강화하였습니다. 또한, 기존 등락 표시 이모지(`🔺`/`🔽` 등)가 혼합되거나 기기별로 렌더링이 상이하던 문제를 해결하기 위해 직관적인 동그라미 색상(`🔴`/`🔵`) 조합으로 전면 개편하고, 텔레그램 상의 표 칼정렬을 더욱 다듬었습니다.

#### 1. 구현된 주요 변경 사항
- **수집 영문 검색 키워드 대거 확충**:
  - [config/config.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/config.json): `us_news_keywords` 목록에 AI 기술 개발(`AI`, `artificial intelligence`), 하이퍼스케일러 및 클라우드 인프라(`hyperscaler`, `cloud infrastructure`), 실적 발표(`earnings`, `earnings report`, `financial results`) 관련 핵심 키워드들을 직접적으로 보강하여 관련 최신 기사가 파이프라인에 대량 인입되도록 조치했습니다.
- **등락 이모지 🔴/🔵 단독 개편**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py): 지수 및 종목 테이블 등락 기호를 기존 화살표 기호에서 오직 **상승: 빨간색 원(`🔴`), 하락: 파란색 원(`🔵`)**으로 전면 교정하여 지저분하지 않은 직관적인 시인성을 확보했습니다.
- **AI 정합성 요약 지침 고도화**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py): 
    - `summarize_news_with_gemini` 함수가 실제 지표 등락률 데이터를 넘겨받아 시장 상태와 요약 내용 간에 모순이 발생하지 않도록(예: 지수 대폭락 중인데 상승 랠리 호재 기사만 일방적으로 요약하는 오류 방지) 지침을 정합성 있게 강화했습니다.
    - AI가 선별 시 **AI 업계 동향, 반도체 공급망, 하이퍼스케일러의 설비투자 계획(CAPEX), 실적 발표** 4대 주제를 최우선적으로 엄선하여 보고하도록 선별 프롬프트 가이드라인을 고도화했습니다.
- **버전 갱신**:
  - [config/version.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/version.json): 프로그램 버전을 `0.6.0`으로 상향하고 변경 기록을 추가했습니다.
- **디버그 테스트**:
  - [Debug/018.debug_test.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/Debug/018.debug_test.py): 신규 수집 파이프라인 및 등락 동기화 카드뉴스 발송을 위한 테스트 스크립트를 작성하여 실제 전송 동작 및 시인성 칼정렬 상태를 완벽히 실증했습니다.

#### 2. 검증 결과
- **AI/하이퍼스케일러/실적 분석 및 동그라미 이모지 전송 테스트 (`Debug/018.debug_test.py`)** -> **성공**
  - 보강된 키워드 기사(Apple AI Siri, Tesla 실적 슬라이딩 분석, SpaceX IPO 등)가 성공적으로 수집되었습니다.
  - 지수/종목의 등락률이 `🔴`(상승) / `🔵`(하락) 동그라미 단독 구성으로 모바일 텔레그램 화면상에 소수점 한 칸 오차도 없이 수직 칼정렬 렌더링되었습니다.
  - AI가 당일 시장의 하락세(나스닥 -0.97%, 반도체 -1.93% 등)를 완벽히 인지하여, 지정학적 완화나 과거 애플 발표 랠리 등의 상승 호재 위주가 아닌 **"반도체 섹터 전반의 약세 주도", "애플 WWDC 발표 후 소문에 사서 뉴스에 파는 반응과 개인정보 우려로 인한 하락", "테슬라 실적 우려 하락"** 등 하락 분석 중심의 톤앤매너로 주요 요인(💡)을 정합성 있게 도출하여 송출함을 최종 입증 완료하였습니다.

---

## 📅 2026-06-10
### 미국 현지 금융 외신 단독 포커스(국내 뉴스 배제) 및 AI 시장 요인/경제 지표 자동 추출 개편 완료 (v0.5.0)

국내 언론 및 뉴스를 발송 대상에서 완전히 배제하고, 오직 미국의 신뢰성 높은 금융 외신(글로벌 매크로, 기술주, 국채, 지수에 영향력을 준 뉴스)만 단독 포커스하여 리포트를 발송하도록 전면 개편하였습니다. 또한 AI(Gemini 2.5-flash)가 외신 15개 기사를 종합 분석하여 **💡 오늘의 미국 시장 주요 요인** 및 **📊 오늘 발표된 주요 경제 지표**를 텔레그램 카드뉴스 상에 자동으로 선별/추출하는 기능도 성공적으로 융합하였습니다.

#### 1. 구현된 주요 변경 사항
- **국내 뉴스 수집 제외**:
  - [src/main.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/main.py): 국내 뉴스 수집 함수 호출을 생략하고 `news_list = []`로 설정하여 불필요한 국내 잡음 뉴스의 파이프라인 유입을 원천 차단했습니다.
- **외신 단독 포커스 및 AI 선별 프롬프트 전면 리팩토링**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py):
    - 훼손되었던 파일 구문 오류(시장 데이터 및 빅테크 종목 정렬 테이블 포맷팅 로직)를 완벽하게 복구하였습니다.
    - `format_news_list` 폴백 전송 엔진 내에서 국내 뉴스 렌더링 로직을 영구 제거하고 미국 외신 기사만 표시하도록 슬림화했습니다.
    - `summarize_news_with_gemini` 함수에서 한국 언론 뉴스 입력 섹션을 완전 삭제하고, 프롬프트 요건을 미국 금융 외신(최대 15개 후보군)만을 단독 분석하도록 재구성하였습니다.
    - AI가 당일 증시의 상승/하락 핵심 요인(마켓 드라이버 3~5선, 💡)과 주요 경제 지표(📊, 기대인플레/CPI/고용지표 등 고정폭 테이블)를 추출하여 **미국 현지 시황 & 외신 요약(🇺🇸)** 섹션과 함께 텔레그램에 전달하도록 지침을 최적화했습니다.
    - 카드뉴스 템플릿(v0.4.8 사양)을 완벽히 유지하여 `번역 · [출처] · [시간]` 접두사 배지, 굵은 제목 전체 하이퍼링크(`<b><a href="...">제목</a></b>`), 핵심 2줄 요약 들여쓰기(`  • `), 구분선 등이 조화롭게 렌더링되게 하였습니다.
- **디버그 테스트**:
  - [Debug/016.debug_test.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/Debug/016.debug_test.py): 외신 단독 수집 및 자격 증명 자동 복원, 텔레그램 실발송 검증을 위한 신규 테스트 스크립트를 작성하여 실시간 발송 완료를 성공적으로 입증했습니다.

#### 2. 검증 결과
- **외신 단독 요약 및 지표 추출 발송 테스트 (`Debug/016.debug_test.py`)** -> **성공**
  - 자격 증명을 로그 파일에서 안정적으로 복원하여, Apple Intelligence 및 엔비디아/TSMC 등 15개 외신을 실시간으로 성공적 수집했습니다.
  - Gemini API가 수집된 외신을 바탕으로 종합 시장 주요 요인(💡)과 기대 인플레이션 등 경제 지표(📊)를 테이블 형태로 정확히 선별하여, 텔레그램 상에 가독성 높은 카드뉴스 포맷으로 전송되는 것을 최종 확인하였습니다.

---

## 📅 2026-06-09
### 뉴스 선별 기준 고도화 및 수집 한도 확장, 시장 요인/경제 지표 추출 통합 완료 (v0.4.9)

뉴스 개수 제한을 풀고 더 넓은 범위에서 유의미한 정보를 엄선하기 위해 뉴스 수집 구조를 15개로 대폭 확장하였으며, 수집된 뉴스 기사 분석을 기반으로 **오늘 시장의 주요 요인** 및 **주요 경제 지표**를 텔레그램 리포트에 동적으로 도출해 융합하는 고도화 리팩토링을 완료했습니다.

#### 1. 구현된 주요 변경 사항
- **설정 및 키워드 보강**:
  - [config/config.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/config.json): 국채, 기술주 관련 매크로 주요 키워드("미 국채", "국채 금리", "기술주", "treasury", "yields", "tech stocks")를 수집 설정에 대거 확충하였습니다.
- **수집 한도 확장**:
  - [src/main.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/main.py): 국내 및 해외 뉴스의 API 수집 한도를 기존 10개에서 15개로 상향하여 파이프라인 기사 풀을 대폭 넓혔습니다.
- **시장 요인 / 경제 지표 동적 분석 및 AI 선별 프롬프트 고도화**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py):
    - `format_news_list` 폴백 출력 뉴스 슬라이싱을 기존 5개에서 10개로 확대 적용했습니다.
    - `summarize_news_with_gemini` 의 AI 입력 기사 슬라이싱 한도를 15개로 상향하였습니다.
    - AI(Gemini)에게 **"기술주, 반도체 업황, 미 국채 금리, 지수에 직접적으로 영향을 미친 매크로성 중요 이슈만 엄선해라"**라는 자동 필터링 지침을 적용하여 노이즈 기사(단순 인사, 실적 단신 등)를 완벽 차단했습니다.
    - 당일 수집된 30여 개의 뉴스 기사 속에서 **"💡 오늘의 미국 시장 주요 요인"** 3~5가지와 당일 새로 발표된 **"📊 오늘 발표된 주요 경제 지표"** 결과/예상/이전 수치를 표 형식으로 동적 발굴해 내는 로직을 프롬프트에 종합 반영했습니다.
- **버전 갱신**:
  - [config/version.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/version.json): 프로그램 버전을 `0.4.9`로 갱신하고 버전 변경 이력을 추가하였습니다.
- **디버그 테스트**:
  - [Debug/015.debug_test.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/Debug/015.debug_test.py): 확장된 뉴스 수집과 AI 선별 카드뉴스, 시장 요인, 경제 지표 종합 리포트의 실제 텔레그램 전송 동작을 실발송을 통해 종합 입증하였습니다.

#### 2. 검증 결과
- **동적 분석 및 요약 카드 발송 테스트 (`Debug/015.debug_test.py`)** -> **성공**
  - 국채, 기술주 등 보강된 키워드 뉴스가 정상적으로 수집되었으며, AI가 수집된 기사를 통해 증시 상승/하락의 4대 원인(마이크론 반등, 트럼프 휴전 노력 등)을 정확히 도출해내고, 기대인플레 등 당일의 경제 지표 수치를 단일 <code> 표로 동적 생성하여 텔레그램 상에 파싱 에러(400 Bad Request) 없이 깨끗한 포맷으로 전송되는 것을 최종 검증 완료하였습니다.

---

## 📅 2026-06-09
### 뉴스 요약 영역의 카드뉴스 템플릿 레이아웃 개편 완료 (v0.4.8)

금융 뉴스 모바일 앱 스타일의 세련된 카드 레이아웃을 도입하여 뉴스 요약 영역의 가독성과 미적 완성도를 대폭 끌어올렸습니다. 텔레그램 HTML 포맷 한계 내에서 `<code>` 태그의 둥근 모서리 회색 배경 배지 효과를 활용하여 고급스러운 모바일 UI를 완벽 구현하였습니다.

#### 1. 구현된 주요 변경 사항
- **출처 및 시간 배지 카드뉴스 구조 도입**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py): 
    - `format_news_list` 폴백 함수 개편: 기사별 최상단에 `<code>출처 · 시간</code>` 형태의 배지를 표시하고 굵은 글씨로 제목 하이퍼링크를 삽입해 기사 카드들이 세련되게 정렬되도록 리팩토링했습니다.
    - `summarize_news_with_gemini` AI 요약 프롬프트 개편: Gemini API 요약 시 기사당 `[출처] · [시간]` 배지 정보, 굵은 제목 링크, 들여쓰기된 핵심 2줄 요약(`  • `), 그리고 주식 종목 연관 시 하단 해시태그 배지(예: `<code>#NVIDIA</code>`)가 정확하게 렌더링되어 출력되도록 지침을 전면 수정했습니다.
    - 뉴스 카드 사이의 구분을 명확히 하기 위해 얇은 구분선(`<code>──────────────────────────────</code>`)을 카드의 경계선으로 일체화했습니다.
- **버전 갱신**:
  - [config/version.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/version.json): 프로그램 버전을 `0.4.8`로 갱신하고 변경 내용을 기록하였습니다.
- **디버그 테스트**:
  - [Debug/014.debug_test.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/Debug/014.debug_test.py): 실시간 뉴스 수집 데이터와 연동하여 폴백 모드 및 Gemini API 카드뉴스 요약 모드 모두를 실행하고 실제 텔레그램 메시지로 실발송하여 카드뉴스 UI가 완벽히 출력되는 것을 검증하였습니다.

#### 2. 검증 결과
- **카드뉴스 발송 및 렌더링 실검증 (`Debug/014.debug_test.py`)** -> **성공**
  - 폴백 카드 및 Gemini AI 요약 카드가 텔레그램 모바일 앱 상에서 출처 배지, 굵은 하이퍼링크 제목, 들여쓰기 요약, 종목 해시태그 배지 형태로 완벽하게 어우러져 출력되는 것을 확인하였으며, HTML 파싱 오류도 전혀 발생하지 않음을 입증했습니다.

---

## 📅 2026-06-09
### 종가 고정폭 확장 및 표 내부 한글의 영문(DOW, NASDAQ 등) 완전 전환 완료 (v0.4.7)

비트코인(`103,456.78` 등 10자리)과 같은 긴 가격 수치를 안정적으로 수용하기 위해 종가 정렬 폭을 10자로 확장했습니다. 또한, 기존 `<pre>` 태그 및 행 단위 `<code>` 태그 적용 시 발생하던 텔레그램 렌더링 오류를 영구 해결하였습니다.
1. `<pre>` 태그를 사용하면 모바일 화면에서 표가 회색 'copy' 코드 상자로 감싸져 글자 크기가 지나치게 작아지는 문제가 있었습니다.
2. 각 행을 개별 `<code>` 태그로 쪼개어 감싸면, 줄 간의 가로 정렬이 미세하게 틀어지는 문제가 발생했습니다.
3. 가장 치명적으로, 텔레그램 `<code>` 태그 내부에서 모바일 스마트폰의 시스템 폰트 환경에 따라 **한글 1글자 너비가 공백 2글자 너비보다 좁게 표현되는 렌더링 자간 왜곡 현상**이 발견되었습니다. 이로 인해 한글 글자 수가 서로 다른 행들(예: 지수[한글2자] vs 다우존스[한글4자] vs S&P500[영문6자]) 간에 세로선 `|`이 전혀 정렬되지 않는 물리적 한계가 존재했습니다.

이를 극복하기 위해:
* 표 전체를 단 하나의 **`<code>...</code>` 단일 태그**로 감싸 복사 상자를 제거하고 일반 글씨 크기를 보장하였습니다.
* 표 내부의 모든 한글 텍스트(지수명, 헤더 등)를 **완벽한 영문 약칭(INDEX, TICKER, DOW, NASDAQ, SOX, US10Y, DXY 등)으로 전면 교체**하였습니다. 영문 모노스페이스는 모바일 기기 종류와 관계없이 공백과 100% 동일한 가로 너비를 가지므로, 자간 렌더링 왜곡이 원천 차단되어 세로선 `|` 위치가 소수점 한 자리 오차도 없이 수직으로 완벽하게 칼정렬됩니다.

#### 1. 구현된 주요 변경 사항
- **표 내부 한글의 영문 완전 전환 구현**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py): `INDEX_NAME_MAP`을 영어 약어로 전면 전환하고, 테이블 헤더 및 패딩 함수도 영문(`INDEX`, `TICKER`, `PRICE`, `CHANGE`) 기준으로 정렬되도록 리팩토링하였습니다.
- **테이블 단위 단일 <code> 래핑**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py): 테이블 전체 텍스트 행을 통째로 하나의 `<code>` 태그로 래핑하여 모노스페이스 비율을 유지했습니다.
- **디버그 테스트**:
  - [Debug/012.debug_test.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/Debug/012.debug_test.py): 비트코인 및 다우존스와 같은 9~10자리의 큰 수치를 포함한 모의 데이터를 활용하여, 실제 텔레그램 메시지 발송 시 세로 라인이 칼같이 수직 정렬되는 것을 성공적으로 실검증 완료하였습니다.
  - [Debug/013.debug_test.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/Debug/013.debug_test.py): 실시간 야후 파이낸스 데이터를 직접 수집해 와 전체 지표와 빅테크 종목 리포트를 텔레그램으로 최종 실발송하여 정렬 가독성을 최종 검증 완료하였습니다.

#### 2. 검증 결과
- **세로 칼정렬 텔레그램 메시지 실시간 발송 테스트 (`Debug/012.debug_test.py` & `Debug/013.debug_test.py`)** -> **성공**
  - 모바일 화면에서 복사 상자 없이 깔끔하고 큼직한 본문 글씨로 표가 출력되며, 한글 왜곡 문제가 원천 차단되어 헤더와 구분선, 데이터의 세로선 `|`가 수직으로 완벽하게 정렬되는 것을 최종 입증하였습니다.

---

## 📅 2026-06-09
### 다중행 고정폭 정밀 칼정렬을 위한 <pre> 태그 전환 완료 (v0.4.6)

텔레그램 HTML 모드에서 다중행 데이터를 테이블 형식으로 표현할 때 `<code>` 태그를 사용할 경우, 텔레그램 모바일 및 일부 PC 클라이언트에서 이를 가변폭 인라인 코드로 인식해 글자 렌더링 너비를 어긋나게 하던 원인을 발견해 수정했습니다. 다중행 표 블록 전체를 텔레그램 공식 블록 고정폭 태그 규격인 `<pre>...</pre>`로 감싸 표를 전송하도록 교정하였습니다. 이 변경으로 인해 한글 약칭 폭, 숫자 폭, 소수점 위치와 무관하게 모든 기기에서 세로 구분선(`|`)과 데이터 열이 한 치의 흐트러짐도 없이 칼같이 일직선으로 수직 정렬되는 완벽한 레이아웃을 제공합니다.

#### 1. 구현된 주요 변경 사항
- **다중행 표 고정폭 태그 전환**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py): `format_market_data` 내부에서 시장 지수 테이블 및 주요 종목 테이블, 그리고 구분선들의 `<code>` 태그를 모두 `<pre>` 태그로 교체했습니다.
- **버전 갱신**:
  - [config/version.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/version.json): 프로그램 버전을 `0.4.6`으로 갱신하고 변경 내용을 기록하였습니다.
- **디버그 테스트**:
  - [Debug/011.debug_test.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/Debug/011.debug_test.py): `<pre>` 태그 전환이 올바르게 렌더링되어 전송되는지 실제 텔레그램 실발송을 통해 검증을 완료하였습니다.

#### 2. 검증 결과
- **세로 칼정렬 텔레그램 메시지 실제 발송 테스트 (`Debug/011.debug_test.py`)** -> **성공**
  - 모바일 및 PC 텔레그램 화면에서 구분선 `|` 와 숫자들이 한 칸의 어긋남 없이 세로 방향으로 칼같이 일직선을 맞추어 정렬되는 결과를 육안으로 검증 완료하였습니다.

---

## 📅 2026-06-09
### 등락률 이모지 분리 정렬을 통한 테이블 세로 칼정렬 극대화 완료 (v0.4.5)

가변적인 모바일 폰트 환경에서 지수/종목 등락률 열의 이모지(🔺, 🔻, ➖) 렌더링 폭 차이로 인해 발생할 수 있는 미세한 세로 정렬 흐트러짐 문제를 완벽히 해결하였습니다. 등락률 수치 텍스트(`+1.20%` 등 순수 ASCII 문자)만 정확한 고정폭(7자) 우측 정렬로 패딩 처리한 후, 이모지는 패딩 영역 바깥 우측 끝에 공백 1칸을 띄우고 결합하게 정렬 로직을 고도화했습니다. 이로 인해 모든 모바일 텔레그램 화면에서 구분선과 열 데이터 수치들이 칼같이 세로로 정렬되는 상태를 완성하였습니다.

#### 1. 구현된 주요 변경 사항
- **이모지와 고정폭 수치 영역 분리 구현**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py): `format_market_data` 함수 내부에서 `change_val_str = f"{sign}{pct_change:.2f}%"`로 순수 수치 텍스트를 먼저 7자 정렬하고, 뒤에 `f" {emoji}"`를 붙여 정렬 영역에서 이모지를 제외시켰습니다.
- **버전 갱신**:
  - [config/version.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/version.json): 프로그램 버전을 `0.4.5`로 갱신하고 변경 내용을 기록하였습니다.
- **디버그 테스트**:
  - [Debug/010.debug_test.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/Debug/010.debug_test.py): 이모지 분리 정렬이 적용된 최종 리포트의 발송을 검증하는 신규 테스트 스크립트를 작성하여 테스트를 완료하였습니다.

#### 2. 검증 결과
- **세로 칼정렬 텔레그램 메시지 실제 발송 테스트 (`Debug/010.debug_test.py`)** -> **성공**
  - 모바일 텔레그램 화면에서 지표와 수치 데이터가 미세하게 밀리던 현상이 완전히 사라지고, 세로 컬럼 바 `|` 와 숫자들이 일직선으로 완벽하게 일치하는 것을 확인하였습니다.

---

## 📅 2026-06-09
### 모바일 가로폭 최적화 및 텔레그램 HTML 렌더링 모드 전환 완료 (v0.4.4)

스마트폰의 좁은 가로 폭 환경에서 지수/종목 표가 찌그러지거나 잘리지 않도록 지수명을 한글 약칭(예: "필라반도체", "미국채10년" 등)으로 전환하고 가로 컬럼 폭을 대폭 축소(전체 폭 35자 내외)하여 모바일 가로 뷰를 최적화했습니다. 또한, 구글 뉴스 RSS의 복잡한 URL 기호들로 인해 발생했던 텔레그램 마크다운 파싱 오류를 영구적으로 제거하기 위해 텔레그램 전송 모드를 **HTML 모드**로 전격 전환하였습니다. 이를 통해 URL과 관계없이 뉴스 헤드라인 글자 자체에 클릭 가능한 파란색 하이퍼링크가 정상적으로 연동되어 슬림한 메시지 레이아웃이 완성되었습니다.

#### 1. 구현된 주요 변경 사항
- **지수명 한글 약칭 매핑 사전 적용**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py): `INDEX_NAME_MAP`을 추가하여 "PHLX Semiconductor" -> "필라반도체" 등 지수명을 가독성 있는 한글 약칭으로 전환했습니다.
- **시장 데이터 표 폭 축소 및 HTML <code> 래핑**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py): `format_market_data`가 가로 컬럼 폭을 `10 | 9 | 10` (총 35자 내외)으로 구성하고, HTML `<code>` 태그로 묶어 고정폭이 텔레그램 내에서 깔끔하게 유지되게 하였습니다.
- **텔레그램 전송 엔진 HTML 파싱 모드 전환**:
  - [src/telegram_sender.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/telegram_sender.py): `parse_mode`를 `"HTML"`로 변경하여 마크다운 예외 문제를 원천 방지하였습니다.
- **뉴스 링크 태그 HTML화 및 Gemini 요약 지침 업데이트**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py): 뉴스 목록 폴백 함수와 AI 요약 생성 프롬프트를 수정하여 `<a href="...">`와 `<b>` HTML 서식을 강제 준수하게 하였습니다.
- **버전 갱신**:
  - [config/version.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/version.json): 프로그램 버전을 `0.4.4`로 갱신하고 변경 내용을 기록하였습니다.
- **디버그 테스트**:
  - [Debug/009.debug_test.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/Debug/009.debug_test.py): HTML 모드 전환 및 모바일용 단축 표 발송을 종합 검증하는 신규 테스트 스크립트를 작성해 실시간 발송 완료를 검증했습니다.

#### 2. 검증 결과
- **HTML 텔레그램 메시지 실제 발송 테스트 (`Debug/009.debug_test.py`)** -> **성공**
  - 복잡한 구글 뉴스 링크가 포함되어도 마크다운 에러로 인해 기사 링크 괄호가 지저분하게 노출되지 않고, 정상적으로 파란색 하이퍼링크 제목 형태로 깔끔하게 렌더링되어 발송되었습니다.
  - 지수 표의 한글명이 단축되어 모바일 화면 가로폭 내에 표가 일그러지지 않고 수직 정렬되어 가독성이 극대화되었습니다.

---

## 📅 2026-06-09
### 텔레그램 메시지 정렬 최적화 및 헤드라인 하이퍼링크 포맷 도입 완료 (v0.4.3)

한글 지수명 및 다양한 길이의 종목 티커가 포함되어 표 정렬이 어긋나는 문제를 해결하기 위해, 동아시아 문자 폭(한글 2칸, 영문/숫자 1칸)을 계산하는 정렬 로직을 적용하여 텔레그램 모노스페이스 폰트 내에서 열 정렬을 완벽하게 맞추었습니다. 또한 외신 뉴스 요약 메시지의 가독성을 높이기 위해 불필요한 원문 기사 바로가기 화살표 행을 제거하고, 번역된 헤드라인 제목에 직접 원문 하이퍼링크를 입혀 클릭을 통해 바로 연결되는 심플하고 직관적인 레이아웃으로 개편하였습니다.

#### 1. 구현된 주요 변경 사항
- **Unicode 기반 표시 폭 정렬 헬퍼 추가**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py): `get_display_width`와 `pad_string` 함수를 신설하여 문자 폭 단위 정렬을 보장합니다.
- **시장 지수 및 주요 종목 테이블 개선**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py): `format_market_data`가 표시 폭을 반영해 지수명(폭 18), 종가(폭 10), 등락률(폭 12)로 컬럼을 정렬하도록 개편했습니다.
- **뉴스 헤드라인 하이퍼링크 단순화**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py): `format_news_list` 폴백 출력과 `summarize_news_with_gemini` 프롬프트 템플릿 요구사항을 수정하여, `숫자 이모지 *[[출처] 번역된 기사 제목](원문 링크)*` 형태로만 제목을 한국어로 번역 출력하고 별도 화살표 링크 줄은 완전히 배제하도록 하였습니다.
- **버전 갱신**:
  - [config/version.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/version.json): 프로그램 버전을 `0.4.3`으로 갱신하고 변경 내용을 기록하였습니다.
- **디버그 테스트**:
  - [Debug/007.debug_test.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/Debug/007.debug_test.py): 신규 고정폭 계산 테이블 정렬 및 하이퍼링크 뉴스 포맷 렌더링 기능을 종합 검증하는 스크립트를 작성하여 테스트를 완료하였습니다.

#### 2. 검증 결과
- **정렬 및 포맷팅 종합 검증 (`Debug/007.debug_test.py`)** -> **성공**
  - "미국 10년물 국채" 등의 한글 지수명과 "BTC-USD" 등의 긴 티커가 포함되어도 가로바(`|`) 구분이 흐트러짐 없이 똑바로 열을 맞춰 정렬되는 것을 콘솔 상에서 입증했습니다.
  - 번역된 뉴스 제목에 하이퍼링크(`[제목](링크)`)가 완벽하게 결합되고, 기존의 군더더기 같던 화살표 링크 줄이 제거되어 전체 요약 메시지가 모바일에 최적화된 컴팩트한 사이즈로 깔끔해졌음을 확인하였습니다.

---

## 📅 2026-06-09
### 미국 영어 뉴스 수집 및 AI 한국어 번역 요약 연동 완료 (v0.4.0)

미국의 신뢰도 높은 금융 전문 외신 매체들(Yahoo Finance, CNBC, Reuters 등)로부터 영문 매크로 및 반도체 소식을 직접 수집하고, 이를 Gemini 2.5-flash 모델을 통해 깔끔한 한국어 2줄 요약본으로 번역하여 제공하는 기능을 성공적으로 구현하였습니다. 

#### 1. 구현된 주요 변경 사항
- **미국 영어 뉴스 설정 로드**:
  - [config/config.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/config.json): 영문 검색 키워드(`us_news_keywords`), 영어 제외 키워드(`us_exclude_keywords`), 영문 타겟 금융 도메인(`us_target_domains`) 설정을 추가하였습니다.
  - [config/version.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/version.json): 프로그램 버전을 `0.4.0`으로 갱신하고 버전 변경 이력을 추가하였습니다.
- **미국 뉴스 수집 엔진 개발**:
  - [src/collector.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/collector.py):
    - 영문 구글 뉴스 RSS 검색을 통해 미국 도메인들에서 핀포인트로 최신 뉴스를 긁어오는 `get_us_focused_news` 함수를 신설하였습니다.
    - 한국어 수집과 동일하게 기사 발행일 3일 이내 필터 및 미국 제외 키워드 필터가 안전하게 적용됩니다.
- **분리형 번역/요약 엔진 및 프롬프트 고도화**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py):
    - `summarize_news_with_gemini` 함수가 한국어 뉴스 목록(`ko_news_list`)과 영문 뉴스 목록(`us_news_list`)을 각각 독립 인자로 수신하도록 설계했습니다.
    - 리포트 내에 `📰 [글로벌 금융/증시 요약 뉴스]` 섹션과 `🇺🇸 [미국 현지 시황 & 외신 요약]` 섹션이 나누어 표현되도록 고도화된 프롬프트 템플릿을 구성했습니다.
    - API 키 부재 시 두 영역의 기사 링크 목록을 각각 분류해 제공하도록 폴백(`format_news_list`) 로직을 개편했습니다.
- **메인 파이프라인 연동**:
  - [src/main.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/main.py): 한국어 뉴스와 미국 영문 뉴스를 함께 수집 및 가공하는 파이프라인을 완성하고, 텔레그램 메시지 구조에 분리 요약문을 합치도록 조율했습니다.
- **디버그 테스트**:
  - [Debug/005.debug_test.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/Debug/005.debug_test.py): 신규 영문 뉴스 수집기와 Gemini 한국어 번역 요약 흐름을 단독으로 검증하는 검증 스크립트를 새로 작성했습니다.
  - [Debug/003.debug_test.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/Debug/003.debug_test.py): 영문 뉴스 수집 및 가공 로직을 통합 테스트 스크립트에 이식 완료했습니다.

#### 2. 검증 결과
- **영문 기사 수집 및 Gemini 번역 요약 단독 테스트 (`Debug/005.debug_test.py`)** -> **성공**
  - 미국의 5개 주요 외신사들로부터 영문 최신 시황 기사들을 차단 없이 정확히 수집하였습니다.
  - 수집된 영어 뉴스 원문을 Gemini 2.5-flash 모델이 자연스러운 국내 투자 금융 용어로 번역 및 한국어 요약에 성공함을 화면 출력을 통해 입증했습니다.

---

## 📅 2026-06-09
### Gemini 요약 복구 및 텔레그램 줄바꿈 청크 분할 개선 완료 (v0.3.0)

사용자가 제공한 새로운 API 키를 연동하고, 404 API 오류가 났던 이전 `gemini-pro` 모델을 최신 호환 모델인 `gemini-2.5-flash`로 갱신하여 인공지능 요약 엔진을 완벽히 복구하였습니다. 또한, 텔레그램 메시지 발송 시 마크다운 파싱 에러(4000자 초과 청크 분할 시 마크다운 태그가 끊기는 현상)를 방지하기 위해 줄바꿈 단위로 안전하게 쪼개는 분할 로직을 추가 적용했습니다.

#### 1. 구현된 주요 변경 사항
- **Gemini 모델 최신화**:
  - [src/summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py):
    - v1beta API 버전에서 더 이상 지원되지 않는 구버전 모델 `gemini-pro` 대신, 현재 계정에서 사용 가능하고 빠른 속도를 지닌 최신 모델 **`gemini-2.5-flash`**로 업데이트하였습니다.
- **텔레그램 분할 전송 안정성 개선**:
  - [src/telegram_sender.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/telegram_sender.py):
    - 텔레그램 메시지 크기 제한(4000자)으로 잘릴 때 `*` 이나 `[` 등 마크다운 시작 태그와 종료 태그가 서로 다른 청크로 나뉘어 발생하는 파싱 에러(`Bad Request: can't parse entities`)를 예방하기 위해, **줄바꿈(`\n`) 단위로 합산하여 청크를 만드는 안전 분할 알고리즘**을 적용했습니다.
- **버전 갱신 및 설정**:
  - [config/version.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/version.json): 프로그램 버전을 `0.3.0`으로 갱신하고 버전 변경 이력을 보충하였습니다.
- **디버그 테스트**:
  - [Debug/004.debug_test.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/Debug/004.debug_test.py): Gemini API 모델 목록을 조회하고, `gemini-2.5-flash` 생성 성공 여부를 검증하는 신규 테스트 스크립트를 작성하여 모델 갱신 및 사용량 한도 한계를 진단하였습니다.

#### 2. 검증 결과
- **모델 조회 및 생성 검증 (`Debug/004.debug_test.py`)**:
  - `gemini-2.5-flash` 모델이 신규 API 키를 사용하여 텍스트 생성을 정상적으로 수행함을 확인(성공).
- **종합 시나리오 검증 (`Debug/003.debug_test.py`)**:
  - 최근 수집된 테크 및 매크로 뉴스가 `gemini-2.5-flash`를 통해 한국어 요약본(마크다운 형태)으로 올바르게 번역/가공된 후, 개선된 안전 분할 방식을 거쳐 사용자 텔레그램 방으로 파싱 에러 없이 **완전한 포맷팅 형태로 전송 성공**하였습니다.

---

## 📅 2026-06-09
### 전문 금융 플랫폼 연동 및 과거 기사 유입 차단 날짜 필터 도입 완료 (v0.2.3)

사용자의 피드백과 분석 대상 사이트(인베스팅닷컴, 트레이딩뷰, 트레이딩키 등) 연동 의견을 적극 수용하여, 해외 금융 정보의 신뢰도 및 최신성을 최우선으로 개선하였습니다.

#### 1. 구현된 주요 변경 사항
- **금융 전문 플랫폼 조준 수집 설계**:
  - [config/config.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/config.json):
    - 공식 RSS가 부재하거나 크롤링이 차단되는 구조를 극복하기 위해, 구글 뉴스 내 타겟 도메인 필터 목록(`target_domains`: `["hankyung.com", "investing.com", "tradingview.com", "tradingkey.com"]`)을 설정에 추가하였습니다.
  - [config/version.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/version.json): 프로그램 버전을 `0.2.3`으로 업데이트하였습니다.
- **날짜 필터(is_recent) 도입 및 수집 리팩토링**:
  - [src/collector.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/collector.py):
    - 구글 뉴스 연동 시 과거의 옛날 기사(예: 스티브 잡스 연설, 과거 초전도체 이슈 등)가 섞여 유입되는 현상을 방지하기 위해, 기사 발행일(`published_parsed`)을 기준으로 **최근 3일 이내의 기사만 수집하는 `is_recent` 필터 함수**를 구현하였습니다.
    - 금융 전문 플랫폼의 기사들만 골라서 핀포인트 수집하는 `get_domain_focused_news` 함수를 신설하고, `get_combined_news` 에서 이들을 병합해 중복을 거른 후 인베스팅닷컴, 트레이딩뷰, 트레이딩키, 한국경제 출처 뉴스가 최상단에 먼저 노출되도록 정렬 로직을 반영하였습니다.
- **소스 및 테스트 코드 갱신**:
  - [src/main.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/main.py): `target_domains`를 로드하여 뉴스 수집 엔진에 연동하였습니다.
  - [Debug/001.debug_test.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/Debug/001.debug_test.py), [Debug/002.debug_test.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/Debug/002.debug_test.py), [Debug/003.debug_test.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/Debug/003.debug_test.py): `target_domains` 파라미터 전달 및 검증 테스트 코드로 업데이트 완료하였습니다.

#### 2. 검증 결과
- **단위 및 통합 디버그 테스트 완료**:
  - `Debug/001.debug_test.py` (다각화 및 날짜 검증 테스트) -> **성공** (날짜 필터 덕분에 과거 기사들이 완전히 차단되고, 최근 24~48시간 이내의 뉴욕증시 개장 및 매크로 하락 마감 등 최신 시황 한글 뉴스만 10개 수집됨을 검증)
  - `Debug/003.debug_test.py` (통합 전송 테스트) -> **성공** (해외 금융 및 미국 시황에 정밀 타겟팅된 고품질 아침 리포트가 사용자 텔레그램으로 정상 전송 완료)

---

## 📅 2026-06-09
### 국내 대기업/증시 잡음 뉴스 제거 및 해외 증시 시황 위주 최적화 개편 완료 (v0.2.2)

수집된 뉴스 기사가 주로 국내 대기업(삼성, SK 등) 동향이나 국내 증시 관련 단신인 문제를 해결하기 위해 국내 관련 노이즈를 완벽하게 차단하고 미국 뉴욕 증시 및 글로벌 금융 거시 매크로 뉴스 위주로 수집되도록 제외 키워드(`exclude_keywords`)를 적용하였습니다.

---

## 📅 2026-06-08
### 미국 시장 정보 및 반도체 업황 뉴스 텔레그램 자동 전송 시스템 구현 완료

매일 아침 자동으로 구동되는 미국 시장(US Market) 지수 및 반도체 업계 소식 발송 시스템 개발을 완료하였습니다. 로컬 PC 구동에 의존하지 않도록 GitHub Actions 클라우드 환경을 이용해 무료 자동화 스케줄링을 완료했습니다.

---
