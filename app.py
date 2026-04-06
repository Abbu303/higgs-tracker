import os
import requests

# Grabbing the hidden secrets from GitHub
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_message(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("❌ Error: Missing BOT_TOKEN or CHAT_ID in Secrets!")
        return
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    
    response = requests.post(url, data=payload)
    print(f"Response from Telegram: {response.json()}")

# This runs every time the GitHub Action starts (every 5 mins)
if __name__ == "__main__":
    send_message("🤖 Keyword Tracker is now active and checking for tweets...")
