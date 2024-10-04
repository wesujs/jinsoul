import discord
from discord.ext import commands
from discord import app_commands

class GeneralCog(app_commands.Group):
    def __init__(self, bot: discord.Client):
        super().__init__()
        self.bot = bot

    @commands.command(name="hello", description="Say hello to the bot")
    async def hello(self, ctx):
        try:
            await ctx.send("Hello! I'm your Discord bot.")
        except Exception as e:
            await ctx.send(f"An error occured trying to say hello back: {str(e)}")

    @commands.command(name="ping", description="Check for current latency")
    async def ping(self, ctx):
        try:
            latency = round(self.bot.latency * 1000)
            await ctx.send(f'Pong! Latency: {latency}ms')
        except Exception as e:
            await ctx.send(f"An error occured attempting to grab ping: {str(e)}")

async def setup(bot):
    bot.tree.add_command(GeneralCog(bot))