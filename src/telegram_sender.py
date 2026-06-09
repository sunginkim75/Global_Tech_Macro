import requests

def send_telegram_message(token, chat_id, text):
    """
    텔레그램 봇을 통해 마크다운 메시지를 전송합니다.
    글자 수 제한(4,096자)을 고려하여 필요 시 분할하여 전송합니다.
    """
    if not token or not chat_id:
        print("Telegram configuration missing. Token or Chat ID is null.")
        return False
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # 텔레그램 메시지 글자 수 제한: 4096자
    MAX_LENGTH = 4000
    
    # 마크다운 태그가 잘리는 것을 방지하기 위해 줄바꿈(\n) 단위로 안전하게 분할
    lines = text.split('\n')
    message_chunks = []
    current_chunk = []
    current_length = 0
    
    for line in lines:
        if len(line) > MAX_LENGTH:
            if current_chunk:
                message_chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_length = 0
            for i in range(0, len(line), MAX_LENGTH):
                message_chunks.append(line[i:i+MAX_LENGTH])
            continue
            
        if current_length + len(line) + 1 > MAX_LENGTH:
            message_chunks.append("\n".join(current_chunk))
            current_chunk = [line]
            current_length = len(line)
        else:
            current_chunk.append(line)
            current_length += len(line) + 1
            
    if current_chunk:
        message_chunks.append("\n".join(current_chunk))
        
    success = True
    for chunk in message_chunks:
        payload = {
            "chat_id": chat_id,
            "text": chunk,
            "parse_mode": "HTML",
            "disable_web_page_preview": False
        }
        
        try:
            response = requests.post(url, json=payload, timeout=15)
            result = response.json()
            
            if not result.get("ok"):
                # Markdown 파싱 에러 등으로 실패 시, parse_mode 없이 일반 텍스트로 재시도
                print(f"Failed to send with Markdown. Error: {result.get('description')}. Retrying in plain text...")
                payload["parse_mode"] = ""
                response = requests.post(url, json=payload, timeout=15)
                result = response.json()
                
            if not result.get("ok"):
                print(f"Telegram API Error: {result.get('description')}")
                success = False
            else:
                print("Telegram message sent successfully.")
        except Exception as e:
            print(f"Exception while sending telegram message: {e}")
            success = False
            
    return success
