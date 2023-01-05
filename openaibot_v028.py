import os
import discord
from discord.ext import commands
from discord import app_commands
import openai
from openai import Completion
import asyncio
import api_key_manager
#import debug_logger
#import admin_commands

bot_token = ''
#debug_logger.setup_debug_logger()
intents = discord.Intents.default()
intents.members = True
intents.dm_messages = True
intents.message_content = True
#intents.guild_permissions = True
activity = discord.Activity(name='CoCFire somehow get me to work', type=discord.ActivityType.watching)
bot = commands.Bot(intents=intents,activity=activity,command_prefix="/")

# Setting up admin commands for bot owner
#admin_commands.setup(bot)

# Connecting to the Server
#@bot.event
#async def on_ready():
    # Initial message
#    await debug_logger.log_command("on_ready", "Bot initialized")

@bot.event
async def on_guild_join(guild):
    owner = guild.owner
    if owner:
        await owner.send("Thank you for adding me to your server! Please use `/setapikey` within your server to finish setup!")
#        await debug_logger.log_command("on_guild_join", f"Bot joined the guild {guild.name} ID: {guild.id}")

@bot.event
async def on_guild_remove(guild):
    # DM the guild owner to ask for feedback
    owner = guild.owner
    if owner:
        await owner.send(f"Hello! I'm sorry that I have been removed from your guild {guild.name}. "
                         "Could you please take a moment to give us some feedback on why you decided to remove the bot? "
                         "We would really appreciate it if you could let us know how we can improve. "
                         "Thank you for using our bot!")

        # Wait for the owner's response
        try:
            message = await client.wait_for('message', check=lambda message: message.author == owner, timeout=600.0)
        except asyncio.TimeoutError:
            # If the owner doesn't respond within 60 seconds, log a message
            print(f"No response from the owner of guild {guild.name}")
        else:
            # If the owner responds, write their feedback to a file
            with open(f'server_data/{guild.id}/feedback', 'w') as feedback_file:
                feedback_file.write(message.content)
#    await debug_logger.log_command("on_guild_remove", f"Bot left the guild {guild.name} ID: {guild.id}")


@bot.tree.command()
@app_commands.default_permissions(manage_guild=True)
async def setapikey(interaction: discord.Interaction, api_key: str):
    # Check if the user has the manage_guild permission
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("You do not have permission to run this command.")
#        await debug_logger.log_command("setapikey", f"user {interaction.user.name}#{interaction.user.discriminator}(ID: {interaction.user.id}) with insufficient permissions attempted to run setapikey in guild {guild.name} ID: {guild.id}")
        return

    # check if the API key is valid
    if not api_key.startswith('sk-'):
        await interaction.response.send_message("That doesn't appear to be a valid API key. Please make sure you're providing an OpenAI API key. This should start with 'sk-'.")
#        await debug_logger.log_command("setapikey", f"user {interaction.user.name}#{interaction.user.discriminator}(ID: {interaction.user.id}) attempted to run setapikey in guild {guild.name} ID: {guild.id}, but provided an invalid API key")

    else:
        guild_id = interaction.guild.id
        api_key_manager.set_server_api_key(guild_id, api_key)
        await interaction.response.send_message("Successfully set the API key for this server.")
#        await debug_logger.log_command("setapikey", f"user {interaction.user.name}#{interaction.user.discriminator}(ID: {interaction.user.id}) reset the API key in guild {guild.name} ID: {guild.id}")


@bot.tree.command()
async def direct(interaction: discord.Interaction, prompt: str):
    await interaction.response.send_message("disabled")
@bot.tree.command()
async def openai(interaction: discord.Interaction, prompt: str):
    await interaction.response.send_message("disabled")
@bot.tree.command()
async def aiprompt(interaction: discord.Interaction, prompt: str):
    api_key = await api_key_manager.get_server_api_key(interaction.guild.id)
#    openai.api_key = api_key

    max_tokens = 64
    temperature = 0.4
    completion = Completion.create(
        engine="text-davinci-003",
        prompt=prompt[3:],
        max_tokens=max_tokens,
        temperature=temperature,
        api_key=api_key
    )
    # Relaying to Discord
    debugchan = bot.get_channel(1050996354085830748)
    await interaction.response.send_message(completion["choices"][0]["text"])
    await debugchan.send(completion)

bot.run(bot_token)

