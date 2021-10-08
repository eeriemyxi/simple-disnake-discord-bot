import aiohttp
from ._markdown import DocMarkdownConverter
from ._caching import DocsCaching
from bs4 import BeautifulSoup
from contextlib import suppress
import aiohttp
import aiofiles
from functools import lru_cache
class Scraping:
    def __init__(self, bot):
        self.bot = bot
        self.cacher = DocsCaching()

    @lru_cache(maxsize = 50)
    async def get_source(self):
        print('passed to get source')
        return 'flwfkn'
        # async with aiohttp.ClientSession() as session:
        #     async with session.get(
        #         "https://disnake.readthedocs.io/en/latest/api.html?"
        #     ) as res:
        #         return await res.text()

    async def _scraper(source, query):
        soup = BeautifulSoup(source, "html.parser")
        search_list = soup.find("dt", attrs={"id": query})
        codeblock = search_list.parent.find("dt")
        markdown = DocMarkdownConverter(
            page_url="https://disnake.readthedocs.io/en/master/api.html?"
        ).convert
        desc = "\n".join(
            [
                markdown(str(i))
                for i in search_list.parent.find("dd").find_all("p", recursive=False)
            ]
        )
        return "```py\n{}```\n\n{}".format(codeblock.text.replace("Â¶", ""), desc)

    async def get_def(self, query):
        try:
            source = self.cacher.get_cache(query)
        except ValueError:
            source = self.bot.doc_local_cache
        return await self._scraper(source, query)


# def scrapper(query):
#     source = requests.get('https://discordpy.readthedocs.io/en/master/api.html').text
#     soup = BeautifulSoup(source, 'html.parser')
#     search_list = soup.find('dt', attrs = {'id':query})
#     codeblock = search_list.parent.find('dt')
#     markdown = DocMarkdownConverter(page_url='https://disnake.readthedocs.io/en/master/api.html?').convert
#     desc_h = '\n'.join([markdown(str(i)) for i in search_list.parent.find('dd').find_all('p',recursive=False)])
#     return "```py\n{}```\n\n{}".format(codeblock.text.replace('Â¶', ''), desc_h)
