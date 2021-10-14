from typing import Text
import disnake
from disnake.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_deleted = {}

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        if ctx.author.bot is True:
            return
        self.last_deleted[ctx.channel.id] = (
            ctx.content,
            str(ctx.author),
            ctx.author.avatar.url,
            ctx.created_at.strftime("%x | %X UTC"),
        )

    @commands.command()
    async def snipe(self, ctx):
        """
        Shows the most recent deleted message.
        """
        await ctx.send(
            embed=disnake.Embed(description=message[0])
            .set_author(icon_url=message[2], name=message[1])
            .set_footer(text=message[3])
            if (message := self.last_deleted.get(ctx.channel.id))
            else "Nothing to snipe yet."
        )


def setup(bot):
    bot.add_cog(Fun(bot))
