"""
Veylora Telegram Bot
Creator: Infiloo
Telegram port of the original Discord bot.
"""

import os
import io
import json
import time
import random
import asyncio
import secrets
import aiohttp
from pathlib import Path

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from telegram.constants import ParseMode

# ─────────────────────────────────────────────
#  Config
# ─────────────────────────────────────────────
TOKEN = os.environ.get("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN_HERE")
DEFAULT_COOLDOWN = 5   # seconds
PATPAT_COOLDOWN  = 10  # seconds

# ─────────────────────────────────────────────
#  Responses  (mirrors Discord bot exactly)
# ─────────────────────────────────────────────
RESPONSES = {
    "hug": {
        "emoji": "💕",
        "messages": [
            "{author} wraps {target} in the warmest hug ever 💕",
            "{author} squeezes {target} tight and won't let go 🤗",
            "{author} sneaks up and surprise-hugs {target}! 💞",
            "{author} gives {target} a big, fluffy hug 🌸",
            "{author} rushes over and hugs {target} like it's been forever 💗",
        ],
    },
    "pat": {
        "emoji": "🖐️",
        "messages": [
            "{author} pats {target} gently 🖐️",
            "{author} gives {target} a reassuring pat ✨",
            "{author} pat-pat-pats {target} on the shoulder 🥺",
            "{author} softly pats {target} — you're doing great! 🌟",
        ],
    },
    "headpat": {
        "emoji": "🥰",
        "messages": [
            "{author} gives {target} the gentlest headpat 🥰",
            "{author} reaches up and boops {target}'s head lovingly 💫",
            "{author} headpats {target} and whispers 'good job' 🌸",
            "{author} slowly places a hand on {target}'s head... headpat achieved 🎯",
        ],
    },
    "boop": {
        "emoji": "👉",
        "messages": [
            "{author} boops {target} right on the nose 👉",
            "{author} sneakily boops {target} and runs 💨",
            "boop! {author} got {target} 😏",
            "{author} extends one finger and gently boop-s {target} 👆",
        ],
    },
    "highfive": {
        "emoji": "✋",
        "messages": [
            "{author} high-fives {target}! ✋ SLAP",
            "{author} and {target} share an epic high five 🙌",
            "{author} goes in for the high five... {target} delivers! ✨",
            "POW! {author} and {target} high-five so hard the server shakes ✋💥",
        ],
    },
    "cheer": {
        "emoji": "🎉",
        "messages": [
            "{author} cheers {target} on with full energy 🎉",
            "{author} waves pom-poms for {target}! You got this!! 🥳",
            "{author} screams '{target} IS AMAZING' from the rooftops 📣",
            "{author} sends {target} a wave of good vibes and confetti 🎊",
        ],
    },
    "wave": {
        "emoji": "👋",
        "messages": [
            "{author} waves at {target}! 👋",
            "{author} spots {target} and gives an enthusiastic wave 😄",
            "👋 {author} says hi to {target}!",
            "{author} waves shyly at {target} 🌸",
        ],
    },
}

# ─────────────────────────────────────────────
#  Per-chat config storage  (mirrors guild config)
# ─────────────────────────────────────────────
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def load_chat_config(chat_id: int) -> dict:
    path = DATA_DIR / f"{chat_id}.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def save_chat_config(chat_id: int, config: dict):
    path = DATA_DIR / f"{chat_id}.json"
    with open(path, "w") as f:
        json.dump(config, f, indent=2)


# ─────────────────────────────────────────────
#  Cooldown tracker
# ─────────────────────────────────────────────
_cooldowns: dict[tuple, float] = {}


def check_cooldown(user_id: int, command: str, seconds: int = DEFAULT_COOLDOWN) -> float:
    """Returns 0.0 if OK, else remaining seconds."""
    key = (user_id, command)
    now = time.time()
    if key in _cooldowns:
        elapsed = now - _cooldowns[key]
        if elapsed < seconds:
            return seconds - elapsed
    _cooldowns[key] = now
    return 0.0


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────

def display_name(user) -> str:
    """Return a friendly Telegram display name."""
    if user.first_name:
        name = user.first_name
        if user.last_name:
            name += f" {user.last_name}"
        return name
    return user.username or str(user.id)


def parse_mention(text: str, entities, bot_username: str):
    """
    Return the @username or None from the first mention in the message.
    Telegram doesn't give us a User object from a mention — callers should
    use reply-to instead for richer data.
    """
    for entity in (entities or []):
        if entity.type.name == "MENTION":
            start = entity.offset
            length = entity.length
            return text[start:start + length]
    return None


