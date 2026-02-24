"""
Veylora Discord Bot
Creator: Infiloo
"""

import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import time
import random
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
#  Run
# ─────────────────────────────────────────────
if __name__ == "__main__":
    bot.run(TOKEN)
