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

    # --- TOGGLE ---
    @commands.command(name="toggle")
    async def toggle(self, ctx, name: str):

        if ctx.author.id not in self.bot.owner_ids:
            await ctx.send("Только администраторы могут использовать эту команду.")
            return

        cmd = self.bot.get_command(name)

        if cmd:
            if cmd.name == "toggle":
                await ctx.send("Команду `toggle` нельзя отключить.")
                return

            cmd.enabled = not cmd.enabled

            await ctx.send(
                f"Команда `{cmd.name}` "
                f"{'включена' if cmd.enabled else 'отключена'}."
            )
            return

        loaded_cogs = list(self.bot.cogs.keys())

        if name.capitalize() in loaded_cogs:
            if name.lower() == "basic":
                await ctx.send("Cog `basic` нельзя выгружать.")
                return

            try:
                self.bot.unload_extension(f"cogs.{name}")
                await ctx.send(f"Cog `{name}` выгружен.")
            except Exception as e:
                await ctx.send(f"Не удалось выгрузить `{name}`: {e}")
            return

        try:
            self.bot.load_extension(f"cogs.{name}")
            await ctx.send(f"Cog `{name}` загружен.")
            return
        except:
            pass

        await ctx.send("Не найдено ни команды, ни кога с таким именем.")


def setup(bot):
    bot.add_cog(Basic(bot))
