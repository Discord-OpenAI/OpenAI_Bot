import os
import discord
from discord.ext import commands
from discord import app_commands
import openai
from openai import Completion
import asyncio
import api_key_manager
intents = discord.Intents.default()
intents.members = True
intents.dm_messages = True
intents.message_content = True
#intents.guild_permissions = True
activity = discord.Activity(name='CoCFire somehow get me to work', type=discord.ActivityType.watching)
bot = commands.Bot(intents=intents,activity=activity,command_prefix="/")
# A bit of extra larp to make it look cool
def setup(bot):
    @bot.tree.command()
    @commands.is_owner()
    async def disable(interaction: discord.Interaction):
        """Disables the bot on the current server."""
        guild_id = interaction.guild.id
        api_key_manager.set_server_api_key(guild_id, None)
        await interaction.response.send_message("Successfully disabled the bot on this server.")

    @bot.tree.command()
    @commands.is_owner()
    async def overrideapikey(interaction: discord.Interaction, api_key: str):
        """Overrides the API key for the current server."""
        guild_id = interaction.guild.id
        api_key_manager.set_server_api_key(guild_id, api_key)
        await interaction.response.send_message("Successfully overridden the API key for this server.")

    @bot.tree.command()
    @commands.is_owner()
    async def disableuser(interaction: discord.Interaction, user: discord.Member):
        """Disables the bot for the specified user."""
        user_id = str(user.id)
        if user_id in interaction.bot.disabled_users:
            interaction.bot.disabled_users.remove(user_id)
            await interaction.response.send_message(f"Successfully enabled the bot for user {user.name}.")
        else:
            interaction.bot.disabled_users.append(user_id)
            await interaction.response.send_message(f"Successfully disabled the bot for user {user.name}.")
    @bot.tree.command()
    async def override(interaction: discord.Interaction):
        await interaction.response.send_message("Successfully overridden Admin. Bot owner commands enabled.")
    @bot.tree.command()
    async def eject(interaction: discord.Interaction):
        await interaction.response.send_message("Successfully ejected owner commands")
