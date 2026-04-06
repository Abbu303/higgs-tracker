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
    # Looking back 4 hours because the "trap" pulls every 3 hours
    lookback_time = now_ist - timedelta(hours=4)

# Try this specific endpoint which is the most stable for Twitter AIO
url = "https://twitter-aio.p.rapidapi.com/user/tweets"
# If that fails, the alternative is:
# url = "https://twitter-aio.p.rapidapi.com/user/higgsfield/tweets"
    
    headers = {
        "X-RapidAPI-Key": str(RAPID_API_KEY).strip(), # .strip() removes any hidden spaces
        "X-RapidAPI-Host": "twitter-aio.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    
    querystring = {"username": "higgsfield", "count": "20"}

    try:
        print(f"🎣 Trap pulling up... (IST: {now_ist.strftime('%H:%M')})")
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            data = response.json()
            # Most APIs nest tweets in a list
            tweets = data.get('tweets', [])
            
            for tweet in tweets:
                text = tweet.get('text', '')
                tweet_id = tweet.get('id_str', tweet.get('id'))
                
                if any(k.lower() in text.lower() for k in KEYWORDS):
                    msg = f"🔥 NEW TWEET FOUND!\n\n{text}\n\nhttps://x.com/i/status/{tweet_id}"
                    send_telegram(msg)
                    print(f"✅ Match sent: {tweet_id}")
        else:
            print(f"❌ API Error: {response.status_code}")

    except Exception as e:
        print(f"❌ System Error: {e}")

if __name__ == "__main__":
    check_tweets()
