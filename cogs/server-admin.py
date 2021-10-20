from disnake.ext import commands
import disnake
from utils.cog_id import COG_ID

class ServerAdmin(commands.Cog, name='Admin only'):
    def __init__(self, bot):
        self.bot = bot
        self.category = COG_ID.ADMIN
    @commands.command(description="Kick a server member.", usage="<USER> [REASON]")
    @commands.has_guild_permissions(administrator = True)
    async def kick(self, ctx, user: disnake.Member, *, reason=None):
        reason = "{kicked_user} was kicked by {mod}. Reason: {reason}".format(
            kicked_user=user, mod=ctx.author, reason=reason or "Not specified"
        )
        await user.kick(reason=reason)
        await ctx.send("{} was kicked by {}".format(user, ctx.author))

    @commands.slash_command(
        description="Kick a server member.", usage="<USER> [REASON]"
    )
    @commands.has_guild_permissions(administrator = True)
    async def kick(self, ctx, user: disnake.Member, *, reason=None):
        reason = "{kicked_user} was kicked by {mod}. Reason: {reason}".format(
            kicked_user=user, mod=ctx.author, reason=reason or "Not specified"
        )
        await user.kick(reason=reason)
        await ctx.response.send_message(
            "{} was kicked by {}".format(user, ctx.author)
        )
    @commands.command(
        description="Ban a server member. The `DELETE_MESSAGE_DAYS` parameter is used to specify the number of days worth of messages to delete sent by the banned user. It should range between 0 to 7 and defaults to 7 if not specified. ",
        usage="<USER> [DELETE_MESSAGE_DAYS] [REASON]",
    )
    @commands.has_guild_permissions(administrator = True)
    async def ban(
        self, ctx, user: disnake.Member, delete_message_days=7, *, reason=None
    ):
        reason = "{banned_user} by banned by {mod} and {days} days worth of messages were deleted. Reason: {reason}".format(
            banned_user=user,
            mod=ctx.author,
            days=delete_message_days,
            reason=reason or "Not specified",
        )
        await user.ban(reason=reason, delete_message_days=delete_message_days)
        await ctx.send("{} was banned by {}".format(str(user), str(ctx.author)))

    @commands.slash_command(
        description="Ban a server member.",
        usage="<USER> <DELETE_MESSAGE_DAYS> [REASON]",
    )
    @commands.has_guild_permissions(administrator = True)
    async def ban(
        self,
        ctx,
        user: disnake.Member,
        delete_message_days: int = commands.Param(
            choices={str(i): i for i in range(0, 8)}
        ),
        *,
        reason=None
    ):
        reason = "{banned_user} by banned by {mod} and {days} days worth of messages were deleted. Reason: {reason}".format(
            banned_user=user,
            mod=ctx.author,
            days=delete_message_days,
            reason=reason or "Not specified",
        )
        await user.ban(reason=reason, delete_message_days=delete_message_days)
        await ctx.response.send_message(
            "{} was banned by {}".format(str(user), str(ctx.author))
        )

    print("reminder: you have not completed the mute command yet")

    @commands.command(
        description="Mute a server member.", usage="<USER> <TIME><m | h | min | hour>"
    )
    @commands.has_guild_permissions(administrator = True)
    async def mute(self, ctx, user: disnake.Member, *, reason=None):
        "Later"


def setup(bot):
    bot.add_cog(ServerAdmin(bot))