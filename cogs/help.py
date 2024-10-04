import discord
from discord import app_commands
from discord.ext import commands
from bot.config import config
from utils.embed_utils import EmbedUtils
import math
import os
import re
import logging
import textwrap

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CategorySelect(discord.ui.Select):
    def __init__(self, cog):
        self.cog = cog
        options = [
            discord.SelectOption(label=category, description=f"Commands in {category} category")
            for category in cog.get_categories()
        ]
        options.insert(0, discord.SelectOption(label="Main Menu", description="Return to main help menu"))
        super().__init__(placeholder="Select a category", options=options)

    async def callback(self, interaction: discord.Interaction):
        try:
            if self.values[0] == "Main Menu":
                await self.cog.send_main_help_menu(interaction)
            else:
                await self.cog.send_category_help(interaction, self.values[0])
        except Exception as e:
            logger.error(f"Error in CategorySelect callback: {e}", exc_info=True)
            await interaction.response.send_message("An error occurred. Please try again later.", ephemeral=True)


class HelpView(discord.ui.View):
    def __init__(self, cog):
        super().__init__()
        self.add_item(CategorySelect(cog))


class PaginationView(discord.ui.View):
    def __init__(self, cog, category, pages, timeout=180):
        super().__init__(timeout=timeout)
        self.cog = cog
        self.category = category
        self.pages = pages
        self.current_page = 0

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.gray)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page - 1) % len(self.pages)
        await self.update_message(interaction)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.gray)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page + 1) % len(self.pages)
        await self.update_message(interaction)

    @discord.ui.button(label="Main Menu", style=discord.ButtonStyle.blurple)
    async def main_menu_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.send_main_help_menu(interaction)

    async def update_message(self, interaction: discord.Interaction):
        try:
            await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)
        except Exception as e:
            logger.error(f"Error updating message in PaginationView: {e}", exc_info=True)
            await interaction.response.send_message("An error occurred. Please try again later.", ephemeral=True)


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cogs_dir = os.path.dirname(__file__)

    def get_categories(self):
        return [folder for folder in os.listdir(self.cogs_dir)
                if os.path.isdir(os.path.join(self.cogs_dir, folder)) and folder != '__pycache__']

    def get_commands_in_category(self, category):
        commands = []
        category_path = os.path.join(self.cogs_dir, category)
        for filename in os.listdir(category_path):
            if filename.endswith('.py'):
                file_path = os.path.join(category_path, filename)
                try:
                    with open(file_path, 'r') as file:
                        content = file.read()
                        # Find all command definitions
                        command_matches = re.finditer(
                            r'(@commands\.command\((.*?)\)|@app_commands\.command\((.*?)\))\s*?\n\s*?async def (\w+)\((.*?)\):\s*?\n\s*?([\'"].*?[\'"])?',
                            content, re.DOTALL)

                        for match in command_matches:
                            decorator = match.group(1)
                            cmd_info = match.group(2) or match.group(3)
                            func_name = match.group(4)
                            docstring = match.group(6)

                            # Determine command type
                            cmd_type = "Slash Command" if "app_commands.command" in decorator else "Prefix Command"

                            # Extract name from decorator
                            name_match = re.search(r'name\s*=\s*["\'](\w+)["\']', cmd_info)
                            name = name_match.group(1) if name_match else func_name

                            # Extract description
                            desc_match = re.search(r'description\s*=\s*["\'](.+?)["\']', cmd_info)
                            description = desc_match.group(1) if desc_match else None

                            # If no description in decorator, use docstring
                            if not description and docstring:
                                description = docstring.strip('\'\"')

                            # Default description if none found
                            description = description or "No description available."

                            # Check if command is hidden
                            if 'hidden=True' not in cmd_info:
                                commands.append((name, description, cmd_type))

                except Exception as e:
                    logger.error(f"Error parsing file {file_path}: {e}", exc_info=True)
        return commands

    @app_commands.command(name='help', description='Shows All Commands')
    async def slash_help(self, interaction: discord.Interaction):
        await self.send_main_help_menu(interaction)

    @commands.command(name="help", aliases=['h'], description='Shows All Commands')
    async def prefix_help(self, ctx):
        await self.send_main_help_menu(ctx)

    async def send_main_help_menu(self, ctx):
        try:
            categories = self.get_categories()
            embed = EmbedUtils.create_embed(
                title=f"{self.bot.user.name}'s Help Menu",
                description=textwrap.shorten(self.bot.description or "No description available.", width=2048,
                                             placeholder="..."),
                color=config.get_embed_color(),
                fields=[("Categories", "\n".join(categories), False)],
                footer="Use the dropdown to navigate between categories"
            )

            view = HelpView(self)

            if isinstance(ctx, discord.Interaction):
                if ctx.response.is_done():
                    await ctx.edit_original_response(embed=embed, view=view)
                else:
                    await ctx.response.send_message(embed=embed, view=view)
            else:
                await ctx.send(embed=embed, view=view)
        except Exception as e:
            logger.error(f"Error in send_main_help_menu: {e}", exc_info=True)
            error_message = "An error occurred while fetching the help menu. Please try again later."
            if isinstance(ctx, discord.Interaction):
                await ctx.response.send_message(error_message, ephemeral=True)
            else:
                await ctx.send(error_message)

    async def send_category_help(self, interaction: discord.Interaction, category: str):
        try:
            commands = self.get_commands_in_category(category)
            if not commands:
                await interaction.response.send_message(f"No commands found in the {category} category.",
                                                        ephemeral=True)
                return

            pages = []
            items_per_page = 3  # Reduced to allow for longer descriptions
            for i in range(0, len(commands), items_per_page):
                page_commands = commands[i:i + items_per_page]
                embed = EmbedUtils.create_embed(
                    title=f"{category} Commands",
                    description=f"Page {len(pages) + 1}/{math.ceil(len(commands) / items_per_page)}",
                    color=config.get_embed_color(),
                    footer=f"Use {self.bot.command_prefix}help <command> for more info on a specific command."
                )

                for name, description, cmd_type in page_commands:
                    embed.add_field(name=f"{name} ({cmd_type})",
                                    value=textwrap.shorten(description, width=1024, placeholder="..."), inline=False)

                pages.append(embed)

            view = PaginationView(self, category, pages)
            await interaction.response.edit_message(embed=pages[0], view=view)
        except Exception as e:
            logger.error(f"Error in send_category_help: {e}", exc_info=True)
            await interaction.response.send_message(
                "An error occurred while fetching category help. Please try again later.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(HelpCog(bot))