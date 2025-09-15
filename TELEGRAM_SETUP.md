# 🤖 Telegram Bot Setup for GitHub Actions

This guide will help you set up Telegram notifications for your GitHub Actions workflow.

## 📱 Step 1: Get Your Chat ID

1. **Start a conversation with your bot:**
   - Go to: https://t.me/Dual_Mode_Mood_bot
   - Click "START" or send any message like "Hello"

2. **Get your Chat ID:**
   ```bash
   # In your Codespaces terminal
   python3 telegram_notifier.py get-chat-id
   ```

3. **Copy the Chat ID** (it will be a number like `123456789`)

## 🔐 Step 2: Add Secrets to GitHub Repository

1. **Go to your GitHub repository**
2. **Click "Settings" → "Secrets and variables" → "Actions"**
3. **Click "New repository secret"**
4. **Add these secrets:**

   | Secret Name | Value | Description |
   |-------------|-------|-------------|
   | `TELEGRAM_CHAT_ID` | `123456789` | Your chat ID from step 1 |
   | `HF_USERNAME` | `your_hf_username` | Your Hugging Face username |
   | `HF_TOKEN` | `your_hf_token` | Your Hugging Face token |
   | `HF_SPACE_NAME` | `your_space_name` | Your Hugging Face Space name |

## 🧪 Step 3: Test the Integration

1. **Test locally first:**
   ```bash
   # Set your chat ID
   export TELEGRAM_CHAT_ID="your_chat_id_here"
   
   # Test sending a message
   python3 telegram_notifier.py
   ```

2. **Test with GitHub Actions:**
   - Make a small change to any file
   - Commit and push to main branch
   - Check your Telegram for notifications!

## 📋 What You'll Receive

When GitHub Actions run, you'll get messages like:

**✅ Success Notification:**
```
🚀 GitHub Action Update
✅ Status: SUCCESS
📋 Workflow: Test & Sync to Hugging Face
⏰ Time: 2024-01-15 14:30:25 UTC
👤 Actor: your-username
📝 Commit: Fixed API output formatting
🔗 Repository: your-username/hugging_face_mood_app

MLOps Case Study - Mood Analysis App
```

**❌ Failure Notification:**
```
🚀 GitHub Action Update
❌ Status: FAILED
📋 Workflow: Test & Sync to Hugging Face
⏰ Time: 2024-01-15 14:30:25 UTC
👤 Actor: your-username
📝 Commit: Added new feature
🔗 Repository: your-username/hugging_face_mood_app

MLOps Case Study - Mood Analysis App
```

## 🔧 Troubleshooting

### Bot not responding?
- Make sure you've sent a message to the bot first
- Check that your Chat ID is correct
- Verify the bot token is correct

### Notifications not working?
- Check that `TELEGRAM_CHAT_ID` secret is set in GitHub
- Look at the GitHub Actions logs for error messages
- Test the bot locally first

### Bot token security?
- The bot token is visible in the code (for simplicity)
- In production, you should store it as a GitHub secret
- The token only allows sending messages to your specific chat

## 🎯 Extra Credit Features

This implementation includes several enhancements beyond the basic requirement:

1. **Rich formatting** with HTML and emojis
2. **Detailed information** including commit message, actor, timestamp
3. **Both success and failure notifications**
4. **Easy setup script** for getting chat ID
5. **Error handling** and fallback messages
6. **Professional formatting** with project branding

## 🚀 Ready to Go!

Once you've completed these steps, every time you push to the main branch, you'll get a Telegram notification about your GitHub Actions status!

This gives you real-time feedback on your MLOps pipeline and demonstrates advanced automation skills for your case study.
