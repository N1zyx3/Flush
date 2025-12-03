from discord.ext import commands
import discord

class Template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="template")
    async def template(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Template(bot))