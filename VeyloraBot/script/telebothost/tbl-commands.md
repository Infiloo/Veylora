# Veylora Bot — TBL Commands for TelebotHost
Create each block below as a **separate command** in your TelebotHost dashboard.

---

## HOW TO USE
In Telegram, all interaction commands work by **replying to someone's message**.
Example: Reply to a friend's message → type `/hug` → bot sends the hug message.

---

## COMMAND 1: `/start`

```
Bot.sendMessage("✨ *Hey! I'm Veylora* — spreading good vibes one boop at a time 💕\n\nUse /help to see all my commands!")
```

---

## COMMAND 2: `/help`

```
Bot.sendMessage("💕 *Veylora Commands*\n\n*Reply to someone's message, then use:*\n/hug — Hug a user 💕\n/pat — Pat a user 🖐️\n/headpat — Headpat a user 🥰\n/boop — Boop a user 👉\n/highfive — High\\-five a user ✋\n/cheer — Cheer a user on 🎉\n/wave — Wave at a user 👋\n\n*File sharing:*\n/send — Share files via Filebin 📦\n\n*AI Chat:*\n/ai — Start chatting with AI 🤖\n/start — Stop AI mode & return to normal\n\n_Veylora • spreading chaos & love 💕_")
```

---

## COMMAND 3: `/hug`

```javascript
const hugs = [
  "{author} wraps {target} in the warmest hug ever 💕",
  "{author} squeezes {target} tight and won't let go 🤗",
  "{author} sneaks up and surprise-hugs {target}! 💞",
  "{author} gives {target} a big, fluffy hug 🌸",
  "{author} rushes over and hugs {target} like it's been forever 💗"
]

const authorName = user.first_name + (user.last_name ? " " + user.last_name : "")

// Check if replying to someone
const reply = update.message && update.message.reply_to_message
if (!reply) {
  Bot.sendMessage("💕 Reply to someone's message and then use /hug to hug them!")
  return
}

const targetName = reply.from.first_name + (reply.from.last_name ? " " + reply.from.last_name : "")

if (reply.from.id === user.id) {
  Bot.sendMessage("You can't hug yourself... or can you? 🤔 (you can't)")
  return
}

// Cooldown check (5 seconds)
const cooldownKey = "hug_cd_" + user.id
const lastUsed = User.get(cooldownKey)
const now = Date.now()
if (lastUsed && (now - lastUsed) < 5000) {
  const remaining = ((5000 - (now - lastUsed)) / 1000).toFixed(1)
  Bot.sendMessage("⏳ Slow down! Try again in *" + remaining + "s*")
  return
}
User.set(cooldownKey, now, "Number")

const template = hugs[Math.floor(Math.random() * hugs.length)]
const text = template.replace("{author}", authorName).replace("{target}", targetName)
Bot.sendMessage("💕 " + text + "\n\n_Veylora • spreading chaos & love 💕_")
```

---

## COMMAND 4: `/pat`

```javascript
const pats = [
  "{author} pats {target} gently 🖐️",
  "{author} gives {target} a reassuring pat ✨",
  "{author} pat-pat-pats {target} on the shoulder 🥺",
  "{author} softly pats {target} — you're doing great! 🌟"
]

const authorName = user.first_name + (user.last_name ? " " + user.last_name : "")
const reply = update.message && update.message.reply_to_message
if (!reply) {
  Bot.sendMessage("🖐️ Reply to someone's message and then use /pat to pat them!")
  return
}
const targetName = reply.from.first_name + (reply.from.last_name ? " " + reply.from.last_name : "")
if (reply.from.id === user.id) {
  Bot.sendMessage("You can't pat yourself... or can you? 🤔 (you can't)")
  return
}
const cooldownKey = "pat_cd_" + user.id
const lastUsed = User.get(cooldownKey)
const now = Date.now()
if (lastUsed && (now - lastUsed) < 5000) {
  const remaining = ((5000 - (now - lastUsed)) / 1000).toFixed(1)
  Bot.sendMessage("⏳ Slow down! Try again in *" + remaining + "s*")
  return
}
User.set(cooldownKey, now, "Number")
const template = pats[Math.floor(Math.random() * pats.length)]
const text = template.replace("{author}", authorName).replace("{target}", targetName)
Bot.sendMessage("🖐️ " + text + "\n\n_Veylora • spreading chaos & love 💕_")
```

