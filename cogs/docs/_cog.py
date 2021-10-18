import disnake
from disnake.ext import commands
from ._scraping import Scraping
from ._text import Text
from utils.cog_id import COG_ID
text = Text()
class Doc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category = COG_ID.INFO
        self.scraper = Scraping(self.bot)

    @commands.command(aliases=["d", "doc"])
    async def docs(self, ctx, query: str):
        """
        Get definition from readthedocs.io
        """
        await ctx.message.add_reaction("<a:loading:896334280697970748>")
        await ctx.send(
            embed=disnake.Embed(
                title="Results for {}".format(query),
                description=await self.scraper.get_def(text.fix_query(query)),
            )
        )
    @commands.slash_command(name='docs',aliases=["d", "doc"])
    async def docs_slash(self, inter, query: str = commands.Param(autocomp = text.query_choices)):
        """
        Get definition from readthedocs.io
        """
        await inter.response.defer()
        await inter.edit_original_message(
            embed=disnake.Embed(
                title="Results for {}".format(query),
                description=await self.scraper.get_def(query),
            )
        )
