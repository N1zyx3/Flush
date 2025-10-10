import os
import discord
from dotenv import load_dotenv

load_dotenv()
token = str(os.getenv("TOKEN"))
owner_id = str(os.getenv("OWNER_ID"))
bot = discord.Bot(owner_ids=owner_id, prefix=".")

@bot.event
async def on_ready():
    print(f"{bot.user} онлайн")

bot.run(token)