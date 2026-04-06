import os
import requests
from ntscraper import Nitter

# 1. Grab Secrets (Ensure these are in your GitHub Repo Settings!)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# KEYWORDS + PRO TIP: Added 'the' and 'a' to test the connection immediately
KEYWORDS = ["credits", "dm", "DM", "hours", "creds", "retweet", "reply", "like", "follow", "the", "a"]

def send_telegram(msg):
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Secrets missing from GitHub Settings!")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=payload)

def check_tweets():
    # The handle from your URL: x.com/higgsfield
    target_user = "higgsfield" 
    
    print(f"Scraping @{target_user}...")
    scraper = Nitter(log_level=1)
    
    try:
        # number=5 checks the 5 most recent posts
        results = scraper.get_tweets(target_user, mode='user', number=5)
        
        if not results or not results.get('tweets'):
            print(f"No tweets found for {target_user}. Nitter instance might be rotated.")
            return

        for tweet in results['tweets']:
            text = tweet['text'].lower()
            
            # Logic: If any keyword (including 'the' or 'a') is found
            if any(k.lower() in text for k in KEYWORDS):
                link = tweet['link']
                message = f"🔥 TWEET DETECTED!\n\nContent: {tweet['text']}\n\nLink: {link}"
                send_telegram(message)
                print(f"✅ Match found for: {text[:30]}...")
                
    except Exception as e:
        print(f"Scraper Error: {e}")

if __name__ == "__main__":
    print("Workflow Started...")
    check_tweets()
