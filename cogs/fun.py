from typing import Text
import disnake
from disnake.ext import commands
import datetime

from disnake.ext.commands.cog import Cog
from utils.cog_id import COG_ID
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category = COG_ID.FUN
        self.last_deleted = {}
        self.last_edited = {}
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
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot is True:
            return
        self.last_edited[before.channel.id] = (
            before.content,
            str(before.author),
            before.author.avatar.url,
            'Edited at '+before.created_at.strftime("%x | %X UTC"),
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
            else disnake.Embed(title = "Nothing to snipe yet.", description='')
        )

    @commands.command(aliases = ['esnipe'])
    async def editsnipe(self, ctx):
        """
        Shows the most recent edited message's content before it was edited.
        """
        await ctx.send(
            embed=disnake.Embed(description=message[0])
            .set_author(icon_url=message[2], name=message[1])
            .set_footer(text=message[3])
            if (message := self.last_edited.get(ctx.channel.id))
            else disnake.Embed(title = "Nothing to snipe yet.", description='')
        )
def setup(bot):
    bot.add_cog(Fun(bot))