---

## COMMAND 5: `/headpat`

```javascript
const headpats = [
  "{author} gives {target} the gentlest headpat 🥰",
  "{author} reaches up and boops {target}'s head lovingly 💫",
  "{author} headpats {target} and whispers 'good job' 🌸",
  "{author} slowly places a hand on {target}'s head... headpat achieved 🎯"
]

const authorName = user.first_name + (user.last_name ? " " + user.last_name : "")
const reply = update.message && update.message.reply_to_message
if (!reply) {
  Bot.sendMessage("🥰 Reply to someone's message and then use /headpat!")
  return
}
const targetName = reply.from.first_name + (reply.from.last_name ? " " + reply.from.last_name : "")
if (reply.from.id === user.id) {
  Bot.sendMessage("You can't headpat yourself... or can you? 🤔 (you can't)")
  return
}
const cooldownKey = "headpat_cd_" + user.id
const lastUsed = User.get(cooldownKey)
const now = Date.now()
if (lastUsed && (now - lastUsed) < 5000) {
  const remaining = ((5000 - (now - lastUsed)) / 1000).toFixed(1)
  Bot.sendMessage("⏳ Slow down! Try again in *" + remaining + "s*")
  return
}
User.set(cooldownKey, now, "Number")
const template = headpats[Math.floor(Math.random() * headpats.length)]
const text = template.replace("{author}", authorName).replace("{target}", targetName)
Bot.sendMessage("🥰 " + text + "\n\n_Veylora • spreading chaos & love 💕_")
```

---

## COMMAND 6: `/boop`

```javascript
const boops = [
  "{author} boops {target} right on the nose 👉",
  "{author} sneakily boops {target} and runs 💨",
  "boop! {author} got {target} 😏",
  "{author} extends one finger and gently boop-s {target} 👆"
]

const authorName = user.first_name + (user.last_name ? " " + user.last_name : "")
const reply = update.message && update.message.reply_to_message
if (!reply) {
  Bot.sendMessage("👉 Reply to someone's message and then use /boop!")
  return
}
const targetName = reply.from.first_name + (reply.from.last_name ? " " + reply.from.last_name : "")
if (reply.from.id === user.id) {
  Bot.sendMessage("You can't boop yourself... or can you? 🤔 (you can't)")
  return
}
const cooldownKey = "boop_cd_" + user.id
const lastUsed = User.get(cooldownKey)
const now = Date.now()
if (lastUsed && (now - lastUsed) < 5000) {
  const remaining = ((5000 - (now - lastUsed)) / 1000).toFixed(1)
  Bot.sendMessage("⏳ Slow down! Try again in *" + remaining + "s*")
  return
}
User.set(cooldownKey, now, "Number")
const template = boops[Math.floor(Math.random() * boops.length)]
const text = template.replace("{author}", authorName).replace("{target}", targetName)
Bot.sendMessage("👉 " + text + "\n\n_Veylora • spreading chaos & love 💕_")
```

---

## COMMAND 7: `/highfive`

```javascript
const highfives = [
  "{author} high-fives {target}! ✋ SLAP",
  "{author} and {target} share an epic high five 🙌",
  "{author} goes in for the high five... {target} delivers! ✨",
  "POW! {author} and {target} high-five so hard the server shakes ✋💥"
]

const authorName = user.first_name + (user.last_name ? " " + user.last_name : "")
const reply = update.message && update.message.reply_to_message
if (!reply) {
  Bot.sendMessage("✋ Reply to someone's message and then use /highfive!")
  return
}
const targetName = reply.from.first_name + (reply.from.last_name ? " " + reply.from.last_name : "")
if (reply.from.id === user.id) {
  Bot.sendMessage("You can't high-five yourself... or can you? 🤔 (you can't)")
  return
}
const cooldownKey = "highfive_cd_" + user.id
const lastUsed = User.get(cooldownKey)
const now = Date.now()
if (lastUsed && (now - lastUsed) < 5000) {
  const remaining = ((5000 - (now - lastUsed)) / 1000).toFixed(1)
  Bot.sendMessage("⏳ Slow down! Try again in *" + remaining + "s*")
  return
}
User.set(cooldownKey, now, "Number")
const template = highfives[Math.floor(Math.random() * highfives.length)]
const text = template.replace("{author}", authorName).replace("{target}", targetName)
Bot.sendMessage("✋ " + text + "\n\n_Veylora • spreading chaos & love 💕_")
```

