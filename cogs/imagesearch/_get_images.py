import httpx
from typing import List
import disnake
from urllib.parse import urljoin, quote_plus


class ImageSearch:
    """
    Fetches the images related to the query and returns a :class:`list` of :class:`disnake.Embed`

    Parameters
    ----------
    query: :class:`str`
        Text to search
    """

    def __init__(self, ctx, query) -> str:
        self.ctx = ctx
        self.query = query

    def __fix_url(self, url) -> str:
        """
        Some URLs lack the protocol so this function add them manually.
        """
        if not url.startswith("http"):
            return urljoin("http:", url)
        return url

    async def _fetch_images(self) -> List[disnake.Embed]:
        '''
        Fetches the image data from searx.xyz
        '''
        async with httpx.AsyncClient() as client:
            source = await client.get(
                "https://searx.xyz/search?format=json&safesearch=2&categories=images&q={}".format(
                    quote_plus(self.query)
                )
            )
            json = source.json()
            embeds = list()
            for item in json["results"]:
                embeds.append(
                    disnake.Embed(title=item["title"], url=self.__fix_url(item["url"]))
                    .set_author(
                        name=str(self.ctx.author),
                        icon_url=self.ctx.author.display_avatar,
                    )
                    .set_image(url=self.__fix_url(item["img_src"]))
                )
            return embeds
