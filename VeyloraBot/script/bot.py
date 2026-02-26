"""
Veylora Discord Bot
Creator: Infiloo
"""

import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import io
import time
import random
import asyncio
import aiohttp
from pathlib import Path

# ─────────────────────────────────────────────
#  Config
# ─────────────────────────────────────────────
TOKEN = os.environ.get("DISCORD_TOKEN", "YOUR_TOKEN_HERE")
DEFAULT_COOLDOWN = 5  # seconds

# ─────────────────────────────────────────────
#  Responses
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
#  Per-server config storage
# ─────────────────────────────────────────────
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def load_guild_config(guild_id: int) -> dict:
    path = DATA_DIR / f"{guild_id}.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


def save_guild_config(guild_id: int, config: dict):
    path = DATA_DIR / f"{guild_id}.json"
    with open(path, "w") as f:
        json.dump(config, f, indent=2)


# ─────────────────────────────────────────────
#  Cooldown tracker
# ─────────────────────────────────────────────
_cooldowns: dict[tuple, float] = {}


def check_cooldown(user_id: int, command: str, seconds: int = DEFAULT_COOLDOWN) -> float:
    """Returns 0 if OK, otherwise remaining seconds."""
    key = (user_id, command)
    now = time.time()
    if key in _cooldowns:
        elapsed = now - _cooldowns[key]
        if elapsed < seconds:
            return seconds - elapsed
    _cooldowns[key] = now
    return 0.0


# ─────────────────────────────────────────────
#  Bot setup
# ─────────────────────────────────────────────
intents = discord.Intents.none()

class VeyloraBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="v!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Synced slash commands globally (including DMs).")

    async def on_ready(self):
        activity = discord.Activity(
            type=discord.ActivityType.playing,
            name="spreading good vibes 💕"
        )
        await self.change_presence(activity=activity)
        print(f"✨ Veylora is online as {self.user} (ID: {self.user.id})")


bot = VeyloraBot()

# ─────────────────────────────────────────────
#  Helper
# ─────────────────────────────────────────────

def build_embed(action: str, author: discord.User, target: discord.User, guild_id: int) -> discord.Embed:
    cfg = load_guild_config(guild_id)
    action_cfg = cfg.get(action, {})

    # Custom messages override defaults
    messages = action_cfg.get("messages") or RESPONSES[action]["messages"]
    emoji = action_cfg.get("emoji") or RESPONSES[action]["emoji"]

    template = random.choice(messages)
    text = template.format(
        author=author.display_name,
        target=target.display_name,
    )

    embed = discord.Embed(description=f"{emoji} {text}", color=0xf4a7c3)
    embed.set_footer(text="Veylora • spreading chaos & love 💕")
    return embed


async def interaction_command(
    interaction: discord.Interaction,
    target: discord.User,
    action: str,
):
    # Self-action check
    if target.id == interaction.user.id:
        await interaction.response.send_message(
            "You can't do that to yourself... or can you? 🤔 (you can't)", ephemeral=True
        )
        return

    # Bot target
    if target.bot and target.id != bot.user.id:
        await interaction.response.send_message(
            "Robots have feelings too, but they're busy... try a human! 🤖", ephemeral=True
        )
        return

    # Cooldown
    remaining = check_cooldown(interaction.user.id, action)
    if remaining > 0:
        await interaction.response.send_message(
            f"⏳ Slow down! Try again in **{remaining:.1f}s**", ephemeral=True
        )
        return

    guild_id = interaction.guild_id or 0
    embed = build_embed(action, interaction.user, target, guild_id)  # type: ignore
    await interaction.response.send_message(embed=embed)


# ─────────────────────────────────────────────
#  Slash Commands
# ─────────────────────────────────────────────

@bot.tree.command(name="hug", description="Hug a user 💕")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(user="Who do you want to hug?")
async def hug(interaction: discord.Interaction, user: discord.User):
    await interaction_command(interaction, user, "hug")


@bot.tree.command(name="pat", description="Pat a user 🖐️")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(user="Who do you want to pat?")
async def pat(interaction: discord.Interaction, user: discord.User):
    await interaction_command(interaction, user, "pat")


@bot.tree.command(name="headpat", description="Headpat a user 🥰")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(user="Who gets the headpat?")
async def headpat(interaction: discord.Interaction, user: discord.User):
    await interaction_command(interaction, user, "headpat")


@bot.tree.command(name="boop", description="Boop a user 👉")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(user="Who are you booping?")
async def boop(interaction: discord.Interaction, user: discord.User):
    await interaction_command(interaction, user, "boop")


@bot.tree.command(name="highfive", description="Highfive a user ✋")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(user="Who gets the high five?")
async def highfive(interaction: discord.Interaction, user: discord.User):
    await interaction_command(interaction, user, "highfive")


@bot.tree.command(name="cheer", description="Cheer a user up 🎉")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(user="Who do you want to cheer on?")
async def cheer(interaction: discord.Interaction, user: discord.User):
    await interaction_command(interaction, user, "cheer")


