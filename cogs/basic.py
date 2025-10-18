from discord.ext import commands
import discord

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- HELP ---
    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="📘 Команды бота",
            description="Вот что я умею:",
            color=discord.Color.blurple()
        )
        embed.add_field(name=".serverinfo", value="Показать информацию о сервере", inline=False)
        embed.add_field(name=".userinfo [пользователь]", value="Информация о пользователе", inline=False)
        # embed.add_field(name=".kick [пользователь]", value="Кикнуть участника", inline=False)
        # embed.add_field(name=".ban [пользователь]", value="Забанить участника", inline=False)
        await ctx.send(embed=embed)

    # --- SERVER INFO ---
    @commands.command(name="serverinfo")
    async def server_info(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(
            title=f"🌐 Информация о сервере {guild.name}",
            color=discord.Color.green()
        )
        embed.add_field(name=f"👑 Владелец: {guild.owner}", value="", inline=True)
        embed.add_field(name=f"🆔 ID: {guild.id}", value="", inline=False)
        embed.add_field(name=f"👥 Участников: {guild.member_count}", value="", inline=False)
        embed.add_field(name=f"📆 Создан {guild.created_at.strftime("%d.%m.%Y %H:%M:%S")}", value="", inline=False)
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        await ctx.send(embed=embed)

    # --- USER INFO ---
    @commands.command(name="userinfo")
    async def user_info(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(
            title=f"👤 Информация о {member}",
            color=discord.Color.orange()
        )
        embed.add_field(name=f"🆔 ID: {member.id}", value="", inline=False)
        embed.add_field(name=f"📅 Аккаунт создан: {member.created_at.strftime("%d.%m.%Y %H:%M:%S")}", value="", inline=False)
        embed.add_field(name=f"📥 Присоединился {member.joined_at.strftime("%d.%m.%Y %H:%M:%S")}", value="", inline=False)
        embed.add_field(
            name="🎭 Роли",
            value=", ".join([role.mention for role in member.roles if role != ctx.guild.default_role]),
            inline=False
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Basic(bot))
