import disnake
from disnake.ext import commands

LANGUAGES = ["python", "javascript", "typescript", "java", "rust", "lisp", "elixir"]
def autocomp(inter, x):
    return [lang for lang in LANGUAGES if x.lower() in lang]
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command()
    async def autocomplete(self, inter, choice: str = commands.Param(autocomp = lambda inter, x: [lang for lang in LANGUAGES if x.lower() in lang])):
        """
        Auto complete test
        
        Parameters
        ----------
        choice: It should show you some stuff when you type
        """
        inter.response.send_message('Hello world!')
    
def setup(bot):
    bot.add_cog(Fun(bot))