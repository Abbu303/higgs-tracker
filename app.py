import os
import requests

# Instead of pasting the token here, we pull it from GitHub Secrets
# 'BOT_TOKEN' and 'CHAT_ID' must match the names in your .yml file
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# This check helps you debug in the GitHub Actions log
if not BOT_TOKEN or not CHAT_ID:
    print("❌ Error: BOT_TOKEN or CHAT_ID is missing from Environment Variables!")
else:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    response = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": "✅ Bot is working!"
    })

    # This will print the result in your GitHub Action logs so you can see if it worked
    print(response.json())
