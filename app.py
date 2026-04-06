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
    url = "https://twitter-aio.p.rapidapi.com/user/-1/tweets"
    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": "twitter-aio.p.rapidapi.com"
    }
    querystring = {"username": "higgsfield", "count": "20"}

    try:
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.status_code == 200:
            print("✅ 200 OK: Success!")
            # ... (rest of your tweet logic)
        else:
            # THIS IS THE KEY PART:
            print(f"❌ Error {response.status_code}")
            print(f"RAW MESSAGE: {response.text}") 
            # Check your GitHub logs for this 'RAW MESSAGE'
            
    except Exception as e:
        print(f"❌ System Error: {e}")
if __name__ == "__main__":
    check_tweets()
