import discord
from discord import app_commands

class GeneralCommands(app_commands.Group):
    def __init__(self, bot: discord.Client):
        super().__init__()
        self.bot = bot

    @app_commands.command(name="hello", description="Say hello to the bot")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello! I'm your Discord bot.")

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f'Pong! Latency: {latency}ms')

async def setup(bot: discord.Client):
    bot.tree.add_command(GeneralCommands(bot))