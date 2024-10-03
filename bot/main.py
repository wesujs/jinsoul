import os
import asyncio
import sys
from dotenv import load_dotenv
import discord
from discord import app_commands

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot instance
class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.load_extension("cogs.general_commands")
        await self.tree.sync()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def load_extension(self, name):
        await asyncio.to_thread(__import__, name)
        setup = getattr(sys.modules[name], 'setup')
        await setup(self)

bot = MyBot()

# Run the bot
async def main():
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())