# Veylora — Telegram
![Veylora Logo](https://i.imgur.com/KLc53YE.png)

**Veylora** brings pure good vibes — hugs, pats, boops, chaos, and whatever else you come up with.  
Delightful. Perfectly unnecessary. 100% worth it.

---

⚠️ Join our Telegram Group for Updates on the Telegram Bot! [https://t.me/veylorabot](https://t.me/veylorabot)

---

## ⚠️ Feedback
Hi, a short message from the Veylora Bot Creator. It would really help us if you fill out our short Survey to make Veylora Bot better! A link to a Google Form here: [Form](https://forms.gle/mvcwL8iQwKsym57v5)

---

## ✨ Features
- Hugs, pats, headpats, boops, highfives, cheers and waves
- Chaotic but friendly interactions to keep chat active
- Cooldown system (default 5 s per user per command)
- Per-chat personalization (custom emojis via `/vconfig`)
- Animated headpat GIFs using user profile pictures
- File sharing via Filebin with session management

---

## 📚 Commands

| Command | Description |
|---------|-------------|
| `/hug` | Hug a user 💕 |
| `/pat` | Pat a user 🖐️ |
| `/headpat` | Headpat a user 🥰 |
| `/boop` | Boop a user 👉 |
| `/highfive` | High-five a user ✋ |
| `/cheer` | Cheer a user on 🎉 |
| `/wave` | Wave to a user 👋 |
| `/patpat` | Animated headpat GIF with target's profile picture 🎥 |
| `/send` | Share large files for free via Filebin 📁 |

### Admin Commands *(Groups only — Admin permission required)*

| Command | Description |
|---------|-------------|
| `/vconfig view` | View the chat's current configuration |
| `/vconfig set_emoji <action> <emoji>` | Override emoji for a command |
| `/vconfig reset` | Reset all custom configuration |

> **💡 How to use interaction commands:**  
> **Reply** to someone's message, then type the command.  
> Example: reply to a friend's message → type `/hug` → Veylora sends the hug!

---

## 🧩 Self-Hosting

There are two ways to self-host Veylora on Telegram. Pick whichever suits you best.

---

### Option A — TelebotHost (Easiest, free, no server needed)

TelebotHost runs your bot entirely in the cloud for free using their own scripting language (**TBL**). No Python, no installs, no VPS required.

> ⚠️ **Limitations vs. Python version:** `/patpat` GIF generation and `/vconfig` per-chat config are not available on the TBL free plan due to no file system access.

#### 1. Create your Telegram bot
1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the prompts
3. Copy your **Bot Token**

#### 2. Set up on TelebotHost
1. Go to [console.telebothost.com](https://console.telebothost.com)
2. Click **"Create New Bot"**
3. Enter your bot name and paste your token
4. Click **"Create"**

#### 3. Add each command
For every command in `tbl-commands.md`, do the following:

1. In your bot dashboard, click **"Create Command"**
2. Set the **Command Name** exactly as shown (e.g. `/hug`)
3. Paste the corresponding code block into the **Code** field
4. Click **Save**

Repeat for all 11 commands (`/start`, `/help`, `/hug`, `/pat`, `/headpat`, `/boop`, `/highfive`, `/cheer`, `/wave`, `/send`, and `!`). The full code for each is in `tbl-commands.md`.

#### 4. Done! ✅
Your bot is live 24/7 for free. Test it by sending `/start` to your bot in Telegram.

---

### Option B — Python / Self-Hosted Server

Full-featured version with all commands including `/patpat` GIF generation and `/vconfig`.

#### 1. Create your Telegram bot
1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the prompts
3. Copy your **Bot Token**

#### 2. Install dependencies
```bash
pip install -r requirements.txt
```

#### 3. Configure the bot
Edit `telegram-bot.py` and replace:
```python
TOKEN = "YOUR_BOT_TOKEN_HERE"
```
Or set it as an environment variable:
```bash
export TELEGRAM_TOKEN=your_token_here
```

#### 4. Run the bot
```bash
python telegram-bot.py
```

#### 5. Hosting 24/7 (free options)

**Oracle Cloud — Recommended (truly free forever)**
1. Sign up at [cloud.oracle.com](https://cloud.oracle.com) → use the **Always Free** tier
2. Create a **VM.Standard.A1** instance (4 CPU, 24 GB RAM — free forever)
3. SSH into your VM and run:
```bash
sudo apt update && sudo apt install python3-pip screen -y
pip3 install -r requirements.txt
screen -S veylora
export TELEGRAM_TOKEN=your_token_here
python3 telegram-bot.py
# Press Ctrl+A then D to detach — bot keeps running
```

**Google Cloud Free Tier**
1. Sign up at [cloud.google.com](https://cloud.google.com)
2. Create a free **e2-micro** VM in `us-east1`
3. SSH in and follow the same steps as Oracle above

**Railway ($5 free credits/month)**
1. Sign up at [railway.app](https://railway.app)
2. Create a new project → deploy from GitHub
3. Add environment variable: `TELEGRAM_TOKEN=your_token`
4. Set start command: `python telegram-bot.py`

---

## 📊 Version Comparison

| Feature | TelebotHost (TBL) | Python (Self-hosted) |
|---------|:-----------------:|:--------------------:|
| All interaction commands | ✅ | ✅ |
| Cooldown system | ✅ | ✅ |
| File sharing (`/send`) | ✅ | ✅ |
| `/patpat` GIF generation | ❌ | ✅ |
| Per-chat config (`/vconfig`) | ❌ | ✅ |
| Hosting cost | 🆓 Free | 🆓 Free (with VPS) |
| Setup difficulty | Easy | Medium |

---

## 🔧 Per-Chat Configuration *(Python version only)*

Chat administrators can customize Veylora's emojis with `/vconfig`.  
Configuration is stored in `data/<chat_id>.json`.

Example configuration:
```json
{
  "hug": {
    "emoji": "🫂",
    "messages": [
      "{author} absolutely crushes {target} with a hug 🫂"
    ]
  }
}
```

---

## 💌 Credits
- **Creator:** Infiloo
- **Mascot & Logo:** Infiloo
- Thanks to everyone enjoying Veylora's wholesome chaos 💕
