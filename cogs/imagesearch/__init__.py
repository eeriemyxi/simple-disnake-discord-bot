from ._cog import ImageSearchCog

def setup(bot):
    bot.add_cog(ImageSearchCog(bot))