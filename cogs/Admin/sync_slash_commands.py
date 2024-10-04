import discord
from discord.ext import commands
from discord import app_commands


class SyncSlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sync", description="Sync slash commands (Owner only)", hidden=True)
    @commands.is_owner()
    async def sync(self, ctx):
        """Syncs the slash commands to Discord"""
        try:
            synced = await self.bot.tree.sync()
            await ctx.send(f"Synced {len(synced)} commands.")
        except Exception as e:
            await ctx.send(f"An error occurred while syncing commands: {str(e)}")

    @app_commands.command(name="sync", description="Sync slash commands (Owner only)")
    @app_commands.default_permissions(administrator=True)
    async def slash_sync(self, interaction: discord.Interaction):
        if not await self.bot.is_owner(interaction.user):
            await interaction.response.send_message("Only the bot owner can use this command.", ephemeral=True)
            return
        try:
            synced = await self.bot.tree.sync()
            await interaction.response.send_message(f"Synced {len(synced)} commands.")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred while syncing commands: {str(e)}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(SyncSlashCommands(bot))