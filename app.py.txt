import requests

BOT_TOKEN = "8656149277:AAHxOg-F53EctZcDQ-l4pmX0AzEQ6GHWXyUN"
CHAT_ID = "978070354"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(url, data={
    "chat_id": CHAT_ID,
    "text": "✅ Bot is working!"
})
