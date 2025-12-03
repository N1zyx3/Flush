from discord.ext import commands
import discord

class Autoroles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="autoroles")
    async def autoroles(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Autoroles(bot))