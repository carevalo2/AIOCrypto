import discord
import os
from discord.ext import commands
from discord.ext.commands import ExtensionNotFound, NoEntryPointError, ExtensionFailed
from dotenv import load_dotenv

load_dotenv()


class AIOCrypto(commands.Bot):

    def __init__(self, *args, **kwargs):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        command_prefix = os.getenv('COMMAND_PREFIX')

        super().__init__(
            command_prefix=command_prefix,
            intents=intents,
            *args,
            **kwargs
        )
        self.db = None

    async def load_cogs(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                cog_name = f"cogs.{filename[:-3]}"
                try:
                    await self.load_extension(cog_name)
                    print(f"Loaded cog: {cog_name}")
                except ExtensionNotFound:
                    print(f"{cog_name} could not be found.")
                except NoEntryPointError:
                    print(f"{cog_name} does not have a setup function.")
                except ExtensionFailed as e:
                    print(f"Failed to load {cog_name} because of failure: \n{e}")

    async def setup_hook(self) -> None:
        try:
            await self.load_cogs()
        except (ExtensionNotFound, ExtensionFailed, NoEntryPointError) as e:
            print(f"Error during bot startup. \n{e}")

    async def on_ready(self):
        print(f"{self.user} is logged in.")

    async def run(self):
        await self.start(os.getenv('DISCORD_TOKEN'))


