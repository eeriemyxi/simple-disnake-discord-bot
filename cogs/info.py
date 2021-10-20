import disnake
from disnake.ext import commands
from utils.cog_id import COG_ID

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category = COG_ID.INFO


def setup(bot):
    bot.add_cog(Information(bot))
