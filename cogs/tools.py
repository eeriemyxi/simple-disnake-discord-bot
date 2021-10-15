import disnake
from disnake.ext import commands
import asyncio
from datetime import datetime, timedelta
import time



class Tools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def remindme(
        self,
        inter,
        day: int,
        hour: int,
        minute: float,
        reason: str = "Not specified.",
        secret: bool = False,
    ):
        """
        Reminds you at a specific time.

        Parameters
        ----------
        day: You may set it to 0 to get reminded today.
        hour: You may set it to 0 to get reminded under an hour.
        minute: You may also enter something like 0.05 to get reminded in 5 seconds.
        secret: If set to `True`, It will send an ephemeral message to indicate whether I can remind you or not.
        """
        created_at = time.time()
        seconds = round(86400 * day + 3600 * hour + 60 * minute)
        await inter.response.send_message(
            "Okay. I'll remind you <t:{}:R>.".format(
                int(
                    (
                        datetime.fromtimestamp(created_at) + timedelta(seconds=seconds)
                    ).timestamp()
                )
            ),
            ephemeral=secret,
        )
        await asyncio.sleep(seconds)
        try:
            await inter.author.send(
                f"Hello, you asked me to remind you <t:{int(created_at)}:R>. Reason: `{reason}`"
            )
        except Exception:
            await inter.channel.send(
                f"Hello <@{inter.author.id}>, I couldn't DM you so I'm reminding you here. You asked me to remind you <t:{int(created_at)}:R>. Reason: `{reason}`"
            )
        return
def setup(bot):
    bot.add_cog(Tools(bot))