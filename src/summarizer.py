# -*- coding: utf-8 -*-
import os
import google.generativeai as genai
import unicodedata
import email.utils
from datetime import datetime, timezone

def get_relative_time_str(pub_date_str):
    """
    RSS 발행 시간 문자열을 현재 기준 상대 시간(예: 10분 전, 2시간 전)으로 계산합니다.
    """
    if not pub_date_str:
        return "최근"
    try:
        dt = email.utils.parsedate_to_datetime(pub_date_str)
        now = datetime.now(timezone.utc)
        diff = now - dt
        diff_seconds = diff.total_seconds()
        
        if diff_seconds < 60:
            return "방금 전"
        elif diff_seconds < 3600:
            return f"{int(diff_seconds // 60)}분 전"
        elif diff_seconds < 86400:
            return f"{int(diff_seconds // 3600)}시간 전"
        elif diff_seconds < 86400 * 3:
            return f"{int(diff_seconds // 86400)}일 전"
        else:
            return dt.strftime("%m-%d")
    except Exception:
        return "최근"

def get_display_width(text):
    """
    문자열이 텔레그램 모노스페이스 폰트에서 차지하는 실제 화면상의 너비를 계산합니다.
    한글/전각 문자는 2, 영문/숫자/반각 문자는 1로 계산합니다.
    """
    width = 0
    for char in str(text):
        if unicodedata.east_asian_width(char) in ('F', 'W', 'A'):
            width += 2
        else:
            width += 1
    return width

def pad_string(text, target_width, align='left'):
    """
    실제 표시 넓이를 기준으로 문자열에 공백을 채워 정렬합니다.
    """
    text_str = str(text)
    text_width = get_display_width(text_str)
    pad_len = max(0, target_width - text_width)
    if align == 'left':
        return text_str + ' ' * pad_len
    elif align == 'right':
        return ' ' * pad_len + text_str
    else:
        left_pad = pad_len // 2
        right_pad = pad_len - left_pad
        return ' ' * left_pad + text_str + ' ' * right_pad

INDEX_NAME_MAP = {
    "S&P 500": "S&P500",
    "Nasdaq": "NASDAQ",
    "TQQQ": "TQQQ",
    "SOXL": "SOXL",
    "Dow Jones": "DOW",
    "PHLX Semiconductor": "SOX",
    "VIX": "VIX",
    "미국 10년물 국채": "US10Y",
    "미국 30년물 국채": "US30Y",
    "미국 달러지수": "DXY"
}

STOCK_NAME_MAP = {
    "CL=F": "WTI",
    "BTC-USD": "BTC"
}

def format_market_data(market_data):
    """
    수집된 주가 데이터를 텔레그램 HTML 표 형식으로 포맷팅합니다.
    모바일 폭에 최적화하여 35자 내외의 좁은 가로 폭 테이블을 빌드합니다.
    이모지 렌더링 너비 차이로 인한 정렬 흐트러짐을 방지하기 위해 이모지를 패딩 영역에서 제외합니다.
    다중행 고정폭 정렬을 보장하고 복사 상자 발생 및 폰트 렌더링 왜곡을 방지하기 위해 단일 <code> 태그로 감쌉니다.
    v0.5.1: 등락 표시 이모지를 한국 투자자 정서(상승: 🔺, 하락: 🔵)로 변경합니다.
    """
    lines = []
    lines.append("📊 <b>[미국 증시 및 주요 종목 현황]</b>")
    lines.append("<code>──────────────────────────────</code>")
    
    # 1. 시장 지수
    lines.append("\n▪️ <b>주요 시장 지수</b>")
    table_lines = []
    table_lines.append(f"{pad_string('INDEX', 10)} | {pad_string('PRICE', 10)} | {pad_string('CHANGE', 8)}")
    table_lines.append(f"{'-'*10} | {'-'*10} | {'-'*8}")
    
    indices = market_data.get("indices", {})
    for name, info in indices.items():
        display_name = INDEX_NAME_MAP.get(name, name)
        
        if "error" in info:
            table_lines.append(f"{pad_string(display_name, 10)} | {pad_string('-', 10, 'right')} | 오류")
            continue
            
        close = info["close"]
        pct_change = info["pct_change"]
        emoji = "🔴" if pct_change > 0 else "🔵" if pct_change < 0 else "➖"
        sign = "+" if pct_change > 0 else ""
        
        close_str = f"{close:,.2f}"
        change_val_str = f"{sign}{pct_change:.2f}%"
        change_display = f"{pad_string(change_val_str, 7, 'right')} {emoji}"
        
        table_lines.append(f"{pad_string(display_name, 10)} | {pad_string(close_str, 10, 'right')} | {change_display}")
        
    lines.append(f"<code>" + "\n".join(table_lines) + "</code>")
    
    # 2. 주요 종목
    lines.append("\n▪️ <b>주요 빅테크 & 반도체</b>")
    stock_lines = []
    stock_lines.append(f"{pad_string('TICKER', 10)} | {pad_string('PRICE', 10)} | {pad_string('CHANGE', 8)}")
    stock_lines.append(f"{'-'*10} | {'-'*10} | {'-'*8}")
    
    stocks = market_data.get("stocks", {})
    for name, info in stocks.items():
        if "error" in info:
            continue
            
        ticker = info.get("ticker", name)
        display_ticker = STOCK_NAME_MAP.get(ticker, ticker)
        close = info["close"]
        pct_change = info["pct_change"]
        
        emoji = "🔴" if pct_change > 0 else "🔵" if pct_change < 0 else "➖"
        sign = "+" if pct_change > 0 else ""
        
        close_str = f"{close:,.2f}"
        change_val_str = f"{sign}{pct_change:.2f}%"
        change_display = f"{pad_string(change_val_str, 7, 'right')} {emoji}"
        
        stock_lines.append(f"{pad_string(display_ticker, 10)} | {pad_string(close_str, 10, 'right')} | {change_display}")
        
    lines.append(f"<code>" + "\n".join(stock_lines) + "</code>")
    return "\n".join(lines)

