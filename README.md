# Veylora

![Veylora Logo](https://i.imgur.com/KLc53YE.png)

**Veylora** brings pure good vibes — hugs, pats, boops, chaos, and whatever else you come up with.  
Delightful. Perfectly unnecessary. 100% worth it.

---
## ⚠️ Feedback

Hi, a short mesage from the Veylora Bot Creator. It would really help us if you fill out our short Survey to make Veylora Bot better! A link to a google form here: [Form](https://forms.gle/mvcwL8iQwKsym57v5)

---

### Please note that the Veylora Telegram Bot and the Veylora Discord Bot are two different Projects! 

More about the Telegram version of the Bot here: [https://github.com/Infiloo/Veylora/tree/telegram](https://github.com/Infiloo/Veylora/tree/telegram)

---

## ✨ Features

- Hugs, pats, headpats, boops, highfives, cheers and waves  
- Chaotic but friendly interactions to keep chat active  
- Cooldown system (default 5 s per user per command)  
- Per‑server personalization (custom emojis via `/vconfig`)  
- Highly configurable responses and cooldowns  
- Uses modern Discord features (discord.py v2, slash commands)

---

## 🚀 Getting Started

### User Install
Invite Veylora to your Discord user profile for personal commands:  
[**User Install**](https://discord.com/oauth2/authorize?client_id=1475540281418973306&integration_type=1&scope=applications.commands)

### Server Install
Add Veylora to your Discord server:  
[**Server Install**](https://discord.com/oauth2/authorize?client_id=1475540281418973306&integration_type=0&scope=bot%20applications.commands&permissions=8)

---

## 🧩 Self‑Hosting

### Get the Bot Code here: [Github](https://github.com/Infiloo/Veylora)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Create your bot
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)  
2. Create a new **Application → Bot**  
3. Under *Privileged Gateway Intents*, enable **Message Content Intent**  (After a Big change this is not Necessary anymore)
4. Copy your **Bot Token**

### 3. Configure the bot
Edit `bot.py` and replace:
```python
TOKEN = "YOUR_TOKEN_HERE"
```
Or set it as an environment variable:
```bash
export DISCORD_TOKEN=your_token_here
```

Replace `YOUR_CLIENT_ID` in the `/add` command with your Application ID.

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

## 🚀 Hosting & Support

**Veylora** is proudly hosted for free on **Wispbyte**! 

To keep the bot running 24/7 without costs, I rely on reliable hosting services. If you'd like to support the project at no extra cost to you, please consider signing up for Wispbyte using my referral link below. 

### How to support me:
By using this link, you help me maintain the bot and potentially unlock more resources for future updates:

👉 **[Support Veylora on Wispbyte](https://wispbyte.com/a?ref=infiloo)**

---

## 📚 Commands

| Command | Description |
|----------|-------------|
| `/hug` | Hug a user 💕 |
| `/pat` | Pat a user 🖐️ |
| `/headpat` | Headpat a user 🥰 |
| `/boop` | Boop a user 👉 |
| `/highfive` | High‑five a user ✋ |
| `/cheer` | Cheer a user up 🎉 |
| `/wave` | Wave to a user 👋 |
| `/patpat` | Generates a Headpat Gif with the entered User PFP 🎥 |
| `/send` | Easilly send large files for free over Discord 📁 |
| `/add` | Add Veylora to your Profile or Server ➕ |

### Admin Commands *(Manage Server permission required)*

| Command | Description |
|----------|-------------|
| `/vconfig view` | View the server’s current configuration |
| `/vconfig set_emoji` | Override custom emoji for a command |
| `/vconfig reset` | Reset all custom configuration |

---

## 🔧 Per‑Server Configuration

Server administrators can fully customize Veylora’s emojis and responses with `/vconfig`.  
Configuration is stored in `data/<guild_id>.json`.

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
- Thanks to everyone enjoying Veylora’s wholesome chaos 💕
