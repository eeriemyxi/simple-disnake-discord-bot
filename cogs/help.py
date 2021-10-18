import disnake
from disnake.ext import commands
from utils.paginator import Paginator
from utils.cog_id import COG_ID



class HelpCommand(commands.MinimalHelpCommand):
    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        paginator = Paginator(ctx=self.context, embeds=await self.get_embeds(mapping))
        paginator.message = await channel.send(
            embed=paginator.current_embed, view=paginator
        )

    async def get_embeds(self, mapping):
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
                    description="\n".join(i.name for i in command_list),
                )
            )
        return embed_list


class HelpCommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category = COG_ID.INFO
        self.bot.help_command = HelpCommand()


def setup(bot):
    bot.add_cog(HelpCommandCog(bot))