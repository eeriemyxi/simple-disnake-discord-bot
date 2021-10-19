from typing import List
import disnake
from disnake.ext import commands
from utils.paginator import Paginator
from utils.cog_id import COG_ID



class HelpCommand(commands.MinimalHelpCommand):
    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        paginator = Paginator(ctx=self.context, embeds=await self._get_embeds(mapping))
        paginator.message = await channel.send(
            embed=paginator.current_embed, view=paginator
        )

    async def _get_embeds(self, mapping) -> List[disnake.Embed]:
        embeds = {}
        embed_list = list()
        for cog, command_list in mapping.items():
            if not len(command_list) or not command_list:
                continue
            command_list = await self.filter_commands(command_list)
            for command in command_list:
                category = (
                    COG_ID.UNKNOWN
                    if command.cog is None
                    else command.cog.category
                    if hasattr(command.cog, "category")
                    else COG_ID.UNKNOWN
                )
                if category not in embeds:
                    embeds[category] = [command]
                else:
                    embeds[category].append(command)
        for cog, command_list in embeds.items():
            embed_list.append(
                disnake.Embed(
                    title=cog.value[1],
                    description="List of all commands:\n> `<>`: Means that its a required argument\n> `[]`: Means that its an optional argument\n"+"\n".join(await self.__get_command_description(command_list)),
                )
            )
        return embed_list
    async def __get_command_description(self, command_list: List[commands.Command]) -> str:
        descriptions = list()
        for command in command_list:
            # command_name = "**{}**".format(command.name)
            command_usage = ' '+command.usage if command.usage else ''
            command_description = command.short_doc
            command_str = "`{}{}`\n{}".format(command.name, command_usage, command_description)
            descriptions.append(command_str)
        return descriptions


class HelpCommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category = COG_ID.INFO
        self.bot.help_command = HelpCommand()


def setup(bot):
    bot.add_cog(HelpCommandCog(bot))