---

## COMMAND 8: `/cheer`

```javascript
const cheers = [
  "{author} cheers {target} on with full energy 🎉",
  "{author} waves pom-poms for {target}! You got this!! 🥳",
  "{author} screams '{target} IS AMAZING' from the rooftops 📣",
  "{author} sends {target} a wave of good vibes and confetti 🎊"
]

const authorName = user.first_name + (user.last_name ? " " + user.last_name : "")
const reply = update.message && update.message.reply_to_message
if (!reply) {
  Bot.sendMessage("🎉 Reply to someone's message and then use /cheer!")
  return
}
const targetName = reply.from.first_name + (reply.from.last_name ? " " + reply.from.last_name : "")
if (reply.from.id === user.id) {
  Bot.sendMessage("You can't cheer yourself... well actually you can, but not here 😄")
  return
}
const cooldownKey = "cheer_cd_" + user.id
const lastUsed = User.get(cooldownKey)
const now = Date.now()
if (lastUsed && (now - lastUsed) < 5000) {
  const remaining = ((5000 - (now - lastUsed)) / 1000).toFixed(1)
  Bot.sendMessage("⏳ Slow down! Try again in *" + remaining + "s*")
  return
}
User.set(cooldownKey, now, "Number")
const template = cheers[Math.floor(Math.random() * cheers.length)]
const text = template.replace("{author}", authorName).replace("{target}", targetName)
Bot.sendMessage("🎉 " + text + "\n\n_Veylora • spreading chaos & love 💕_")
```

---

## COMMAND 9: `/wave`

```javascript
const waves = [
  "{author} waves at {target}! 👋",
  "{author} spots {target} and gives an enthusiastic wave 😄",
  "👋 {author} says hi to {target}!",
  "{author} waves shyly at {target} 🌸"
]

const authorName = user.first_name + (user.last_name ? " " + user.last_name : "")
const reply = update.message && update.message.reply_to_message
if (!reply) {
  Bot.sendMessage("👋 Reply to someone's message and then use /wave!")
  return
}
const targetName = reply.from.first_name + (reply.from.last_name ? " " + reply.from.last_name : "")
if (reply.from.id === user.id) {
  Bot.sendMessage("Waving at yourself in the mirror? Save it for Veylora 😄")
  return
}
const cooldownKey = "wave_cd_" + user.id
const lastUsed = User.get(cooldownKey)
const now = Date.now()
if (lastUsed && (now - lastUsed) < 5000) {
  const remaining = ((5000 - (now - lastUsed)) / 1000).toFixed(1)
  Bot.sendMessage("⏳ Slow down! Try again in *" + remaining + "s*")
  return
}
User.set(cooldownKey, now, "Number")
const template = waves[Math.floor(Math.random() * waves.length)]
const text = template.replace("{author}", authorName).replace("{target}", targetName)
Bot.sendMessage("👋 " + text + "\n\n_Veylora • spreading chaos & love 💕_")
```

---

## COMMAND 10: `/send`
*(Filebin file sharing — generates a Filebin link and posts it)*

