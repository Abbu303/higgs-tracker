import os
import requests
from datetime import datetime, timedelta
import pytz

# Secrets
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
RAPID_API_KEY = os.environ.get("RAPID_API_KEY")

# Keywords
KEYWORDS = ["credits", "dm", "DM", "hours", "creds", "the", "a"]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg}, timeout=10)
    except Exception as e:
        print(f"Telegram Error: {e}")

def check_tweets():
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    # Look back window
    lookback_time = now_ist - timedelta(hours=4)

    # --- TYPO FIXES HERE ---
    url = "https://twitter-aio.p.rapidapi.com/user/-1/tweets"
    querystring = {"username": "higgsfield", "count": "20"}
    
    headers = {
        "x-rapidapi-key": str(RAPID_API_KEY).strip(),
        "x-rapidapi-host": "twitter-aio.p.rapidapi.com"
    }

    try:
        print(f"🎣 Trap pulling up... (IST: {now_ist.strftime('%H:%M %p')})")
        response = requests.get(url, headers=headers, params=querystring, timeout=15)
        
        if response.status_code == 200:
            print("✅ 200 OK: Success!")
            data = response.json()
            
            # Twitter AIO returns a list under 'tweets'
            tweets = data.get('tweets', [])
            
            if not tweets:
                print("📭 No tweets found in the response.")
                return

            for tweet in tweets:
                text = tweet.get('text', tweet.get('full_text', ''))
                tweet_id = tweet.get('id_str', tweet.get('id'))
                
                # Check keywords
                if any(k.lower() in text.lower() for k in KEYWORDS):
                    display_date = now_ist.strftime('%d %b, %I:%M %p')
                    msg = f"🔥 NEW TWEET ({display_date} IST)!\n\n{text}\n\nLink: https://x.com/i/status/{tweet_id}"
                    send_telegram(msg)
                    print(f"✅ Alert sent for: {tweet_id}")
        else:
            print(f"❌ Error {response.status_code}")
            print(f"RAW MESSAGE: {response.text}") 
            # ADD THIS LINE TEMPORARILY:
            print(f"DEBUG: Using Host {headers['x-rapidapi-host']}") 
            
    except Exception as e:
        print(f"❌ System Error: {e}")

if __name__ == "__main__":
    check_tweets()
