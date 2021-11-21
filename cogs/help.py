from typing import List
import disnake
from disnake.ext import commands
from utils.paginator import Paginator
from utils.cog_id import COG_ID


class HelpCommand(commands.MinimalHelpCommand):
    async def send_bot_help(self, mapping) -> None:
        channel = self.get_destination()
        paginator = Paginator(ctx=self.context, embeds=await self._get_embeds(mapping))
        paginator.remove_button("RANDOM")
        paginator.message = await channel.send(
            embed=paginator.current_embed, view=paginator
        )

    async def send_command_help(self, command: commands.Command) -> None:
        aliases = ", ".join([f"`{i}`" for i in command.aliases])
        description = command.short_doc
        usage = (await self.__get_command_description([command]))[0].split("\n")[0]
        await self.context.send(
            embed=disnake.Embed(title=command.name)
            .add_field(name="What does it do?", value=description, inline=False)
            .add_field(name="How to use it?", value=usage, inline=False)
            .add_field(name="Aliases", value=aliases, inline=False)
        )

    async def send_cog_help(self, cog: commands.Cog) -> None:
        await self.context.send(
            embed=disnake.Embed(
                title=cog.category.value[1],
                description="List of all commands:\n> `<>`: Means that its a required argument\n> `[]`: Means that its an optional argument\n"
                + "\n".join(
                    await self.__get_command_description(
                        await self.filter_commands(cog.get_commands())
                    )
                ),
            )
        )

    def command_not_found(self, string: str) -> str:
        hint = str()
        for command in self.context.bot.commands:
            if string in command.name:
                hint: str = f"\nI think you're looking for `{command.name}`?"
        return f'Um..."{string}"? Sorry but my owner never added such command or category. :pensive:{hint}'

    async def send_error_message(self, error):
        await self.context.send(embed=disnake.Embed(title="Error!", description=error))

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
                    description=f'List of all commands:\n> `<>`: Means that its a required argument\n> `[]`: Means that its an optional argument\n'
                    + "\n".join(await self.__get_command_description(command_list)),
                )
            )
        return embed_list

    async def __get_command_description(
        self, command_list: List[commands.Command]
    ) -> str:
        descriptions = list()
        for command in command_list:
            command_usage = " " + command.usage if command.usage else ""
            command_description = command.short_doc
            command_str = f"`{command.name}{command_usage}`\n{command_description}"
            descriptions.append(command_str)
        return descriptions


class HelpCommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category = COG_ID.INFO
        self.bot.help_command = HelpCommand()


def setup(bot):
    bot.add_cog(HelpCommandCog(bot))
