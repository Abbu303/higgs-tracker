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
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def check_tweets():
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    lookback_time = now_ist - timedelta(hours=4)

    # 1. THE ENDPOINT (Twitter AIO specific)
    url = "https://twitter-aio.p.rapidapi.com/user/tweets"
    
    # 2. THE PARAMETERS
    querystring = {"username": "higgsfield", "count": "10"}
    
    # 3. THE HEADERS
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "twitter-aio.p.rapidapi.com"
    }

    try:
        print(f"Checking @higgsfield via API at {now_ist.strftime('%H:%M')} IST...")
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            return

        data = response.json()
        
        # Twitter AIO usually returns a list under 'tweets' or 'items'
        # We use .get() to avoid the 'list index' error from before
        tweets = data.get('tweets', [])
        
        if not tweets:
            print("📭 No tweets found in this response.")
            return

        for tweet in tweets:
            # Most APIs return 'text' or 'full_text'
            text = tweet.get('text', tweet.get('full_text', ''))
            tweet_id = tweet.get('id_str', tweet.get('id')) # Get ID for the link
            
            if any(k.lower() in text.lower() for k in KEYWORDS):
                display_date = now_ist.strftime('%d %b, %I:%M %p')
                msg = f"🔥 NEW TWEET ({display_date} IST)!\n\n{text}\n\nLink: https://x.com/i/status/{tweet_id}"
                send_telegram(msg)
                print(f"✅ Match found: {tweet_id}")

    except Exception as e:
        print(f"❌ System Error: {e}")

if __name__ == "__main__":
    check_tweets()