@bot.tree.command(name="wave", description="Wave to a user 👋")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(user="Who are you waving at?")
async def wave(interaction: discord.Interaction, user: discord.User):
    await interaction_command(interaction, user, "wave")


@bot.tree.command(name="patpat", description="Generate a headpat GIF for a user 🐾")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(user="Who gets the patpat?")
async def patpat(interaction: discord.Interaction, user: discord.User):
    if user.id == interaction.user.id:
        await interaction.response.send_message(
            "You can't patpat yourself... but the thought is cute 🥺", ephemeral=True
        )
        return

    remaining = check_cooldown(interaction.user.id, "patpat", seconds=10)
    if remaining > 0:
        await interaction.response.send_message(
            f"⏳ Slow down! Try again in **{remaining:.1f}s**", ephemeral=True
        )
        return

    await interaction.response.defer()

    try:
        from petpetgif import petpet as petpetgif

        # Download avatar
        avatar_url = user.display_avatar.replace(format="png", size=128).url
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    await interaction.followup.send("😿 Couldn't fetch that user's avatar, try again!")
                    return
                avatar_bytes = await resp.read()

        # Generate petpet GIF locally (no external API)
        source = io.BytesIO(avatar_bytes)
        dest = io.BytesIO()
        await asyncio.get_event_loop().run_in_executor(None, petpetgif.make, source, dest)
        dest.seek(0)

        file = discord.File(fp=dest, filename="patpat.gif")
        embed = discord.Embed(
            description=f"🐾 {interaction.user.display_name} patpats {user.display_name}!",
            color=0xf4a7c3
        )
        embed.set_image(url="attachment://patpat.gif")
        embed.set_footer(text="Veylora • spreading chaos & love 💕")
        await interaction.followup.send(embed=embed, file=file)

    except Exception as e:
        await interaction.followup.send("😿 Something went wrong generating the gif, try again later!")


@bot.tree.command(name="add", description="Add Veylora to your Profile or Server ➕")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def add(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Add Veylora 💕",
        description=(
            "**[➕ Server Install](https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot+applications.commands&permissions=277025770560)**\n"
            "Add Veylora to your server for everyone to enjoy!\n\n"
            "**[👤 User Install](https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&integration_type=1&scope=applications.commands)**\n"
            "Install Veylora to your user profile for personal commands anywhere!\n\n"
            "*Spreading good vibes one boop at a time 💫*"
        ),
        color=0xf4a7c3,
    )
    embed.set_footer(text="Veylora • by Infiloo 💕")
    await interaction.response.send_message(embed=embed, ephemeral=True)


# ─────────────────────────────────────────────
#  Admin: per-server config command
# ─────────────────────────────────────────────

config_group = app_commands.Group(
    name="vconfig",
    description="Configure Veylora for this server (Admin only)",
    default_permissions=discord.Permissions(manage_guild=True),
)


@config_group.command(name="view", description="View current Veylora config for this server")
async def config_view(interaction: discord.Interaction):
    cfg = load_guild_config(interaction.guild_id or 0)
    if not cfg:
        await interaction.response.send_message("No custom config set — using defaults! 🌸", ephemeral=True)
        return
    txt = json.dumps(cfg, indent=2)
    await interaction.response.send_message(f"```json\n{txt[:1900]}\n```", ephemeral=True)


@config_group.command(name="set_emoji", description="Override the emoji for a command")
@app_commands.describe(action="Command name (hug, pat, etc.)", emoji="New emoji to use")
async def config_set_emoji(interaction: discord.Interaction, action: str, emoji: str):
    if action not in RESPONSES:
        await interaction.response.send_message(
            f"Unknown action `{action}`. Valid: {', '.join(RESPONSES.keys())}", ephemeral=True
        )
        return
    cfg = load_guild_config(interaction.guild_id or 0)
    cfg.setdefault(action, {})["emoji"] = emoji
    save_guild_config(interaction.guild_id or 0, cfg)
    await interaction.response.send_message(f"✅ Emoji for `{action}` set to {emoji}", ephemeral=True)


@config_group.command(name="reset", description="Reset all custom config for this server")
async def config_reset(interaction: discord.Interaction):
    path = DATA_DIR / f"{interaction.guild_id}.json"
    if path.exists():
        path.unlink()
    await interaction.response.send_message("✅ Config reset to defaults!", ephemeral=True)


bot.tree.add_command(config_group)

# ─────────────────────────────────────────────
#  /send — Filebin session sharing
# ─────────────────────────────────────────────

import secrets

# Active sessions: user_id -> {bin_id, bin_url, destination, expires_at}
# destination is either a discord.TextChannel or discord.User
_send_sessions: dict[int, dict] = {}
SESSION_LIFETIME = 30 * 60  # 30 minutes in seconds
FILEBIN_BASE = "https://filebin.net"


def make_bin_id() -> str:
    """Generate a unique Filebin bin ID."""
    return secrets.token_urlsafe(12)


def make_bin_url(bin_id: str) -> str:
    return f"{FILEBIN_BASE}/{bin_id}"


