#!/usr/bin/env python3
"""
Telegram Bot Notifier for GitHub Actions
Sends notifications when GitHub Actions complete
"""

import requests
import json
import os
import sys
from datetime import datetime

# Your bot token (keep this secure!)
BOT_TOKEN = "8119497602:AAEGqaZ_HJjX_asIu43rZMqoDFnz_jmq3dY"

# Get chat ID from environment variable
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message, parse_mode="HTML"):
    """
    Send a message to Telegram bot
    """
    if not CHAT_ID:
        print("❌ TELEGRAM_CHAT_ID not set. Please set your chat ID.")
        return False
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": parse_mode
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("✅ Telegram message sent successfully!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send Telegram message: {e}")
        return False

def get_chat_id():
    """
    Helper function to get your chat ID
    Run this first to get your chat ID
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data["ok"] and data["result"]:
            print("📱 Recent messages from your bot:")
            for update in data["result"][-5:]:  # Show last 5 messages
                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    text = update["message"].get("text", "")
                    print(f"  Chat ID: {chat_id} | Message: {text}")
            print(f"\n💡 Use this Chat ID: {data['result'][-1]['message']['chat']['id']}")
        else:
            print("❌ No messages found. Send a message to your bot first!")
            print(f"   Bot URL: https://t.me/Dual_Mode_Mood_bot")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to get chat ID: {e}")

def send_github_action_notification(action_status, workflow_name, commit_message="", actor="", repo=""):
    """
    Send a formatted notification about GitHub Action completion
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Status emoji
    status_emoji = "✅" if action_status == "success" else "❌" if action_status == "failure" else "🔄"
    
    # Status text
    status_text = {
        "success": "SUCCESS",
        "failure": "FAILED", 
        "cancelled": "CANCELLED",
        "in_progress": "IN PROGRESS"
    }.get(action_status, action_status.upper())
    
    message = f"""
🚀 <b>GitHub Action Update</b>
{status_emoji} <b>Status:</b> {status_text}
📋 <b>Workflow:</b> {workflow_name}
⏰ <b>Time:</b> {timestamp}
👤 <b>Actor:</b> {actor}
📝 <b>Commit:</b> {commit_message}
🔗 <b>Repository:</b> {repo}

<i>MLOps Case Study - Mood Analysis App</i>
    """.strip()
    
    return send_telegram_message(message)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "get-chat-id":
        print("🔍 Getting your Telegram Chat ID...")
        print("Make sure you've sent at least one message to your bot first!")
        print(f"Bot URL: https://t.me/Dual_Mode_Mood_bot")
        get_chat_id()
    else:
        print("🤖 Telegram Bot Notifier")
        print("Usage:")
        print("  python telegram_notifier.py get-chat-id  # Get your chat ID")
        print("  python telegram_notifier.py              # Show this help")
