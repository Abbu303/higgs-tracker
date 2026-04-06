import os
import requests
from ntscraper import Nitter
from datetime import datetime, timedelta
import pytz  # New import for timezones

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
KEYWORDS = ["credits", "dm", "DM", "hours", "creds", "retweet", "reply", "like", "follow", "the", "a"]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def check_tweets():
    scraper = Nitter(log_level=1)
    ist = pytz.timezone('Asia/Kolkata')
    now_ist = datetime.now(ist)
    lookback_time = now_ist - timedelta(days=2)
    
    print(f"Current Time (IST): {now_ist.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # We add 'instance' manually to try a more reliable one
        results = scraper.get_tweets("higgsfield", mode='user', number=10)
        
        # --- THE FIX IS HERE ---
        # If results is empty or None, don't try to loop through it
        if not results or not results.get('tweets'):
            print("⚠️ No tweets found. The Nitter instances might be blocked right now.")
            return 
        # -----------------------

        for tweet in results['tweets']:
            # Extra safety check for the date field
            if 'date' not in tweet:
                continue

            raw_date = datetime.strptime(tweet['date'], "%b %d, %Y · %I:%M %p %Z")
            tweet_time_ist = pytz.utc.localize(raw_date).astimezone(ist)
            
            if tweet_time_ist > lookback_time:
                text = tweet['text'].lower()
                if any(k.lower() in text for k in KEYWORDS):
                    display_date = tweet_time_ist.strftime('%d %b, %I:%M %p')
                    send_telegram(f"🔥 TWEET FOUND ({display_date} IST)!\n\n{tweet['text']}\n\n{tweet['link']}")
                    print(f"✅ Match found: {text[:30]}...")
                
    except Exception as e:
        # This prevents the "list index out of range" from stopping the whole Action
        print(f"Scraper Error: {e}")
    
    # 1. Set up IST Timezone
    ist = pytz.timezone('Asia/Kolkata')
    
    # 2. Get current time in IST
    now_ist = datetime.now(ist)
    
    # 3. Look back 2 days (to catch those April 5th tweets!)
    lookback_time = now_ist - timedelta(days=2)
    
    print(f"Current Time (IST): {now_ist.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Checking for tweets since (IST): {lookback_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        results = scraper.get_tweets("higgsfield", mode='user', number=10)
        
        if not results or not results.get('tweets'):
            print("No tweets found.")
            return

        for tweet in results['tweets']:
            # 4. Convert the tweet's time string to an IST object
            # Nitter usually returns time in UTC, so we localize then convert
            raw_date = datetime.strptime(tweet['date'], "%b %d, %Y · %I:%M %p %Z")
            tweet_time_utc = pytz.utc.localize(raw_date)
            tweet_time_ist = tweet_time_utc.astimezone(ist)
            
            if tweet_time_ist > lookback_time:
                text = tweet['text'].lower()
                if any(k.lower() in text for k in KEYWORDS):
                    # We format the date nicely for your Telegram message
                    display_date = tweet_time_ist.strftime('%d %b, %I:%M %p')
                    send_telegram(f"🔥 TWEET FOUND ({display_date} IST)!\n\n{tweet['text']}\n\n{tweet['link']}")
            else:
                print(f"Skipping old tweet from {tweet_time_ist}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_tweets()