def destination_label(destination) -> str:
    """Human-readable destination for embed display."""
    if isinstance(destination, discord.User) or isinstance(destination, discord.Member):
        return f"📬 DM to **{destination.display_name}**"
    elif isinstance(destination, discord.TextChannel):
        return f"📢 Channel **#{destination.name}** in **{destination.guild.name}**"
    else:
        return "📬 Direct Message"


class SendView(discord.ui.View):
    def __init__(self, issuer: discord.User, bin_id: str, bin_url: str, destination):
        super().__init__(timeout=SESSION_LIFETIME)
        self.issuer = issuer
        self.bin_id = bin_id
        self.bin_url = bin_url
        self.destination = destination
        self.sent = False

    def build_preview_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="📦 File Share Session Ready",
            color=0xf4a7c3
        )
        embed.add_field(name="📎 Upload your files here", value=f"[Open Filebin]({self.bin_url})", inline=False)
        embed.add_field(name="📬 Will be sent to", value=destination_label(self.destination), inline=False)
        embed.add_field(
            name="⏳ Session expires",
            value="This session is valid for **30 minutes**. Click **Send** when ready.",
            inline=False
        )
        embed.set_footer(text="Veylora • spreading chaos & love 💕")
        return embed

    @discord.ui.button(label="Send 📤", style=discord.ButtonStyle.success)
    async def send_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.issuer.id:
            await interaction.response.send_message("This isn't your session! 👀", ephemeral=True)
            return

        if self.sent:
            await interaction.response.send_message("Already sent! 📬", ephemeral=True)
            return

        self.sent = True
        self.stop()

        # Disable buttons
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)

        # Build the delivery embed
        delivery_embed = discord.Embed(
            title="📦 Files shared with you!",
            description=f"**{self.issuer.display_name}** sent you a file share link 💕",
            color=0xf4a7c3
        )
        delivery_embed.add_field(name="📎 Download / View files", value=f"[Open Filebin]({self.bin_url})", inline=False)
        delivery_embed.set_footer(text="Veylora • spreading chaos & love 💕")

        try:
            if isinstance(self.destination, (discord.User, discord.Member)):
                await self.destination.send(embed=delivery_embed)
                await interaction.followup.send(
                    f"✅ Link sent to **{self.destination.display_name}**'s DMs!", ephemeral=True
                )
            elif isinstance(self.destination, discord.TextChannel):
                await self.destination.send(embed=delivery_embed)
                await interaction.followup.send(
                    f"✅ Link posted in **#{self.destination.name}**!", ephemeral=True
                )
        except discord.Forbidden:
            await interaction.followup.send(
                "😿 Couldn't deliver — the user may have DMs closed or I lack channel permissions.",
                ephemeral=True
            )

        # Clean up session
        _send_sessions.pop(self.issuer.id, None)

    @discord.ui.button(label="Cancel ✖", style=discord.ButtonStyle.danger)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.issuer.id:
            await interaction.response.send_message("This isn't your session! 👀", ephemeral=True)
            return

        self.stop()
        await interaction.message.delete()
        _send_sessions.pop(self.issuer.id, None)

    async def on_timeout(self):
        _send_sessions.pop(self.issuer.id, None)


@bot.tree.command(name="send", description="Share files with a user or channel via Filebin 📦")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(user="Send the files to a specific user (optional — leave empty to send to current channel/DM)")
async def send_cmd(interaction: discord.Interaction, user: discord.User = None):

    issuer = interaction.user

    # Block if already has an active session
    existing = _send_sessions.get(issuer.id)
    if existing and time.time() < existing["expires_at"]:
        await interaction.response.send_message(
            f"⚠️ You already have an active session! [Open it]({existing['bin_url']}) or cancel it first.",
            ephemeral=True
        )
        return

    # Determine destination
    if user is not None:
        # Explicit user target — always send as DM to that user
        destination = user
    elif interaction.guild is None:
        # In a DM — destination is the other person in the DM (the issuer receives the link to share)
        destination = issuer  # We send delivery back to this DM context
    else:
        # In a server, no user specified — send to the channel where command was run
        destination = interaction.channel

    # Create Filebin session
    bin_id = make_bin_id()
    bin_url = make_bin_url(bin_id)

    _send_sessions[issuer.id] = {
        "bin_id": bin_id,
        "bin_url": bin_url,
        "destination": destination,
        "expires_at": time.time() + SESSION_LIFETIME,
    }

    view = SendView(issuer=issuer, bin_id=bin_id, bin_url=bin_url, destination=destination)

    # Always send the control embed as an ephemeral DM-style message to the issuer
    try:
        dm = await issuer.create_dm()
        await dm.send(embed=view.build_preview_embed(), view=view)
        await interaction.response.send_message(
            "📬 Check your DMs — I've sent you your file share session!", ephemeral=True
        )
    except discord.Forbidden:
        # If DMs are closed, fall back to ephemeral in-channel
        await interaction.response.send_message(
            embed=view.build_preview_embed(), view=view, ephemeral=True
        )


if __name__ == "__main__":
    bot.run(TOKEN)
