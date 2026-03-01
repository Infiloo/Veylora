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
Bot.sendMessage("💕 *Veylora Commands*\n\n*Reply to someone's message, then use:*\n/hug — Hug a user 💕\n/pat — Pat a user 🖐️\n/headpat — Headpat a user 🥰\n/boop — Boop a user 👉\n/highfive — High\\-five a user ✋\n/cheer — Cheer a user on 🎉\n/wave — Wave at a user 👋\n\n*File sharing:*\n/send — Share files via Filebin 📦\n\n_Veylora • spreading chaos & love 💕_")
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

## COMMAND 11: `!` (Error handler — IMPORTANT)
*Command name is just:* `!`

```javascript
Bot.sendMessage("😿 Oops! Something went wrong. Try again in a moment!\n\n_Error: " + (error ? error.message : "unknown") + "_")
```

---

## SETUP STEPS IN TELEBOTHOST

1. Go to your bot dashboard → click **"Create Command"**
2. For each command above:
   - Set the **Command Name** (e.g. `/hug`)
   - Paste the code into the **Code** field
   - Click **Save**
3. Create all 11 commands
4. Done! ✅

## USAGE IN TELEGRAM
- **Reply** to any message in a chat → type `/hug` (or any command)
- The bot responds with a random action message tagging both people
- 5-second cooldown per command per user (stored in TBL User properties)
