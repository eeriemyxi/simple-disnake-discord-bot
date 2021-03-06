import disnake
from disnake.ext import commands
from utils.animals import Animals
from utils.cog_id import COG_ID

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category = COG_ID.IMAGES

    @commands.slash_command()
    async def animal(
        self,
        inter,
        name: str = commands.Param(
            choices={
                "Dog": "dog",
                "Cat": "cat",
                "Panda": "panda",
                "Fox": "fox",
                "Red Panda": "red_panda",
                "Koala": "koala",
                "Bird": "bird",
                "Raccoon": "raccoon",
                "Kangaroo": "kangaroo",
            }
        ),
    ):
        """
        Random images of animals. And some cool facts about them.

        Parameters
        ----------
        name: Name of the animal.
        """
        await inter.response.defer()
        animal = Animals(name)
        return await inter.edit_original_message(
            embed=disnake.Embed(
                title=name.replace("_", " ").title(),
                description=await animal.fact(),
            ).set_image(url=await animal.image())
        )


def setup(bot):
    bot.add_cog(Images(bot))
