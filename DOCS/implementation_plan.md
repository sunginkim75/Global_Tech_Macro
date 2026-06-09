# [외신 단독 포커스 뉴스 리포트 개편 계획] (v0.5.0)

본 계획서는 사용자의 피드백을 반영하여 데일리 리포트에서 국내 금융/증시 요약 뉴스를 완전히 제거하고, 오직 미국의 신뢰도 높은 금융 외신(Yahoo Finance, CNBC, Reuters 등) 뉴스 위주로 자동 선별 및 요약하여 슬림하고 전문적인 리포트를 구성하는 개편 작업을 다룹니다.

## User Review Required

> [!IMPORTANT]
> **주요 설계 변경 사항**:
> - **국내 뉴스 수집 생략**: 불필요한 국내 뉴스 수집 과정을 제거하여 데이터 수집 속도와 네트워크 효율성을 대폭 개선합니다.
> - **리포트 슬림화**: 텔레그램 메시지 내에서 국내 뉴스 섹션을 완전히 배제하고, 오직 **`[오늘의 미국 시장 주요 요인]`, `[오늘 발표된 주요 경제 지표]`, `[미국 현지 시황 & 외신 요약]`**만 담아 가독성을 극대화합니다.
> - **AI 프롬프트 단순화**: Gemini가 국내 뉴스를 가공하는 과정을 없애고, 오직 외신 기사(영어 뉴스)를 고품질 한국어로 번역/요약하는 데 역량을 집중하게 유도합니다.

## Proposed Changes

### 1. 설정 및 버전 관리 업데이트

#### [MODIFY] [version.json](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/config/version.json)
- 프로그램 버전을 `0.5.0`으로 업데이트하고 국내 뉴스 제거 및 외신 단독 개편 내역을 히스토리에 반영합니다.

---

### 2. 소스 코드 수정 (외신 단독 요약 파이프라인 개편)

#### [MODIFY] [main.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/main.py)
- 국내 뉴스 수집 함수 호출(`get_combined_news`)을 생략하고 `news_list`를 빈 리스트(`[]`)로 넘기거나 수집 과정을 주석 처리하여 불필요한 연산을 방지합니다.

#### [MODIFY] [summarizer.py](file:///c:/Users/SunginKIm/PYthon_WorkSpace/Global_Tech_Macro/src/summarizer.py)
- **`format_news_list` 개편**:
  - 국내 뉴스 렌더링 섹션을 완전히 삭제하고, 미국 외신 목록만 출력하도록 변경합니다.
- **`summarize_news_with_gemini` 개편**:
  - 한국어 뉴스 입력 구성부(`ko_news_input`) 및 프롬프트 인자 주입부를 제거합니다.
  - Gemini 프롬프트를 전면 개편하여, `📰 [글로벌 금융/증시 요약 뉴스]` 섹션을 완전히 제거하고 오직 `🇺🇸 [미국 현지 시황 & 외신 요약]`만 출력하도록 지침을 단순화합니다.

---

## Verification Plan

### Automated Tests
- **`Debug/016.debug_test.py` [NEW]**
  - 실시간 외신 뉴스(15개 한도)만 수집하여, 국내 뉴스 섹션 없이 깔끔한 시장 주요 요인, 경제 지표 및 미국 외신 요약 카드로만 구성된 텔레그램 리포트가 정상 발송되는지 검증합니다.

### Manual Verification
- 전송된 텔레그램 리포트에서 국내 뉴스 요약이 완전히 배제되고, 오직 양질의 미국 외신 번역 요약 카드와 당일 경제 지표/시장 요인만 미려하게 노출되는지 최종 확인합니다.
