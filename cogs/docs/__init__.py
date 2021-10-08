from ._cog import Doc
# from ._scraping import Scraping

def setup(bot):
    bot.add_cog(Doc(bot))