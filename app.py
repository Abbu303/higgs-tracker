import os
import requests
from ntscraper import Nitter
from datetime import datetime, timedelta
import pytz

# 1. SECRETS (Do NOT paste your real token here!)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# 2. KEYWORDS (Including 'the' and 'a' for testing)
KEYWORDS = ["credits", "dm", "DM", "hours", "creds", "retweet", "reply", "like", "follow", "the", "a"]

def send_telegram(msg):
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Secrets missing in GitHub Settings!")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

def check_tweets():
    scraper = Nitter(log_level=1)
    target_user = "higgsfield"
    
    # Set up IST Timezone
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    
    # Look back 2 days to catch the April 5th tweets
    lookback_time = now_ist - timedelta(days=2)
    
    print(f"Current Time (IST): {now_ist.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Checking @{target_user} since: {lookback_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Try to get the latest 10 tweets
        results = scraper.get_tweets(target_user, mode='user', number=10)
        
        # SAFETY CHECK: If the scraper gets blocked or returns nothing
        if not results or not results.get('tweets'):
            print("⚠️ No tweets found. Nitter instances might be blocked. Will try again in 5 mins.")
            return

        for tweet in results['tweets']:
            if 'date' not in tweet:
                continue

            # Convert tweet time to IST
            # Nitter: "Apr 05, 2026 · 10:00 AM UTC"
            raw_date = datetime.strptime(tweet['date'], "%b %d, %Y · %I:%M %p %Z")
            tweet_time_ist = pytz.utc.localize(raw_date).astimezone(ist)
            
            if tweet_time_ist > lookback_time:
                text = tweet['text'].lower()
                if any(k.lower() in text for k in KEYWORDS):
                    display_date = tweet_time_ist.strftime('%d %b, %I:%M %p')
                    message = f"🔥 TWEET FOUND ({display_date} IST)!\n\n{tweet['text']}\n\n{tweet['link']}"
                    send_telegram(message)
                    print(f"✅ Match sent: {text[:30]}...")
            else:
                print(f"Skipping old tweet from {tweet_time_ist}")
                
    except Exception as e:
        print(f"❌ Scraper encountered an error: {e}")

if __name__ == "__main__":
    check_tweets()
