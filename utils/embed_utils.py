import discord
from bot.config import *
from datetime import datetime


class EmbedUtils:
    @staticmethod
    def create_embed(title, description, color=config.get_embed_color(), fields=None, footer=None, thumbnail=None,
                     image=None, author=None):
        """
        Create a Discord embed with customizable fields.

        :param title: Embed title
        :param description: Embed description
        :param color: Embed color (default: discord.Color.blue())
        :param fields: List of tuples (name, value, inline) for fields
        :param footer: Footer text or tuple (text, icon_url)
        :param thumbnail: URL for thumbnail image
        :param image: URL for main image
        :param author: Tuple (name, url, icon_url) for author
        :return: discord.Embed object
        """
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.utcnow()
        )

        if fields:
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)

        if footer:
            if isinstance(footer, tuple):
                embed.set_footer(text=footer[0], icon_url=footer[1])
            else:
                embed.set_footer(text=footer)

        if thumbnail:
            embed.set_thumbnail(url=thumbnail)

        if image:
            embed.set_image(url=image)

        if author:
            embed.set_author(name=author[0], url=author[1] if len(author) > 1 else discord.Embed.Empty,
                             icon_url=author[2] if len(author) > 2 else discord.Embed.Empty)

        return embed

    @staticmethod
    def create_error_embed(error_message):
        """Create a standardized error embed."""
        return EmbedUtils.create_embed("Error", error_message, color=discord.Color.red())

    @staticmethod
    def create_success_embed(success_message):
        """Create a standardized success embed."""
        return EmbedUtils.create_embed("Success", success_message, color=discord.Color.green())