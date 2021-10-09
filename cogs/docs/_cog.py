import disnake
from disnake.ext import commands
from ._scraping import Scraping
from ._autocomplete import autocomeplete

class Doc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
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
                description=await self.scraper.get_def(query),
            )
        )
    @commands.slash_command(name='docs',aliases=["d", "doc"])
    async def docs_slash(self, inter, query: str = commands.Param(autocomp = autocomeplete)):
        """
        Get definition from readthedocs.io
        """
        msg = await inter.response.defer()
        # await ctx.message.add_reaction("<a:loading:896334280697970748>")
        await inter.edit_original_message(
            embed=disnake.Embed(
                title="Results for {}".format(query),
                description=await self.scraper.get_def(query),
            )
        )
