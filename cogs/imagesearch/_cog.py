import disnake
from disnake.ext import commands
from ._paginator import Paginator
from ._get_images import ImageSearch


class ImageSearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["img"])
    async def imagesearch(self, ctx, query: str):
        paginator = Paginator(ctx, embeds=await ImageSearch(ctx, query)._fetch_images())
        paginator.message = await ctx.send(
            embed=paginator.current_embed, view=paginator
        )
        await paginator.wait()
