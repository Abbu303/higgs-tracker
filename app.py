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
    # Since we check every 3 hours, we look back 4 hours to catch everything
    lookback_time = now_ist - timedelta(hours=4)

    # Use the exact URL from your screenshot
    url = "https://twitter-aio.p.rapidapi.com/user/-1/tweets"
    querystring = {"username": "higgsfield", "count": "10"}
    
   headers = {
    "x-rapidapi-key": RAPID_API_KEY,      # Use lowercase keys as seen in curl
    "x-rapidapi-host": "twitter-aio.p.rapidapi.com",
    "Content-Type": "application/json"   # Added from your screenshot
}

    try:
        print(f"🎣 Trap pulling up... (IST: {now_ist.strftime('%H:%M')})")
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            return

        data = response.json()
        tweets = data.get('tweets', [])
        
        if not tweets:
            print("📭 River is empty (No tweets found).")
            return

        for tweet in tweets:
            text = tweet.get('text', '')
            tweet_id = tweet.get('id_str', tweet.get('id'))
            
            if any(k.lower() in text.lower() for k in KEYWORDS):
                msg = f"🔥 NEW TWEET FOUND!\n\n{text}\n\nhttps://x.com/i/status/{tweet_id}"
                send_telegram(msg)
                print(f"✅ Fish caught! Alert sent for {tweet_id}")

    except Exception as e:
        print(f"❌ System Error: {e}")

if __name__ == "__main__":
    check_tweets()
