import os
import requests
from ntscraper import Nitter
from datetime import datetime, timedelta, timezone

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
KEYWORDS = ["credits", "dm", "DM", "hours", "creds", "retweet", "reply", "like", "follow"]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def check_tweets():
    scraper = Nitter(log_level=1)
    # The time 6 minutes ago (so we only get tweets posted since the last run)
    last_run_time = datetime.now(timezone.utc) - timedelta(minutes=6)
    
    print(f"Checking for new tweets since: {last_run_time}")
    
    try:
        results = scraper.get_tweets("higgsfield", mode='user', number=5)
        
        for tweet in results['tweets']:
            # Convert tweet time string to a Python time object
            tweet_time = datetime.strptime(tweet['date'], "%b %d, %Y · %I:%M %p %Z").replace(tzinfo=timezone.utc)
            
            # ONLY send if the tweet is NEWER than our last run
            if tweet_time > last_run_time:
                text = tweet['text'].lower()
                if any(k.lower() in text for k in KEYWORDS):
                    send_telegram(f"🔥 NEW TWEET FOUND!\n\n{tweet['text']}\n\n{tweet['link']}")
            else:
                print("Tweet is old, skipping...")
                
    except Exception as e:
        print(f"Scraper error: {e}")

if __name__ == "__main__":
    check_tweets()
