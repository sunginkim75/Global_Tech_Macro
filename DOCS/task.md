# 작업 목록 (Task List) - v0.6.1

- [x] `config/config.json` 내 `us_exclude_keywords`에 지엽적 단신 제외 키워드 추가
- [x] `config/config.json` 내 `us_news_keywords`에 주요 빅테크 종목 및 실적/급락 관련 키워드 보강
- [x] `config/config.json` 내 `TQQQ`/`SOXL`을 `stocks`에서 `indices`로 이동 및 순서 조정 (S&P 500, Nasdaq 바로 뒤)
- [x] `config/config.json` 내 `stocks` 목록에 5개 종목 추가 및 시총순 재배치 정렬
- [x] `src/main.py` 내 ±5.0% 이상 변동 종목 감지 시 핀포인트 뉴스 추가 수집 로직 구현
- [x] `src/summarizer.py` 내 `STOCK_NAME_MAP` 추가 및 WTI/BTC 출력 명칭 치환
- [x] `src/summarizer.py` 내 `INDEX_NAME_MAP`에 `TQQQ`/`SOXL` 추가
- [x] `src/summarizer.py` 내 Gemini 요약 프롬프트에 지엽적 단신 배제 규칙 강화
- [x] `config/version.json` 버전 및 히스토리 업데이트 (v0.6.1)
- [x] 디버그 테스트 파일 작성 및 검증
  - [x] `Debug/019.debug_test.py` 스크립트 작성 및 [x] 텔레그램 실발송 검증
- [x] 문서 갱신
  - [x] `DOCS/walkthrough.md`에 v0.6.1 개편 히스토리 반영
- [ ] Git commit 및 push (유저 컨폼 후 실행)

