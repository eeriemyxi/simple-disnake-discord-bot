import disnake
from disnake.ext import commands
import pkgutil
import deta
import dotenv
import os
dotenv.load_dotenv()


class DisnakeSimpleBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=">", test_guilds=[858720379069136896,808030843078836254])
        self.db_project_key = os.environ.get("DETAPROJECTKEY")
        self.server_db = deta.Deta(self.db_project_key).Base(name="serverdb")
        self.user_db = deta.Deta(self.db_project_key).Base(name="userdb")
        self.bot_db = deta.Deta(self.db_project_key).Base(name="botdb")
    async def on_ready(self):
        print("Ready!")


bot = DisnakeSimpleBot()
for cog in pkgutil.iter_modules(["cogs"]):
    bot.load_extension(f"cogs.{cog.name}")
    print("Loaded cog: {}".format(cog.name))

bot.run(os.environ.get("TOKEN"))