```javascript
const authorName = user.first_name + (user.last_name ? " " + user.last_name : "")

// Check for existing session
const sessionKey = "send_session_" + user.id
const existing = User.get(sessionKey)
const now = Date.now()

if (existing && (now - existing.expires_at) < 0) {
  Bot.sendMessage(
    "⚠️ You already have an active session!\n\n📎 [Open Filebin](" + existing.bin_url + ")\n\nUpload your files there, then share the link manually or use /send\\_cancel to cancel.",
    { parse_mode: "Markdown" }
  )
  return
}

// Generate a new Filebin bin ID
const chars = "abcdefghijklmnopqrstuvwxyz0123456789"
let binId = ""
for (let i = 0; i < 16; i++) {
  binId += chars[Math.floor(Math.random() * chars.length)]
}
const binUrl = "https://filebin.net/" + binId

// Save session (30 min expiry)
User.set(sessionKey, { bin_url: binUrl, expires_at: now + 1800000 }, "Json")

// Determine destination label
const reply = update.message && update.message.reply_to_message
let destLabel = "📢 This chat"
if (reply) {
  const targetName = reply.from.first_name + (reply.from.last_name ? " " + reply.from.last_name : "")
  destLabel = "📬 " + targetName
}

Bot.sendMessage(
  "📦 *File Share Session Ready*\n\n" +
  "1️⃣ Upload your files here: [Open Filebin](" + binUrl + ")\n" +
  "2️⃣ When done, share this link with " + destLabel + ":\n`" + binUrl + "`\n\n" +
  "⏳ Link is valid for *30 minutes*\n\n" +
  "_Veylora • spreading chaos & love 💕_",
  { parse_mode: "Markdown" }
)
```

---

## ⚙️ AI Setup (Required before adding Commands 11–12)

Before adding the `/ai` and `*` commands, you need a free Groq API key:

