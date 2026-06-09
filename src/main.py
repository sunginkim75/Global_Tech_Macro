import os
import json
import sys

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.collector import get_market_data, get_combined_news, get_us_focused_news
from src.summarizer import format_market_data, summarize_news_with_gemini
from src.telegram_sender import send_telegram_message

# 윈도우 환경 표준 출력 인코딩 보정
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def load_config():
    """
    config.json 설정 파일을 불러옵니다.
    """
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def main():
    print("Starting Global Tech Macro Daily Report...")
    
    # 1. 설정값 로드
    config = load_config()
    indices = config.get("indices", {})
    stocks = config.get("stocks", {})
    news_keywords = config.get("news_keywords", ["semiconductor"])
    exclude_keywords = config.get("exclude_keywords", [])
    target_domains = config.get("target_domains", [])
    hankyung_rss_urls = config.get("hankyung_rss_urls", [])
    
    # 미국 영어 뉴스 설정 로드
    us_news_keywords = config.get("us_news_keywords", [])
    us_exclude_keywords = config.get("us_exclude_keywords", [])
    us_target_domains = config.get("us_target_domains", [])
    
    # 2. 환경 변수 확인 (GitHub Secrets 또는 로컬 환경 변수)
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    
    if not telegram_token or not telegram_chat_id:
        print("Error: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variable is missing.")
        sys.exit(1)
        
    # 3. 데이터 수집
    print("Collecting market data...")
    market_data = get_market_data(indices, stocks)
    
    print("Collecting semiconductor & macro news (Korean)... [국내 뉴스 제외로 수집 생략]")
    news_list = []
    
    print("Collecting US finance news (English)...")
    us_news_list = get_us_focused_news(us_news_keywords, us_target_domains, us_exclude_keywords, limit=15)
    
    # 4. 리포트 가공 및 포맷팅 (요약 복구)
    print("Formatting market report...")
    market_report_text = format_market_data(market_data)
    
    print("Summarizing news with Gemini (Hybrid Mode, KO/US Split)...")
    news_summary_text = summarize_news_with_gemini(news_list, us_news_list, gemini_api_key)
    
    # 5. 메시지 조합
    report_date = os.environ.get("RUN_DATE") or os.environ.get("CURRENT_DATE")
    if not report_date:
        import datetime
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=9) # KST
        report_date = now.strftime("%Y년 %m월 %d일")
        
    header = f"📅 <b>[Global Tech & Macro Daily 브리핑]</b>\n<b>{report_date} 아침 리포트</b>\n\n"
    divider = "\n\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    # news_summary_text가 자체 분류 섹션을 포함하므로 별도 뉴스 헤더 없이 합침
    final_message = f"{header}{market_report_text}{divider}{news_summary_text}"
    
    # 6. 텔레그램 발송
    print("Sending telegram message...")
    success = send_telegram_message(telegram_token, telegram_chat_id, final_message)
    
    if success:
        print("Daily Report sent successfully.")
    else:
        print("Failed to send Daily Report.")
        sys.exit(1)

if __name__ == "__main__":
    main()

