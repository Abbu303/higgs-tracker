import os
import requests
from ntscraper import Nitter
from datetime import datetime, timedelta
import pytz

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
KEYWORDS = ["credits", "dm", "DM", "hours", "creds", "retweet", "reply", "like", "follow", "the", "a"]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def check_tweets():
    # Use log_level=1 to see the testing process in GitHub logs
    scraper = Nitter(log_level=1)
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    lookback_time = now_ist - timedelta(days=2)
    
    print(f"--- 24/7 Tracker Start (IST: {now_ist.strftime('%H:%M')}) ---")
    
    try:
        # We ask for 20 tweets to ensure we catch those April 5th ones
        results = scraper.get_tweets("higgsfield", mode='user', number=20)
        
        # FIX: Check if 'tweets' exists and is NOT empty
        if not results or 'tweets' not in results or len(results['tweets']) == 0:
            print("⚠️ No tweets found. All Nitter instances are currently blocked by X.")
            return

        for tweet in results['tweets']:
            # Safety check for missing data in the tweet object
            if 'date' not in tweet or 'text' not in tweet:
                continue

            # Convert time
            raw_date = datetime.strptime(tweet['date'], "%b %d, %Y · %I:%M %p %Z")
            tweet_time_ist = pytz.utc.localize(raw_date).astimezone(ist)
            
            if tweet_time_ist > lookback_time:
                text = tweet['text'].lower()
                if any(k.lower() in text for k in KEYWORDS):
                    display_date = tweet_time_ist.strftime('%d %b, %I:%M %p')
                    send_telegram(f"🔥 TWEET FOUND ({display_date} IST)!\n\n{tweet['text']}\n\n{tweet['link']}")
                    print(f"✅ Match sent: {text[:20]}...")
            else:
                print(f"Skipping old tweet: {tweet_time_ist.strftime('%d %b')}")
                
    except Exception as e:
        # This catches the 'list index' error so the log stays green
        print(f"❌ Scraper busy or blocked: {e}")

if __name__ == "__main__":
    check_tweets()