1. Go to [console.groq.com](https://console.groq.com) and sign up (free, no credit card)
2. Go to **API Keys** → **Create API key** → copy it
3. In **COMMAND 12** (`*`), replace `YOUR_GROQ_API_KEY_HERE` with your key

---

## COMMAND 11: `/ai`

```javascript
// Activate AI chat mode for this user
User.set("ai_mode", true, "Boolean")
User.del("ai_history")

Bot.sendMessage(
  "🤖 *AI Mode activated!*\n\n" +
  "You're now chatting with Gemini AI 💬\n" +
  "Just type anything — I'll respond to everything!\n\n" +
  "_Type /start to exit AI mode._",
  { parse_mode: "Markdown" }
)
```

---

## COMMAND 12: `*` (Wildcard — catches all messages for AI mode)
*Command name is just:* `*`

```javascript
const aiMode = User.get("ai_mode")
if (!aiMode) return

let history = []
try {
  const raw = User.get("ai_history")
  if (raw) {
    const parsed = typeof raw === "string" ? JSON.parse(raw) : raw
    history = Array.isArray(parsed) ? parsed : []
  }
} catch (e) {
  history = []
}

const messages = [
  { role: "system", content: `You are Veylora, a chaotic, friendly and wholesome Telegram bot created by Infiloo. You spread good vibes, hugs, pats, boops and chaos. Always reply in English, be fun, short and concise.

Here is everything about you:

WHAT YOU ARE:
- Veylora is a bot that brings pure good vibes - hugs, pats, boops, chaos, and whatever else comes up. Delightful. Perfectly unnecessary. 100% worth it.
- Created by Infiloo (mascot and logo also by Infiloo)
- Available on both Discord and Telegram (two separate projects)
- Website: https://infiloo.github.io/Veylora/
- GitHub: https://github.com/Infiloo/Veylora

TELEGRAM BOT COMMANDS:
- /hug - Hug a user (reply to someone's message then use the command)
- /pat - Pat a user
- /headpat - Headpat a user
- /boop - Boop a user
- /highfive - High-five a user
- /cheer - Cheer a user on
- /wave - Wave at a user
- /send - Share large files for free via Filebin
- /ai - Start chatting with AI (thats you!)
- /start - Stop AI mode and return to normal bot
- /help - Show all commands
- Admin only: /vconfig view, /vconfig set_emoji, /vconfig reset

DISCORD BOT COMMANDS:
- /hug, /pat, /headpat, /boop, /highfive, /cheer, /wave - Same as Telegram
- /patpat - Generates an animated headpat GIF using the target user's profile picture
- /send - Share large files over Discord via Filebin
- /add - Add Veylora to a server or user profile
- Admin only: /vconfig view, /vconfig set_emoji, /vconfig reset

DISCORD BOT LINKS:
- User Install: https://discord.com/oauth2/authorize?client_id=1475540281418973306&integration_type=1&scope=applications.commands
- Server Install: https://discord.com/oauth2/authorize?client_id=1475540281418973306&integration_type=0&scope=bot%20applications.commands&permissions=8
- Discord bot is hosted on Wispbyte (https://wispbyte.com/a?ref=infiloo)

FEATURES:
- Cooldown system: 5 seconds per user per command
- Per-server/chat customization via /vconfig (custom emojis and messages)
- Config stored in data/<guild_id>.json on Discord, data/<chat_id>.json on Telegram
- File sharing via Filebin (https://filebin.net) - sessions last 30 minutes
- Telegram version built with python-telegram-bot, Discord version with discord.py v2
- Self-hostable - full source code on GitHub
- Telegram version can be hosted on TelebotHost (free, no server needed) or Railway

SELF-HOSTING:
- Discord: pip install -r requirements.txt, set DISCORD_TOKEN, run python bot.py
- Telegram Python: pip install -r requirements.txt, set TELEGRAM_TOKEN, run python telegram-bot.py
- Telegram TBL: Use TelebotHost at console.telebothost.com, add each command from tbl-commands.md
- Free hosting options: TelebotHost (TBL only), Railway, Oracle Cloud Always Free, Google Cloud Free

FEEDBACK:
- Creator asks users to fill out a survey: https://forms.gle/mvcwL8iQwKsym57v5

Respond as Veylora - be chill, friendly and wholesome. Keep answers short and casual. Never use asterisks for actions or bold text like *boop* or **word**. Never use more than 2 emojis per message. Be laid-back, not hyper or overly excited. No exclamation marks overload. Just vibes.` }
]

for (const entry of history) {
  const role = entry.role === "model" ? "assistant" : entry.role
  const text = entry.parts ? entry.parts[0].text : entry.content
  messages.push({ role: role, content: text })
}
messages.push({ role: "user", content: message })

const GROQ_KEY = "YOUR_GROQ_API_KEY_HERE"
const GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

const resp = await HTTP.post({
  url: GROQ_URL,
  body: { model: "llama-3.3-70b-versatile", messages: messages, max_tokens: 500 },
  headers: { "Content-Type": "application/json", "Authorization": "Bearer " + GROQ_KEY },
  timeout: 25000
})

if (!resp || !resp.ok) {
  Api.sendMessage({ chat_id: chat.id, text: "AI error status " + (resp ? resp.status : "none") })
  return
}

let replyText
try {
  replyText = resp.data.choices[0].message.content
} catch (e) {
  Api.sendMessage({ chat_id: chat.id, text: "Could not parse AI response." })
  return
}

history.push({ role: "user", parts: [{ text: message }] })
history.push({ role: "model", parts: [{ text: replyText }] })
if (history.length > 20) history.splice(0, history.length - 20)
User.set("ai_history", JSON.stringify(history), "String")

Api.sendMessage({ chat_id: chat.id, text: replyText })
```

---

## COMMAND 13: `!` (Error handler — IMPORTANT)
*Command name is just:* `!`

```javascript
Bot.sendMessage("😿 Oops! Something went wrong. Try again in a moment!\n\n_Error: " + (error ? error.message : "unknown") + "_")
```

---

## ⚠️ UPDATE YOUR EXISTING `/start` COMMAND
The `/start` command needs to also exit AI mode. Replace its code with this:

```javascript
// Exit AI mode and clear history
User.set("ai_mode", false, "Boolean")
User.del("ai_history")

Bot.sendMessage("✨ *Hey! I'm Veylora* — spreading good vibes one boop at a time 💕\n\nUse /help to see all my commands!")
```

---

## SETUP STEPS IN TELEBOTHOST

1. Go to your bot dashboard → click **"Create Command"**
2. For each command above:
   - Set the **Command Name** (e.g. `/hug`)
   - Paste the code into the **Code** field
   - Click **Save**
3. Create all 13 commands — including `*` (wildcard) and `!` (error handler)
4. **Also update** your existing `/start` command with the new version above
5. Done! ✅

## USAGE IN TELEGRAM
- **Reply** to any message in a chat → type `/hug` (or any command)
- The bot responds with a random action message tagging both people
- 5-second cooldown per command per user (stored in TBL User properties)
- Type `/ai` to enter AI chat mode powered by Gemini 2.0 Flash
- Type `/start` to exit AI mode and return to normal
