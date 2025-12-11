import os
import json
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
token = str(os.getenv("TOKEN"))
admin_ids = {int(i) for i in os.getenv("ADMIN_IDS").split(",")}
bot = commands.Bot(owner_ids=list(admin_ids), command_prefix=".", intents=discord.Intents.all(), help_command=None)

bot.admin_mode = True
TOGGLE_FILE = "config/toggles.json"

@bot.check
async def global_command_check(ctx):
    if bot.admin_mode and ctx.author.id not in admin_ids:
        await ctx.send("Включен Admin mode. Взаимодействие с ботом невозможно")
        return False
    return True

def load_toggles():
    if not os.path.exists(TOGGLE_FILE):
        return {"commands": {}, "cogs": {}}
    with open(TOGGLE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_toggles(data):
    with open(TOGGLE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

toggles = load_toggles()

@bot.event
async def on_ready():
    print(f"{bot.user} онлайн\nAdmin mode: {bot.admin_mode}\nLoaded cogs:")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return
    print(f"Ошибка команды: {error}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Неизвестная команда. Все доступные команды: `.help`")
        return

    raise error

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

for cmd_name, enabled in toggles["commands"].items():
    cmd = bot.get_command(cmd_name)
    if cmd:
        cmd.enabled = enabled

for cog_name, enabled in toggles["cogs"].items():
    if not enabled:
        try:
            bot.unload_extension(f"cogs.{cog_name}")
        except:
            pass

bot.run(token)