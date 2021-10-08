import disnake
from disnake.ext import commands, tasks
from ._scraping import Scraping
import aiohttp
import aiofiles
import deta
import os
import asyncio
import time
from datetime import datetime
from functools import lru_cache


class Doc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scraper = Scraping(self.bot)
        self.doc_local_cache = None
    # def cog_unload(self):
    #     self.local_cache_download.cancel()
    # @commands.Cog.listener()
    # async def on_ready(self):
    #     self.local_cache_download.start()

    # @tasks.loop(hours=4)
    # async def local_cache_download(self):
    #     # temp_cache = await get_source(cache = self.doc_local_cache)
    #     # print(temp_cache)
    #     # if cache_unix := self.bot.bot_db.get("docs_cache_unix"):
    #     #     last_cache = round(
    #     #         (datetime.now() - datetime.fromtimestamp(cache_unix.get('value'))).total_seconds()
    #     #         / 3600
    #     #     )
    #     #     if last_cache > 4:
    #     #         if self.doc_local_cache == temp_cache:
    #     #             return
    #     #         self.doc_local_cache = temp_cache
    #     #         return
    #     # else:
    #     #     self.bot.bot_db.put(int(time.time()), "docs_cache_unix")
    #     #     self.doc_local_cache = temp_cache
    #     # print(self.doc_local_cache)

    # @local_cache_download.before_loop
    # async def before_local_cache_starts(self):
    #     await self.bot.wait_until_ready()

    @lru_cache(maxsize = 50)
    async def get_source(self):
        print('passed to get source')
        return 'flwfkn'
        # async with aiohttp.ClientSession() as session:
        #     async with session.get(
        #         "https://disnake.readthedocs.io/en/latest/api.html?"
        #     ) as res:
        #         return await res.text()


    @commands.command(aliases=["d", "doc"])
    async def docs(self, ctx, query: str):
        """
        Get definition from readthedocs.io
        """
        await ctx.send(
            embed=disnake.Embed(
                title="Results for {}".format(query),
                description=await self.scraper.get_def(query),
            )
        )
