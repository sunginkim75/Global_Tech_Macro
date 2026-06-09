import yfinance as yf
import feedparser
import urllib.parse
import datetime
import time
from datetime import datetime, timezone, timedelta

def is_recent(published_parsed, max_days=3):
    """
    기사가 최근 max_days 이내에 발행되었는지 검증합니다.
    """
    if not published_parsed:
        return True # 날짜 파싱이 안 되는 경우는 예외적으로 허용
    try:
        # struct_time을 datetime 객체(UTC 기준)로 변환
        dt = datetime(*published_parsed[:6], tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        return now - dt < timedelta(days=max_days)
    except Exception as e:
        print(f"Error checking date recency: {e}")
        return True

def get_market_data(indices, stocks):
    """
    주요 지수 및 개별 주가 데이터를 수집합니다.
    """
    data = {
        "indices": {},
        "stocks": {}
    }
    
    # 1. 지수 데이터 수집
    for name, ticker_sym in indices.items():
        try:
            ticker = yf.Ticker(ticker_sym)
            hist = ticker.history(period="5d")
            if len(hist) >= 2:
                prev_close = hist['Close'].iloc[-2]
                curr_close = hist['Close'].iloc[-1]
                change = curr_close - prev_close
                pct_change = (change / prev_close) * 100
                data["indices"][name] = {
                    "ticker": ticker_sym,
                    "close": curr_close,
                    "change": change,
                    "pct_change": pct_change
                }
            else:
                data["indices"][name] = {"error": "Insufficient data"}
        except Exception as e:
            data["indices"][name] = {"error": str(e)}
            
    # 2. 개별 주가 데이터 수집
    for name, ticker_sym in stocks.items():
        try:
            ticker = yf.Ticker(ticker_sym)
            hist = ticker.history(period="5d")
            if len(hist) >= 2:
                prev_close = hist['Close'].iloc[-2]
                curr_close = hist['Close'].iloc[-1]
                change = curr_close - prev_close
                pct_change = (change / prev_close) * 100
                data["stocks"][name] = {
                    "ticker": ticker_sym,
                    "close": curr_close,
                    "change": change,
                    "pct_change": pct_change
                }
            else:
                data["stocks"][name] = {"error": "Insufficient data"}
        except Exception as e:
            data["stocks"][name] = {"error": str(e)}
            
    return data

def get_semiconductor_news(keywords, exclude_keywords=None, limit=10):
    """
    구글 뉴스 한국어 RSS를 사용하여 최신 뉴스 목록을 가져옵니다.
    """
    query = " OR ".join([f'"{kw}"' for kw in keywords])
    query = f"({query}) when:1d"
    
    encoded_query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    
    news_list = []
    try:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            if len(news_list) >= limit:
                break
                
            title = entry.get("title", "")
            source = entry.get("source", {}).get("title", "뉴스")
            
            # 1. 최근 3일 이내 기사인지 검증
            if not is_recent(entry.get("published_parsed"), max_days=3):
                continue
                
            # 2. 제외 키워드 필터링
            if exclude_keywords:
                if any(ek.lower() in title.lower() for ek in exclude_keywords):
                    continue
                    
            if " - " in title:
                title = " - ".join(title.split(" - ")[:-1])
                
            pub_date = entry.get("published", "")
            news_list.append({
                "title": title,
                "link": entry.get("link", ""),
                "published": pub_date,
                "source": source
            })
    except Exception as e:
        print(f"Error fetching news: {e}")
        
    return news_list

def get_domain_focused_news(keywords, target_domains, exclude_keywords=None, limit=15):
    """
    지정된 전문 금융 도메인들(target_domains) 내에서 키워드와 매치되는 한글 기사만 핀포인트 수집합니다.
    """
    if not target_domains:
        return []
        
    query_keywords = " OR ".join([f'"{kw}"' for kw in keywords])
    query_domains = " OR ".join([f"site:{domain}" for domain in target_domains])
    # when:1d를 키워드 부분에 바로 붙여 쿼리를 더 정교화
    query = f"when:1d ({query_keywords}) ({query_domains})"
    
    encoded_query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ko&gl=KR&ceid=KR:ko"
    
    news_list = []
    try:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            if len(news_list) >= limit:
                break
                
            title = entry.get("title", "")
            link = entry.get("link", "")
            source = entry.get("source", {}).get("title", "금융뉴스")
            
            # 1. 최근 3일 이내 기사인지 검증
            if not is_recent(entry.get("published_parsed"), max_days=3):
                continue
                
            if "investing.com" in link.lower() or "인베스팅" in source:
                source = "인베스팅닷컴"
            elif "tradingview.com" in link.lower() or "트레이딩뷰" in source:
                source = "TradingView"
            elif "tradingkey.com" in link.lower() or "트레이딩키" in source:
                source = "TradingKey"
            elif "hankyung.com" in link.lower() or "한국경제" in source:
                source = "한국경제"
                
            # 2. 제외 키워드 필터링
            if exclude_keywords:
                if any(ek.lower() in title.lower() for ek in exclude_keywords):
                    continue
                    
            if " - " in title:
                title = " - ".join(title.split(" - ")[:-1])
                
            pub_date = entry.get("published", "")
            news_list.append({
                "title": title,
                "link": link,
                "published": pub_date,
                "source": source
            })
    except Exception as e:
        print(f"Error fetching domain focused news: {e}")
        
    return news_list

def get_hankyung_rss_news(rss_urls, keywords, exclude_keywords=None, limit=10):
    """
    한국경제 공식 RSS 피드(금융, 국제)에서 주요 키워드가 포함된 기사를 추출합니다.
    """
    news_list = []
    if not rss_urls:
        return news_list
        
    for url in rss_urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                if len(news_list) >= limit * 2:
                    break
                    
                title = entry.get("title", "")
                
                # 1. 최근 3일 이내 기사인지 검증
                if not is_recent(entry.get("published_parsed"), max_days=3):
                    continue
                    
                # 2. 제외 키워드 필터링
                if exclude_keywords:
                    if any(ek.lower() in title.lower() for ek in exclude_keywords):
                        continue
                        
                matched = any(kw.lower() in title.lower() for kw in keywords)
                
                if matched:
                    pub_date = entry.get("published", "")
                    news_list.append({
                        "title": title,
                        "link": entry.get("link", ""),
                        "published": pub_date,
                        "source": "한국경제"
                    })
        except Exception as e:
            print(f"Error parsing Hankyung RSS ({url}): {e}")
            
    return news_list[:limit]

def get_combined_news(keywords, exclude_keywords=None, target_domains=None, hankyung_rss_urls=None, limit=10):
    """
    금융 전문 도메인 조준 구글 뉴스, 보조 한경 공식 RSS, 일반 반도체 구글 뉴스 등에서 수집한 뉴스를 병합하고
    제목 기준 중복을 제거한 후 최종 뉴스 리스트를 반환합니다.
    """
    combined = []
    
    # 1. 4대 전문 금융 플랫폼 조준 구글 뉴스 수집
    if target_domains:
        combined.extend(get_domain_focused_news(keywords, target_domains, exclude_keywords, limit=15))
        
    # 2. 보조 한경 공식 RSS 수집
    if hankyung_rss_urls:
        combined.extend(get_hankyung_rss_news(hankyung_rss_urls, keywords, exclude_keywords, limit=5))
        
    # 3. 일반 구글 뉴스 수집 (보완용)
    combined.extend(get_semiconductor_news(keywords, exclude_keywords, limit=10))
    
    seen_titles = set()
    seen_links = set()
    unique_news = []
    
    for item in combined:
        title_stripped = "".join(item["title"].split()).lower()
        link = item["link"].strip()
        
        if title_stripped not in seen_titles and link not in seen_links:
            seen_titles.add(title_stripped)
            seen_links.add(link)
            unique_news.append(item)
            
    # 우선순위 정렬: 인베스팅닷컴, TradingView, TradingKey, 한국경제 등 전문 금융 사이트 뉴스 우선 배치
    pref_sources = ["인베스팅닷컴", "TradingView", "TradingKey", "한국경제"]
    pref_news = [n for n in unique_news if n["source"] in pref_sources]
    other_news = [n for n in unique_news if n not in pref_news]
    
    final_list = pref_news + other_news
    return final_list[:limit]

def get_us_focused_news(keywords, target_domains, exclude_keywords=None, limit=10):
    """
    지정된 미국의 주요 금융/시황 사이트(target_domains) 내에서 영문 키워드와 매치되는 기사를 수집합니다.
    """
    if not target_domains:
        return []
        
    query_keywords = " OR ".join([f'"{kw}"' for kw in keywords])
    query_domains = " OR ".join([f"site:{domain}" for domain in target_domains])
    # when:1d (최근 24시간 이내 기사)
    query = f"when:1d ({query_keywords}) ({query_domains})"
    
    encoded_query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en&gl=US&ceid=US:en"
    
    news_list = []
    try:
        feed = feedparser.parse(rss_url)
        for entry in feed.entries:
            if len(news_list) >= limit:
                break
                
            title = entry.get("title", "")
            link = entry.get("link", "")
            source = entry.get("source", {}).get("title", "US Finance")
            
            # 1. 최근 3일 이내 기사인지 검증
            if not is_recent(entry.get("published_parsed"), max_days=3):
                continue
                
            # 소스 이름 정제
            source_lower = source.lower()
            if "yahoo" in source_lower:
                source = "Yahoo Finance"
            elif "cnbc" in source_lower:
                source = "CNBC"
            elif "reuters" in source_lower:
                source = "Reuters"
            elif "marketwatch" in source_lower:
                source = "MarketWatch"
            elif "bloomberg" in source_lower:
                source = "Bloomberg"
                
            # 2. 제외 키워드 필터링
            if exclude_keywords:
                if any(ek.lower() in title.lower() for ek in exclude_keywords):
                    continue
                    
            if " - " in title:
                title = " - ".join(title.split(" - ")[:-1])
                
            pub_date = entry.get("published", "")
            news_list.append({
                "title": title,
                "link": link,
                "published": pub_date,
                "source": source
            })
    except Exception as e:
        print(f"Error fetching US news: {e}")
        
    return news_list