def build_action_text(action: str, author_name: str, target_name: str, chat_id: int) -> str:
    cfg = load_chat_config(chat_id)
    action_cfg = cfg.get(action, {})
    messages = action_cfg.get("messages") or RESPONSES[action]["messages"]
    emoji    = action_cfg.get("emoji")    or RESPONSES[action]["emoji"]
    template = random.choice(messages)
    text = template.format(author=author_name, target=target_name)
    return f"{emoji} {text}\n\n_Veylora • spreading chaos & love 💕_"


async def resolve_target(update: Update) -> tuple:
    """
    Returns (target_user, error_str | None).
    Strategy: prefer reply-to-message; otherwise fail with hint.
    """
    msg = update.message
    if msg.reply_to_message and msg.reply_to_message.from_user:
        return msg.reply_to_message.from_user, None
    return None, "Please **reply** to the user you want to target, or mention them with @username."


async def run_interaction(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    action: str,
    cooldown: int = DEFAULT_COOLDOWN,
):
    msg = update.message
    author = msg.from_user
    chat_id = msg.chat_id

    # Resolve target
    target, err = await resolve_target(update)

    # If no reply, check if they passed a @mention in args
    if target is None and context.args:
        # We can't resolve a username to a User object without extra API calls;
        # just use the username string as the display name.
        raw = " ".join(context.args).strip().lstrip("@")
        target_name = raw or "someone"
        target_is_self = False
        target_is_bot  = False
    elif target:
        target_name    = display_name(target)
        target_is_self = (target.id == author.id)
        target_is_bot  = target.is_bot
    else:
        await msg.reply_text(
            "❓ Who do you want to target? Reply to their message or pass @username.",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    # Self-action check
    if target and target_is_self:
        await msg.reply_text(
            "You can't do that to yourself... or can you? 🤔 (you can't)",
        )
        return

    # Bot target check
    if target and target_is_bot and target.id != (await context.bot.get_me()).id:
        await msg.reply_text("Robots have feelings too, but they're busy... try a human! 🤖")
        return

    # Cooldown
    remaining = check_cooldown(author.id, action, cooldown)
    if remaining > 0:
        await msg.reply_text(f"⏳ Slow down! Try again in **{remaining:.1f}s**", parse_mode=ParseMode.MARKDOWN)
        return

    author_name = display_name(author)
    text = build_action_text(action, author_name, target_name, chat_id)
    await msg.reply_text(text, parse_mode=ParseMode.MARKDOWN)


# ─────────────────────────────────────────────
#  /start  &  /help
# ─────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "✨ *Hey! I'm Veylora* — spreading good vibes one boop at a time 💕\n\n"
        "Use `/help` to see all my commands!"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💕 *Veylora Commands*\n\n"
        "*Interaction commands* — reply to someone or pass @username:\n"
        "`/hug` — Hug a user 💕\n"
        "`/pat` — Pat a user 🖐️\n"
        "`/headpat` — Headpat a user 🥰\n"
        "`/boop` — Boop a user 👉\n"
        "`/highfive` — High-five a user ✋\n"
        "`/cheer` — Cheer a user on 🎉\n"
        "`/wave` — Wave at a user 👋\n"
        "`/patpat` — Animated headpat GIF 🐾\n\n"
        "*File sharing:*\n"
        "`/send` — Share files via Filebin 📦\n\n"
        "*Admin (groups only):*\n"
        "`/vconfig view` — View custom config\n"
        "`/vconfig set_emoji <action> <emoji>` — Override emoji\n"
        "`/vconfig reset` — Reset config\n\n"
        "_Veylora • spreading chaos & love 💕_"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


# ─────────────────────────────────────────────
#  Interaction commands
# ─────────────────────────────────────────────

async def cmd_hug(update, context):      await run_interaction(update, context, "hug")
async def cmd_pat(update, context):      await run_interaction(update, context, "pat")
async def cmd_headpat(update, context):  await run_interaction(update, context, "headpat")
async def cmd_boop(update, context):     await run_interaction(update, context, "boop")
async def cmd_highfive(update, context): await run_interaction(update, context, "highfive")
async def cmd_cheer(update, context):    await run_interaction(update, context, "cheer")
async def cmd_wave(update, context):     await run_interaction(update, context, "wave")


# ─────────────────────────────────────────────
#  /patpat — animated GIF
# ─────────────────────────────────────────────

async def cmd_patpat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg    = update.message
    author = msg.from_user

    # Resolve target
    target, err = await resolve_target(update)
    if target is None and context.args:
        target_name = " ".join(context.args).strip().lstrip("@") or "someone"
        target_photo_url = None
    elif target:
        if target.id == author.id:
            await msg.reply_text("You can't patpat yourself... but the thought is cute 🥺")
            return
        target_name = display_name(target)
        # Fetch profile photo
        photos = await context.bot.get_user_profile_photos(target.id, limit=1)
        if photos.total_count > 0:
            file = await context.bot.get_file(photos.photos[0][-1].file_id)
            target_photo_url = file.file_path
        else:
            target_photo_url = None
    else:
        await msg.reply_text("❓ Reply to someone or pass @username to patpat them!")
        return

    # Cooldown
    remaining = check_cooldown(author.id, "patpat", PATPAT_COOLDOWN)
    if remaining > 0:
        await msg.reply_text(f"⏳ Slow down! Try again in **{remaining:.1f}s**", parse_mode=ParseMode.MARKDOWN)
        return

    processing = await msg.reply_text("🐾 Generating patpat GIF...")

    try:
        from petpetgif import petpet as petpetgif

        if target_photo_url:
            async with aiohttp.ClientSession() as session:
                async with session.get(target_photo_url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status != 200:
                        raise RuntimeError("Avatar fetch failed")
                    avatar_bytes = await resp.read()
        else:
            # Fallback: blank white square
            from PIL import Image
            img = Image.new("RGBA", (128, 128), (255, 255, 255, 255))
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            avatar_bytes = buf.getvalue()

        source = io.BytesIO(avatar_bytes)
        dest   = io.BytesIO()
        await asyncio.get_event_loop().run_in_executor(None, petpetgif.make, source, dest)
        dest.seek(0)

        caption = (
            f"🐾 {display_name(author)} patpats {target_name}!\n"
            "_Veylora • spreading chaos & love 💕_"
        )
        await processing.delete()
        await msg.reply_animation(animation=dest, caption=caption, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        await processing.edit_text("😿 Something went wrong generating the GIF, try again later!")


# ─────────────────────────────────────────────
#  /send — Filebin session sharing
# ─────────────────────────────────────────────

FILEBIN_BASE     = "https://filebin.net"
SESSION_LIFETIME = 30 * 60  # 30 minutes

# user_id -> {bin_id, bin_url, destination_chat_id, expires_at}
_send_sessions: dict[int, dict] = {}


def make_bin_id()  -> str: return secrets.token_urlsafe(12)
def make_bin_url(b) -> str: return f"{FILEBIN_BASE}/{b}"


async def cmd_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg    = update.message
    author = msg.from_user

    # Block duplicate session
    existing = _send_sessions.get(author.id)
    if existing and time.time() < existing["expires_at"]:
        keyboard = [[InlineKeyboardButton("Open Filebin 📎", url=existing["bin_url"])]]
        await msg.reply_text(
            f"⚠️ You already have an active session! Upload files and press **Send** when ready.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    # Determine destination chat
    if msg.reply_to_message and msg.reply_to_message.from_user:
        dest_user    = msg.reply_to_message.from_user
        dest_chat_id = dest_user.id   # send as DM
        dest_label   = f"📬 DM to **{display_name(dest_user)}**"
    elif context.args:
        # @username — we'll send to that username's chat; for simplicity post in same chat
        dest_chat_id = msg.chat_id
        dest_label   = f"📢 This chat"
    else:
        dest_chat_id = msg.chat_id
        dest_label   = f"📢 This chat"

    bin_id  = make_bin_id()
    bin_url = make_bin_url(bin_id)

    _send_sessions[author.id] = {
        "bin_id":       bin_id,
        "bin_url":      bin_url,
        "dest_chat_id": dest_chat_id,
        "expires_at":   time.time() + SESSION_LIFETIME,
    }

    keyboard = [
        [
            InlineKeyboardButton("Open Filebin 📎", url=bin_url),
        ],
        [
            InlineKeyboardButton("Send 📤",   callback_data=f"send_confirm:{author.id}"),
            InlineKeyboardButton("Cancel ✖", callback_data=f"send_cancel:{author.id}"),
        ],
    ]

    text = (
        f"📦 *File Share Session Ready*\n\n"
        f"📎 Upload your files → [Open Filebin]({bin_url})\n"
        f"📬 Will be sent to: {dest_label}\n"
        f"⏳ Session valid for **30 minutes**\n\n"
        f"Press **Send** when you're done uploading!"
    )

    # Try to DM the control panel to the issuer; fall back to in-chat
    try:
        await context.bot.send_message(
            chat_id=author.id,
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN,
        )
        await msg.reply_text("📬 Check your DMs — I've sent you your file share session!")
    except Exception:
        await msg.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN,
        )


async def callback_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query    = update.callback_query
    data     = query.data           # e.g. "send_confirm:12345"
    action, owner_id_str = data.split(":")
    owner_id = int(owner_id_str)

    # Only the issuer can interact
    if query.from_user.id != owner_id:
        await query.answer("This isn't your session! 👀", show_alert=True)
        return

    session = _send_sessions.get(owner_id)

    if action == "send_cancel":
        _send_sessions.pop(owner_id, None)
        await query.message.delete()
        await query.answer("Session cancelled.")
        return

    if action == "send_confirm":
        if not session or time.time() > session["expires_at"]:
            await query.answer("Session expired!", show_alert=True)
            return

        bin_url      = session["bin_url"]
        dest_chat_id = session["dest_chat_id"]

        delivery_text = (
            f"📦 *Files shared with you!*\n\n"
            f"**{display_name(query.from_user)}** sent you a file share link 💕\n\n"
            f"📎 [Open Filebin]({bin_url})\n\n"
            f"_Veylora • spreading chaos & love 💕_"
        )

        try:
            await context.bot.send_message(
                chat_id=dest_chat_id,
                text=delivery_text,
                parse_mode=ParseMode.MARKDOWN,
            )
            await query.answer("✅ Sent!")
            await query.message.edit_text(
                f"✅ Link delivered!\n\n📎 [Filebin]({bin_url})",
                reply_markup=None,
                parse_mode=ParseMode.MARKDOWN,
            )
        except Exception:
            await query.answer("😿 Couldn't deliver — DMs may be closed.", show_alert=True)

        _send_sessions.pop(owner_id, None)


# ─────────────────────────────────────────────
#  /vconfig — per-chat admin config
# ─────────────────────────────────────────────

async def cmd_vconfig(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg     = update.message
    chat_id = msg.chat_id
    args    = context.args or []

    # In groups, require admin
    if msg.chat.type in ("group", "supergroup"):
        member = await context.bot.get_chat_member(chat_id, msg.from_user.id)
        if member.status not in ("administrator", "creator"):
            await msg.reply_text("🔒 Only admins can configure Veylora.")
            return

    if not args:
        await msg.reply_text(
            "Usage:\n"
            "`/vconfig view`\n"
            "`/vconfig set_emoji <action> <emoji>`\n"
            "`/vconfig reset`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    sub = args[0].lower()

    if sub == "view":
        cfg = load_chat_config(chat_id)
        if not cfg:
            await msg.reply_text("No custom config set — using defaults! 🌸")
        else:
            txt = json.dumps(cfg, indent=2)
            await msg.reply_text(f"```json\n{txt[:3800]}\n```", parse_mode=ParseMode.MARKDOWN)

    elif sub == "set_emoji":
        if len(args) < 3:
            await msg.reply_text("Usage: `/vconfig set_emoji <action> <emoji>`", parse_mode=ParseMode.MARKDOWN)
            return
        action, emoji = args[1].lower(), args[2]
        if action not in RESPONSES:
            valid = ", ".join(RESPONSES.keys())
            await msg.reply_text(f"Unknown action `{action}`. Valid: {valid}", parse_mode=ParseMode.MARKDOWN)
            return
        cfg = load_chat_config(chat_id)
        cfg.setdefault(action, {})["emoji"] = emoji
        save_chat_config(chat_id, cfg)
        await msg.reply_text(f"✅ Emoji for `{action}` set to {emoji}", parse_mode=ParseMode.MARKDOWN)

    elif sub == "reset":
        path = DATA_DIR / f"{chat_id}.json"
        if path.exists():
            path.unlink()
        await msg.reply_text("✅ Config reset to defaults!")

    else:
        await msg.reply_text("Unknown subcommand. Use `view`, `set_emoji`, or `reset`.", parse_mode=ParseMode.MARKDOWN)


# ─────────────────────────────────────────────
#  App entry point
# ─────────────────────────────────────────────

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start",    cmd_start))
    app.add_handler(CommandHandler("help",     cmd_help))
    app.add_handler(CommandHandler("hug",      cmd_hug))
    app.add_handler(CommandHandler("pat",      cmd_pat))
    app.add_handler(CommandHandler("headpat",  cmd_headpat))
    app.add_handler(CommandHandler("boop",     cmd_boop))
    app.add_handler(CommandHandler("highfive", cmd_highfive))
    app.add_handler(CommandHandler("cheer",    cmd_cheer))
    app.add_handler(CommandHandler("wave",     cmd_wave))
    app.add_handler(CommandHandler("patpat",   cmd_patpat))
    app.add_handler(CommandHandler("send",     cmd_send))
    app.add_handler(CommandHandler("vconfig",  cmd_vconfig))
    app.add_handler(CallbackQueryHandler(callback_send, pattern=r"^send_(confirm|cancel):"))

    print("✨ Veylora Telegram Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
