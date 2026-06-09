# 작업 목록 (Task List) - v0.5.0

- [x] `config/version.json` 버전 및 히스토리 업데이트 (0.5.0)
- [x] `src/main.py` 소스 코드 수정 (국내 뉴스 수집 부분 생략 및 빈 리스트 처리)
- [x] `src/summarizer.py` 소스 코드 수정 (국내 뉴스 요약 및 목록 렌더링 제거, 외신 단독 개편)
  - [x] `format_news_list` 폴백 내 국내 뉴스 렌더링 삭제
  - [x] `summarize_news_with_gemini` 프롬프트 내 국내 뉴스 분석/출력 제거 및 외신 단독 포커스
- [x] 디버그 테스트 파일 작성 및 검증
  - [x] `Debug/016.debug_test.py` 스크립트 작성 (외신 단독 수집 및 텔레그램 발송)
  - [x] 실제 텔레그램 카드뉴스 메시지 발송 검증
- [x] 문서 갱신
  - [x] `DOCS/walkthrough.md`에 외신 단독 개편 히스토리 반영
