# Veylora 💕

> Veylora brings pure good vibes — hugs, pats, boops, chaos, and whatever else you come up with 💫  
> Delightful. Perfectly unnecessary. 100% worth it.

---

## ✨ Features
- Hugs, pats, headpats, boops, highfives, cheers & waves
- Chaotic but friendly interactions to keep chat alive
- Cooldown system (default 5s per user per command)
- Per-server personalization (custom emojis via `/vconfig`)
- Slash commands and modern Discord API usage (discord.py v2)

---

## 🚀 Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Create your bot
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new Application → Bot
3. Enable **Message Content Intent** (under Bot → Privileged Gateway Intents)
4. Copy your **Bot Token**

### 3. Configure the bot
Open `bot.py` and replace:
```python
TOKEN = "YOUR_TOKEN_HERE"
```
with your actual token. Or set it as an environment variable:
```bash
export DISCORD_TOKEN=your_token_here
```

Also replace `YOUR_CLIENT_ID` in the `/add` command with your bot's application ID.

### 4. Invite your bot
Use this URL (replace `YOUR_CLIENT_ID`):
```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands&permissions=277025770560
```

### 5. Run the bot
```bash
python bot.py
```

---

## 📚 Commands

| Command      | Description                        |
|--------------|------------------------------------|
| `/hug`       | Hug a user 💕                      |
| `/pat`       | Pat a user 🖐️                      |
| `/headpat`   | Headpat a user 🥰                  |
| `/boop`      | Boop a user 👉                     |
| `/highfive`  | Highfive a user ✋                  |
| `/cheer`     | Cheer a user up 🎉                 |
| `/wave`      | Wave to a user 👋                  |
| `/add`       | Add Veylora to your Profile/Server |

### Admin Commands (Manage Server permission required)

| Command                        | Description                          |
|--------------------------------|--------------------------------------|
| `/vconfig view`                | View server's current config         |
| `/vconfig set_emoji`           | Override emoji for a command         |
| `/vconfig reset`               | Reset all custom config              |

---

## 🔧 Per-Server Config

Server admins can customize Veylora using `/vconfig`. Config is stored in `data/<guild_id>.json`.

Example config file:
```json
{
  "hug": {
    "emoji": "🫂",
    "messages": [
      "{author} absolutely CRUSHES {target} with a hug 🫂"
    ]
  }
}
```

---

## 📜 License
Private Project – Not open source.

## 💌 Credits
- **Creator:** Infiloo
- **Mascot & Logo:** Created by Infiloo
- Thanks to everyone enjoying Veylora's wholesome chaos! 💕
