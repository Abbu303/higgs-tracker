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
        # Attempt 1: Check the Profile directly
        print("Attempting to scrape profile @higgsfield...")
        results = scraper.get_tweets("higgsfield", mode='user', number=20)
        
        # Attempt 2: If Profile is blocked/empty, try Search mode
        if not results or not results.get('tweets'):
            print("Profile blocked or empty. Trying Search Fallback...")
            # 'mode=term' searches for tweets from the user
            results = scraper.get_tweets("from:higgsfield", mode='term', number=20)

        # Now, if we STILL have nothing, exit quietly
        if not results or not results.get('tweets'):
            print("⚠️ Both Profile and Search were blocked. Skipping this 5-min run.")
            return

        # If we found tweets, start the loop
        for tweet in results['tweets']:
            # ... (the rest of your code for date checking and keywords)

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
