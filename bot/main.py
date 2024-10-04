import os
import sys
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Add the project root directory to Python's module search path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Set Up Intents and Create Bot Instance
class MyBot(commands.AutoShardedBot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents, help_command=None)

    async def setup_hook(self):
        await self.load_cogs()
        await self.tree.sync()
        print("Slash commands synced.")

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print(f'Shard ID: {self.shard_id}')
        print(f'Total Shards: {self.shard_count}')

    async def load_cogs(self):
        # Set Cog Path
        cogs_dir = os.path.join(project_root, 'cogs')

        # Load cogs from category folders
        for item in os.listdir(cogs_dir):
            item_path = os.path.join(cogs_dir, item)
            if os.path.isdir(item_path):
                for filename in os.listdir(item_path):
                    if filename.endswith('.py'):
                        cog_path = f"cogs.{item}.{filename[:-3]}"
                        await self.load_cog(cog_path)
            elif item.endswith('.py') and item != '__init__.py':
                # Load cogs directly in the cogs folder
                cog_path = f"cogs.{item[:-3]}"
                await self.load_cog(cog_path)

    async def load_cog(self, cog_path):
        try:
            await self.load_extension(cog_path)
            print(f"Loaded extension: {cog_path}")
        except Exception as e:
            print(f"Failed to load extension {cog_path}: {e}")

async def main():
    bot = MyBot()
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())