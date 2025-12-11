import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
token = str(os.getenv("TOKEN"))
admin_ids = {int(i) for i in os.getenv("ADMIN_IDS").split(",")}
bot = commands.Bot(owner_ids=list(admin_ids), command_prefix=".", intents=discord.Intents.all(), help_command=None)

bot.admin_mode = True

@bot.check
async def global_command_check(ctx):
    if bot.admin_mode and ctx.author.id not in admin_ids:
        await ctx.send("Включен Admin mode. Взаимодействие с ботом невозможно")
        return False
    return True

@bot.event
async def on_ready():
    print(f"{bot.user} онлайн\nAdmin mode: {bot.admin_mode}\nLoaded cogs:", list(bot.cogs.keys()))

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

bot.run(token)