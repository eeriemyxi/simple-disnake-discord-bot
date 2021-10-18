import disnake
from disnake.ext import commands
from utils.paginator import Paginator
from ._get_images import ImageSearch
from utils.cog_id import COG_ID


class ImageSearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category = COG_ID.IMAGES

    @commands.command(aliases=["img", "image"])
    async def imagesearch(self, ctx, query: str):
        embeds = await ImageSearch(ctx, query)._fetch_images()
        if len(embeds) > 1:
            paginator = Paginator(ctx, embeds=embeds)
            paginator.message = await ctx.send(
                embed=paginator.current_embed, view=paginator
            )
            await paginator.wait()
            return
        return await ctx.send(
            embed=disnake.Embed(title="No images found.", description="")
        )
