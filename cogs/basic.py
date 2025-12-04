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

    @commands.command(name="toggle")
    async def toggle(self, ctx, type_: str, name: str, state: str):

        if ctx.author.id not in self.bot.owner_ids:
            await ctx.send("Только администраторы могут использовать эту команду.")
            return

        type_ = type_.lower()
        state = state.lower()

        if type_ == "command":
            cmd = self.bot.get_command(name)
            if not cmd:
                await ctx.send(f"Команда не найдена.")
                return
            if cmd.name == "toggle":
                await ctx.send("Эту команду нельзя отключить.")
                return
            cmd.enabled = state == "on"
            await ctx.send(f"Команда {'включена' if state == 'on' else 'отключена'}.")

        elif type_ == "cog":
            if name.lower() == "basic":
                await ctx.send("Basic нельзя выгружать.")
                return
            if state == "off":
                try:
                    self.bot.unload_extension(f"cogs.{name}")
                    await ctx.send(f"`{name}` выгружен.")
                except Exception as e:
                    await ctx.send(f"Не удалось выгрузить `{name}`: {e}")
            elif state == "on":
                try:
                    self.bot.load_extension(f"cogs.{name}")
                    await ctx.send(f"`{name}` загружен.")
                except Exception as e:
                    await ctx.send(f"Не удалось загрузить `{name}`: {e}")
            else:
                await ctx.send("Доступные варианты: on/off")
        else:
            await ctx.send("Доступные варианты: `.toggle [command/cog] <имя> [on/off]`")


def setup(bot):
    bot.add_cog(Basic(bot))
