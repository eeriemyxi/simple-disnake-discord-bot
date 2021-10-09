import aiohttp
from ._markdown import DocMarkdownConverter
from ._caching import DocsCaching
from bs4 import BeautifulSoup
import aiohttp
from cache import AsyncLRU


class Scraping:
    def __init__(self, bot):
        self.bot = bot
        self.cacher = DocsCaching()

    @AsyncLRU(maxsize=50)
    async def get_source(self, idk = ''):

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://disnake.readthedocs.io/en/latest/api.html?"
            ) as res:
                return await res.text(encoding="utf8")

    async def _scraper(self, source, query):
        soup = BeautifulSoup(source, "html.parser")
        search_list = soup.find("dt", attrs={"id": query})
        if search_list is None:
            return (404, "No definition was found for {}".format(query))
        codeblock = search_list.parent.find("dt")
        markdown = DocMarkdownConverter(
            page_url="https://disnake.readthedocs.io/en/latest/api.html?"
        ).convert
        desc = "\n".join(
            [
                markdown(str(i))
                for i in search_list.parent.find("dd").find_all("p", recursive=False)
            ]
        )
        operations = search_list.parent.find('div', attrs = {'class':'operations docutils container'})
        operations = 'Supported operations:\n'+operations.text if operations else ''
        return (200, "```py\n{}```\n\n{}\n{}".format(codeblock.text.replace("¶", ""), desc, operations))


    async def get_def(self, query):
        try:
            desc = self.cacher.get_cache(query)
        except ValueError:
            source = await self.get_source()
            desc = await self._scraper(source, query)
        finally:
            if desc[0] == 200:
                self.cacher.cache(query, desc, True)
            return desc[1]