def format_news_list(ko_news_list, us_news_list):
    """
    수집된 뉴스 리스트를 텔레그램 메시지로 요약하여 전달합니다. (폴백 모드)
    v0.5.0에서는 국내 뉴스를 완전히 제외하고 오직 미국 현지 금융 외신(us_news_list)만 포맷팅합니다.
    헤드라인 제목 자체에 하이퍼링크를 삽입해 포맷을 깔끔하게 간소화합니다.
    """
    if not us_news_list:
        return "최근 수집된 주요 외신 뉴스가 없습니다."

    lines = []
    
    lines.append("🇺🇸 <b>[미국 현지 금융 외신 동향]</b>")
    lines.append("<code>──────────────────────────────</code>")
    for item in us_news_list[:10]:
        rel_time = get_relative_time_str(item.get("published"))
        source = item.get("source", "외신")
        lines.append(f"<code>[번역 필요] {source} · {rel_time}</code>")
        lines.append(f"<b><a href=\"{item['link']}\">{item['title']}</a></b>")
        lines.append("<code>──────────────────────────────</code>")
            
    return "\n".join(lines).strip()

def summarize_news_with_gemini(ko_news_list, us_news_list, api_key=None, market_data=None):
    """
    Gemini API를 사용하여 뉴스 기사들을 한국어로 요약 및 번역합니다.
    v0.5.0에서는 국내 뉴스를 완전히 제외하고 미국 현지 금융 외신만 번역/요약합니다.
    v0.5.1: 실제 시장 등락률(market_data)을 인지하여 시장 상태와 모순되지 않는 균형 잡힌 요약 리포트를 구성합니다.
    """
    if not us_news_list:
        return "수집된 외신 뉴스가 없습니다."
        
    if not api_key:
        print("[정보] GEMINI_API_KEY가 등록되어 있지 않아 폴백 목록 모드로 전송합니다.")
        return format_news_list(None, us_news_list)
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # 미국 영어 뉴스 입력 텍스트 구성 (최대 15개 후보군)
        us_news_input = []
        for idx, item in enumerate(us_news_list[:15], 1):
            rel_time = get_relative_time_str(item.get("published"))
            us_news_input.append(f"기사 {idx}\n출처: {item['source']}\n시간: {rel_time}\n제목: {item['title']}\n링크: {item['link']}")
            
        us_news_section = "\n\n".join(us_news_input)
        
        # 실제 시장 등락률 파악하여 텍스트 주입
        market_status_text = "N/A"
        if market_data:
            status_parts = []
            for name, info in market_data.get("indices", {}).items():
                if "error" not in info:
                    status_parts.append(f"{name}({info.get('pct_change', 0):+.2f}%)")
            for name, info in market_data.get("stocks", {}).items():
                if "error" not in info:
                    status_parts.append(f"{info.get('ticker', name)}({info.get('pct_change', 0):+.2f}%)")
            market_status_text = ", ".join(status_parts)
        
        prompt = (
            "너는 전문 금융 투자 분석가다. 아래 제공된 미국 현지 금융 외신의 뉴스 목록을 분석해서 "
            "당일 미국 시장(증시)의 종합 동향을 정리하고, 각 기사별 핵심 정보를 명확한 한국어로 번역 및 요약하여 텔레그램 HTML 메시지로 포맷팅해라.\n\n"
            "<b>출력 형식 요구사항 (반드시 이 순서대로 출력할 것)</b>:\n"
            "1. 💡 <b>[오늘의 미국 시장 주요 요인]</b>\n"
            "   - 제공된 기사 전체를 종합 분석하여, 당일 뉴욕 증시 상승 또는 하락의 직접적인 배경이 된 핵심 마켓 드라이버 3~5가지를 한 줄씩 불렛(`• `) 형식으로 한글 요약해라.\n"
            "   - 예시:\n"
            "     • 마이크론 반동(+10%) 등 반도체주 상승이 시장 견인\n"
            "     • 트럼프 전 대통령의 이란-이스라엘 중재 노력에 따른 투자 심리 개선\n\n"
            "2. 📊 <b>[오늘 발표된 주요 경제 지표]</b> (뉴스에 관련 언급이 있는 경우에만 표 형식으로 생성, 없으면 이 섹션은 생략 가능)\n"
            "   - 오늘 새로 발표된 주요 경제 지표(예: 뉴욕 기대인플레이션, CPI, 고용 지표, 국채 입찰 등)의 명칭, 발표 수치(결과), 시장 예상치(예상), 이전 수치(이전)를 뉴스 기사 텍스트 속에서 찾아내어 아래의 고정폭 표 형태로 빌드해라.\n"
            "   - 표 양식 (모바일 폭에 맞게 아래와 같이 <code> 래핑을 단일 블록으로 정확히 유지할 것):\n"
            "     <code>지표명            | 결과   | 예상   | 이전\n"
            "     ──────────────────────────────────────\n"
            "     뉴욕 기대인플레(5월)| 3.46%  | 3.72%  | 3.64%</code>\n\n"
            "3. 🇺🇸 <b>[미국 현지 시황 & 외신 요약]</b> (영어 뉴스 번역 및 요약)\n\n"
            "<b>뉴스 요약 카드 세부 지침</b>:\n"
            "- 기사별 요약 카드는 반드시 아래의 레이아웃 구조를 정확히 준수하여 출력할 것:\n"
            "  <code>번역 · [출처] · [시간]</code>\n"
            "  <b><a href=\"원문 링크\">(번역된) 기사 제목</a></b>\n"
            "    • 핵심 요약 1행\n"
            "    • 핵심 요약 2행\n"
            "  (선택) <code>#연관종목명</code> (연관된 주식 종목 또는 섹터 태그가 명확히 있을 때만 배지로 삽입)\n"
            "  <code>──────────────────────────────</code>\n\n"
            "  *주의 및 세부 지침*:\n"
            "  - **핵심 뉴스 자동 선별 지침 (필수 및 절대 준수)**:\n"
            "    - 고정된 개수 제한을 두지 말고, 제공된 뉴스 기사들 중 **인플레이션 지표(CPI, PCE), 연방준비제도(Fed)의 금리 방향성 및 FOMC 회의 결과, 미국 국채 금리 변동, 주요 지수(나스닥, S&P 500 등)의 전체적인 장세 동향과 같은 거시경제(매크로) 시황**을 최우선(1순위)으로 선별해라.\n"
            "    - 2순위로 **반도체 업황 전반의 변화 및 공급망 동향, 하이퍼스케일러들의 AI 인프라 투자(CAPEX) 흐름, 주요 기업들의 분기 실적(Earnings) 발표, 혹은 대형 IPO(예: SpaceX 등)로 인한 증시 내 자금 이동 및 로테이션 우려**를 선별해라.\n"
            "    - **[중요] 지엽적인 기업 단신 배제 규칙**: 개별 기업의 단순 신제품 발표, 소프트웨어/OS 업데이트(예: Apple Siri 기능 개선, Apple Intelligence 일반 기능 소개 등), 지엽적인 제품 리뷰, 루머나 유출 소식 등은 아무리 유명한 기업의 기사라도 **미국 증시 전반의 향방에 직접적인 지수 변동이나 큰 매크로 흐름을 초래하지 않는 한 요약 대상에서 완전히 제외**해라. 미국 증시 전체 흐름을 확실히 대변할 수 있는 매크로 시황과 무게감 있는 핵심 소식으로만 엄격히 필터링 및 슬림화해야 한다.\n"
            "  - [출처]와 [시간] 부분은 뉴스 입력의 '출처' 필드와 '시간' 필드 값을 그대로 활용해라. "
            "예를 들어, 출처가 'Yahoo Finance'이고 시간이 '10분 전'이면 `<code>번역 · Yahoo Finance · 10분 전</code>` 처럼 '번역 · ' 접두사를 무조건 붙여서 생성해라. (외신 기사는 모두 한글 번역 요약이므로 `<code>번역 · [출처] · [시간]</code>` 형식이어야 한다.)\n"
            "  - 외신 기사의 제목은 한국인 투자자가 이해하기 쉽도록 반드시 한글 헤드라인으로 자연스럽게 번역해서 출력해라.\n"
            "  - 기사 제목(헤드라인) 전체에 텔레그램 HTML 하이퍼링크 서식인 `<a href=\"링크\">제목</a>`을 적용해라. 이때 태그 닫기와 따옴표 처리에 각별히 주의하여 HTML 파싱 오류가 나지 않도록 해라. 출처를 제외한 순수 번역된 제목 전체가 굵은꼴(<b>) 안에 HTML 하이퍼링크로 완벽히 래핑되어야 한다. 예: `<b><a href=\"https://finance.yahoo.com/news/1\">미국 연준 금리 인상 속도 조절 시사</a></b>`\n"
            "  - 기사 바로가기 화살표 행이나 기사 링크만 나열하는 행은 절대로 포함하지 마라. 제목 자체에 링크를 거는 것만으로 충분하다.\n"
            "  - 마크다운 서식(*, _, `, [text](url)) 대신 텔레그램에서 파싱 가능한 HTML 태그(<b>, <i>, <code>, <a>)만 사용해라. 특히 HTML 엔티티나 괄호가 누락되지 않도록 검증해라.\n"
            "  - 요약 행의 앞에는 공백 2개(들여쓰기)을 주고, 시작 기호로 특수문자 bullet(`  • `)을 사용해야 한다.\n"
            "  - 기사들 사이에는 구분선 `<code>──────────────────────────────</code>`을 정확히 삽입해라.\n\n"
            "4. 영어 뉴스는 어색한 직역을 배제하고, 우리나라 개인 투자자들이 직관적으로 이해할 수 있는 자연스러운 한국어 금융 용어로 번역 및 요약할 것.\n"
            "5. 불필요한 서론이나 결론(예: '요약본입니다' 등)은 완전히 생략하고 분류된 결과만 반환할 것.\n"
            "6. **중요: 실제 증시 등락 상태와 요약 내용의 정합성 유지 (필수)**:\n"
            f"   - 오늘 실제 미국 시장 지수 및 주요 종목의 등락률 현황은 다음과 같다: [{market_status_text}]\n"
            "   - 실제 지수와 종목들이 대부분 크게 하락(음수 등락률)하고 있다면, 수집된 뉴스 목록에 과거의 일방적인 상승 호재성 뉴스만 들어있다 하더라도 단순히 상승 분위기만 나열하여 실제 증시 상황(폭락세)과 모순되는 뚱딴지같은 리포트를 생성하지 마라.\n"
            "   - 증시가 하락세일 때는 뉴스 기사들 속에서 하락/조정의 배경(예: 기술주/반도체 고점 부담에 따른 차익 실현, 하이퍼스케일러 투자 둔화 우려, 기업 실적 실망감, 연준 금리 인하 지연, 국채 금리 상승 등)을 최우선적으로 파악하여 '💡 오늘의 미국 시장 주요 요인'에 반영하고, 개별 요약 카드에서도 시장 조정의 맥락(특히 반도체/AI/실적 관련 악재나 조정 흐름)을 대변하는 기사들을 앞단에 우선 선별해라.\n"
            "   - 반대로 증시가 상승세일 때는 AI 호재, 반도체 업황 활황, 하이퍼스케일러 인프라 투자 확대, 호실적(Earnings beat) 등 시장을 견인한 핵심 긍정 요인들을 주도적으로 분석해라.\n\n"
            f"--- [미국 현지 외신 뉴스 목록] ---\n{us_news_section}"
        )
        
        response = model.generate_content(prompt)
        summary = response.text.strip()
        
        if not summary:
            raise ValueError("Empty response from Gemini API")
            
        return summary
        
    except Exception as e:
        print(f"[경고] Gemini API 요약 실패: {e}. 폴백(뉴스 목록화) 방식으로 전송을 대체합니다.")
        return format_news_list(None, us_news_list)
