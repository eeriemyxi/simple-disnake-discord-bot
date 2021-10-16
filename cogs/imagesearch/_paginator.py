import disnake
from collections import namedtuple
import random


class Paginator(disnake.ui.View):
    """
    This is the paginator. Currently used to paginate the image search results.
    """

    def __init__(self, ctx, embeds):
        super().__init__(timeout=80.0)
        self.ctx = ctx
        self.message = str()
        self.embeds = embeds
        self.pages = len(self.embeds)
        self.current_page = 0
        self.btn_id = namedtuple("ID", ("NEXT", "BACK", "CANCEL", "RANDOM", "DELETE"))(
            "N", "B", "C", "R", "D"
        )
        self.confirmation = None
    
    @property
    def current_embed(self):
        return self.embeds[self.current_page].set_footer(
            text="Page {} of {}".format(self.current_page + 1, self.pages)
        )

    def current_page_set(self, cmd: str = "next", value: int = None):
        """
        Sets the current page.

        Parameters
        ----------
        cmd: :class:`str`
            "random": It will pick a number between 0 and :variable:`self.pages`.
            "next": It will increase the current page number by one.
            "back": It will decrese the current page number by one.
        value: :class:`int`
            If not None, It will set :variable:`self.current_page` to :variable:`value`.
        """

        if value is not None:
            self.current_page = value
            return
        assert cmd in (
            "next",
            "random",
            "back",
        ), "Parameter `cmd` must be any of these: ['next', 'random', 'back']"
        if cmd == "next":
            self.current_page = (
                self.current_page + 1
                if self.current_page < (self.pages - 1)
                else (self.pages - 1)
            )
            return
        if cmd == "random":
            self.current_page = random.randint(0, self.pages - 1)
            return
        self.current_page = self.current_page - 1 if self.current_page > 0 else 0
        return

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        return interaction.author.id == self.ctx.author.id

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.message.edit(embed=self.current_embed, view=self)

    @disnake.ui.button(label="Back", emoji="◀️", style=disnake.ButtonStyle.green)
    async def back_button(self, button, inter):
        self.value = self.btn_id.BACK
        self.current_page_set("back")
        await self.message.edit(embed=self.current_embed)

    @disnake.ui.button(label="Random", emoji="🔢", style=disnake.ButtonStyle.blurple)
    async def random_button(self, button, inter):
        self.value = self.btn_id.RANDOM
        self.current_page_set("random")
        await self.message.edit(embed=self.current_embed)

    @disnake.ui.button(label="Next", emoji="▶️", style=disnake.ButtonStyle.green)
    async def next_button(self, button, inter):
        self.value = self.btn_id.NEXT
        self.current_page_set("next")
        await self.message.edit(embed=self.current_embed)

    @disnake.ui.button(label="Cancel", emoji="❌", style=disnake.ButtonStyle.red)
    async def cancel_button(self, button, inter):
        self.value = self.btn_id.CANCEL
        for item in self.children:
            item.disabled = True
        await self.message.edit(embed=self.current_embed, view=self)
        self.stop()

    @disnake.ui.button(label="Delete", emoji="🗑️", style=disnake.ButtonStyle.red)
    async def delete_button(self, button, inter):
        self.value = self.btn_id.DELETE
        await self.message.delete()
        self.stop()
