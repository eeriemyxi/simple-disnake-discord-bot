import disnake
from disnake.ext import commands


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info_command(self, ctx):
        await ctx.send("hello this is from info cog")


def setup(bot):
    bot.add_cog(Info(bot))
