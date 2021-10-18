import disnake
from disnake.ext import commands
import pkgutil


class easyembed(disnake.Embed):
    @classmethod
    def error(self, title, desc, ctx):
        id = str(ctx.author.id)
        color = (0, 0, 0)
        return self(
            title=title, description=desc, color=disnake.Color.from_rgb(*(tuple(color)))
        )

    @classmethod
    def unknown(self, ctx, user):
        id = str(ctx.author.id)
        color = (0, 0, 0)
        return self(
            title="Unknown error",
            description=f"Please report it by typing <@{user.id}> report",
            color=disnake.Color.from_rgb(*(tuple(color))),
        )

    @classmethod
    def simple(self, title, desc, ctx):
        id = str(ctx.author.id)
        color = (0, 0, 0)
        return self(
            title=title, description=desc, color=disnake.Color.from_rgb(*(tuple(color)))
        )

    @classmethod
    def getcolor(self, ctx):
        id = str(ctx.author.id)
        color = (0, 0, 0)
        return disnake.Color.from_rgb(*(tuple(color)))


class Owner(commands.Cog, name="Bot Owner", command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reload(self, ctx, name: str):
        cogs = [
            extension.name
            for extension in pkgutil.iter_modules(["cogs"])
            if extension.name != "admin_only"
        ]
        if name.lower() == "all":
            try:
                msg = await ctx.send(
                    embed=easyembed.error(f"Reloading all cogs", "", ctx)
                )
                logs = []
                log = logs.append
                for extension in cogs:
                    try:
                        self.bot.reload_extension(f"cogs.{extension}")
                    except Exception as e:
                        log(
                            f"Failed to log cog {str(extension).capitalize()}. Error:\n{e}"
                        )
                    else:
                        log(f"Reloaded cog: {str(extension).capitalize()}")
            except Exception:
                await msg.edit(embed=easyembed.error("Couldn't reload", "", ctx))
            else:
                await msg.edit(
                    embed=easyembed.simple(
                        "Reloaded all cogs. Logs:", "\n".join(logs), ctx
                    )
                )
                return
        for num, extension in enumerate(cogs):
            if extension.startswith(name):
                try:
                    msg = await ctx.send(
                        embed=easyembed.error(
                            f'Reloading cog "{extension.capitalize()}"', "", ctx
                        )
                    )
                    self.bot.reload_extension(f"cogs.{extension}")
                except Exception:
                    await msg.edit(embed=easyembed.error("Couldn't reload", "", ctx))
                    return
                else:
                    await msg.edit(
                        embed=easyembed.error(
                            f'Cog "{extension.capitalize()}" reloaded.', "", ctx
                        )
                    )
                    return
            else:
                if num == (len(cogs) - 1):
                    await ctx.send(embed=easyembed.simple("Not found", "", ctx))
                    return

    @commands.command()
    async def load(self, ctx, name: str):
        cogs = [
            extension.name
            for extension in pkgutil.iter_modules(["cogs"])
            if extension.name != "admin_only"
        ]
        for num, extension in enumerate(cogs):
            if extension.startswith(name):
                try:
                    msg = await ctx.send(
                        embed=easyembed.error(
                            f'Loading cog "{extension.capitalize()}"', "", ctx
                        )
                    )
                    self.bot.load_extension(f"cogs.{extension}")
                except Exception as err:
                    await msg.edit(
                        embed=easyembed.error(
                            "Either it's already loaded or I couldn't load it.", "", ctx
                        )
                    )
                    return
                else:
                    await msg.edit(
                        embed=easyembed.error(
                            f'Cog "{extension.capitalize()}" loaded.', "", ctx
                        )
                    )
                    return
            else:
                if num == (len(cogs) - 1):
                    await ctx.send(embed=easyembed.simple("Not found", "", ctx))
                    return

    @commands.command()
    async def unload(self, ctx, name: str):
        cogs = [
            extension.name
            for extension in pkgutil.iter_modules(["cogs"])
            if extension.name != "admin_only"
        ]
        for num, extension in enumerate(cogs):
            if extension.startswith(name):
                try:
                    msg = await ctx.send(
                        embed=easyembed.error(
                            f'Unloading cog "{extension.capitalize()}"', "", ctx
                        )
                    )
                    self.bot.unload_extension(f"cogs.{extension}")
                except Exception as err:
                    await msg.edit(
                        embed=easyembed.error(
                            "Either it's not loaded yet or I couldn't unload it.",
                            "",
                            ctx,
                        )
                    )
                    return
                else:
                    await msg.edit(
                        embed=easyembed.error(
                            f'Cog "{extension.capitalize()}" unloaded.', "", ctx
                        )
                    )
                    return
            else:
                if num == (len(cogs) - 1):
                    await ctx.send(embed=easyembed.simple("Not found", "", ctx))
                    return


def setup(bot):
    bot.add_cog(Owner(bot))
