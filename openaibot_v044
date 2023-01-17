# openaibot_v044.py
# Made by CoCFire#1111

# Importing first libraries
import os
import datetime
import json
import asyncio

# Importing Discord and OpenAI
import discord
from discord.ext import commands
from discord import app_commands
from discord import Embed
import openai
from openai import Completion

# Importing custom modules
import api_key_manager
import chatgpttest
import debug_logger
from analytics import *

# Setting up bot intents
intents = discord.Intents.default()
intents.members = True
intents.dm_messages = True
intents.message_content = True
activity = discord.Activity(name='New stuff being added', type=discord.ActivityType.watching)
bot = commands.Bot(intents=intents,activity=activity,command_prefix="/")

async def analytics_loop():
    while True:
        await analytics(bot)
        await debug_logger.log_command("analytics_loop", "recording analytics automatically")
        await asyncio.sleep(1800)

# Setting up the API key dictionary
api_keys = {}

#  Setting up commands defined in the command_setup.py module
chatgpttest.setup(bot)

# Starting the analytics loop
@bot.event
async def on_ready():
    loop = asyncio.get_event_loop()
    loop.create_task(analytics_loop())


# Defining on_guild_join and on_guild_remove functions
@bot.event
async def on_guild_join(guild):
    guild_id = guild.id
    # Creating data folder for guild
    if not os.path.exists(f'server_data/{guild_id}'):
        os.makedirs(f'server_data/{guild_id}')
    owner = guild.owner
    # DMing owner of guild
    if owner:
        await owner.send("Thank you for adding me to your server! Please use `/setapikey` within your server to finish setup!")
    # Log
    await debug_logger.log_command("on_guild_join", f"bot joined guild {guild.name}")
@bot.event
async def on_guild_remove(guild):
    owner = guild.owner
    # Asking for feedback from owner
    if owner:
        await owner.send(f"Hello! I'm sorry that I have been removed from your guild {guild.name}. \n"
                         "Could you please take a moment to give us some feedback on why you decided to remove the bot? \n"
                         "We would really appreciate it if you could let us know how we can improve. \n"
                         "Thank you for using our bot!")

        try:
            message = await bot.wait_for('message', check=lambda message: message.author == owner, timeout=600.0)
        except asyncio.TimeoutError:
            print(f"No response from the owner of guild {guild.name}")
        else:
            # If the owner responds, write their feedback to a file
            with open(f'server_data/{guild.id}/feedback.json', 'w+') as feedback_file:
                feedback_file.write(message.content)
    await debug_logger.log_command("on_guild_remove", f"bot left guild {guild.name}")

@bot.tree.command()
async def run_analytics(interaction: discord.Interaction):
    name = 'run_analytics'
    # Making it only able to be run by bot owner
    if interaction.user.id != 1000729109720219778:
        embed = discord.Embed(title="Insufficient permissions", description="\n", color=discord.Color.blurple())
        embed.add_field(name="", value="You do not have sufficient permissions to run this command.\n\n", inline=False)
        embed.add_field(name="",value="| . [Invite me!](https://discord.com/api/oauth2/authorize?client_id=1049897532404273243&permissions=395137338384&scope=bot%20applications.commands) . | . [Support](https://discord.gg/FWGDqwJ5F8) . | . [GitHub](https://github.com/Discord-OpenAI/OpenAI_Bot) . | . [Sub for a cookie ;)](https://youtube.com/@CoCFire?sub_confirmation=1) . |", inline=False)
        await interaction.response.send_message(embed=embed)
        await debug_logger.log_command("run_analytics", f"user {interaction.user.name}#{interaction.user.discriminator} attepted to use command run_analytics with insuficcient permissions in guild {interaction.guild.name} {interaction.guild.id}")
        return

    # Run the analytics function
    await interaction.response.send_message("Recording analytics for all guilds")
    await analytics(bot)
    await debug_logger.log_command("run_analytics", "successfully recorded analytics")
    await log_use(name)

# Defining setapikey function
@bot.tree.command()
@app_commands.default_permissions(manage_guild=True)
async def setapikey(interaction: discord.Interaction, api_key: str):
    name = 'setapikey'
    # Only allowing it to be run by people with manage_guild permission
    if not interaction.user.guild_permissions.manage_guild:
        embed = discord.Embed(title="Insufficient permissions", description="\n", color=discord.Color.blurple())
        embed.add_field(name="", value="You do not have sufficient permissions to run this command.\n\n", inline=False)
        embed.add_field(name="",value="| . [Invite me!](https://discord.com/api/oauth2/authorize?client_id=1049897532404273243&permissions=395137338384&scope=bot%20applications.commands) . | . [Support](https://discord.gg/FWGDqwJ5F8) . | . [GitHub](https://github.com/Discord-OpenAI/OpenAI_Bot) . | . [Sub for a cookie ;)](https://youtube.com/@CoCFire?sub_confirmation=1) . |", inline=False)
        await interaction.response.send_message(embed=embed)
        # Logging insufficient permissions event
        await debug_logger.log_command("setapikey", f"user {interaction.user.name}#{interaction.user.discriminator} attepted to use command setapikey with insuficcient permissions in guild {interaction.guild.name} {interaction.guild.id}")
        return
    if not api_key.startswith('sk-'):
        embed = discord.Embed(title="Invalid API key", description="\n", color=discord.Color.blurple())
        embed.add_field(name="", value="That doesn't appear to be a valid API key. Please make sure you're providing an OpenAI API key. This should start with 'sk-'.\n\n", inline=False)
        embed.add_field(name="",value="| . [Invite me!](https://discord.com/api/oauth2/authorize?client_id=1049897532404273243&permissions=395137338384&scope=bot%20applications.commands) . | . [Support](https://discord.gg/FWGDqwJ5F8) . | . [GitHub](https://github.com/Discord-OpenAI/OpenAI_Bot) . | . [Sub for a cookie ;)](https://youtube.com/@CoCFire?sub_confirmation=1) . |", inline=False)
        await interaction.response.send_message(embed=embed)
        await debug_logger.log_command("setapikey", f"user {interaction.user.name}#{interaction.user.discriminator} provided an invalid api key when running setapikey in guild {interaction.guild.name} {interaction.guild.id}")
    else:
        guild_id = interaction.guild.id
        api_key_manager.set_server_api_key(guild_id, api_key)
        mbed = discord.Embed(title="API key set", description="\n", color=discord.Color.blurple())
        embed.add_field(name="", value="Successfully set the API key for this server.\n\n", inline=False)
        embed.add_field(name="",value="| . [Invite me!](https://discord.com/api/oauth2/authorize?client_id=1049897532404273243&permissions=395137338384&scope=bot%20applications.commands) . | . [Support](https://discord.gg/FWGDqwJ5F8) . | . [GitHub](https://github.com/Discord-OpenAI/OpenAI_Bot) . | . [Sub for a cookie ;)](https://youtube.com/@CoCFire?sub_confirmation=1) . |", inline=False)
        await interaction.response.send_message(embed=embed)
        await debug_logger.log_command("setapikey", f"user {interaction.user.name}#{interaction.user.discriminator} set the api key for guild {interaction.guild.name} {interaction.guild.id}")
        await log_use(name)

@bot.tree.command()
async def aiprompt(interaction: discord.Interaction, prompt: str):
    name = 'aiprompt'
    guild_id = interaction.guild.id
    if guild_id not in api_keys:
        if not os.path.exists(f'server_data/{guild_id}/api_key.json'):
            embed = discord.Embed(title="No API key", description="\n", color=discord.Color.blurple())
            embed.add_field(name="", value="There is no API key set for this guild. Please ask an admin to set one with /setapikey, or contact CoCFire#1111 for help.\n\n", inline=False)
            embed.add_field(name="",value="| . [Invite me!](https://discord.com/api/oauth2/authorize?client_id=1049897532404273243&permissions=395137338384&scope=bot%20applications.commands) . | . [Support](https://discord.gg/FWGDqwJ5F8) . | . [GitHub](https://github.com/Discord-OpenAI/OpenAI_Bot) . | . [Sub for a cookie ;)](https://youtube.com/@CoCFire?sub_confirmation=1) . |", inline=False)
            await interaction.response.send_message(embed=embed)
            await debug_logger.log_command("aiprompt", f"user {interaction.user.name}#{interaction.user.discriminator} used aiprompt in guild {interaction.guild.name} {interaction.guild.id} with invalid API key set.")
        else:
            api_keys[guild_id] = await api_key_manager.get_server_api_key(guild_id)
            if not api_keys[guild_id].startswith('sk-'):
                await interaction.response.send_message("The API key set for this guild seems to be invalid. Please ask an admin to reset it using /setapikey, or contact CoCFire#1111 for help")
                await debug_logger.log_command("aiprompt", f"user {interaction.user.name}#{interaction.user.discriminator} used aiprompt in guild {interaction.guild.name} {interaction.guild.id} with invalid API key set.")
            else:
                embed = discord.Embed(title="", description="This is the first time `/aiprompt` has been used in this server since bot restart. The API key has been retrieved.", color=discord.Color.blurple())
                embed.add_field(name="", value="Please use `/help` for more info.\n\n", inline=False)
                embed.add_field(name="",value="| . [Invite me!](https://discord.com/api/oauth2/authorize?client_id=1049897532404273243&permissions=395137338384&scope=bot%20applications.commands) . | . [Support](https://discord.gg/FWGDqwJ5F8) . | . [GitHub](https://github.com/Discord-OpenAI/OpenAI_Bot) . | . [Sub for a cookie ;)](https://youtube.com/@CoCFire?sub_confirmation=1) . |", inline=False)
                await interaction.response.send_message(embed=embed)
                await debug_logger.log_command("aiprompt", f"user {interaction.user.name}#{interaction.user.discriminator} used aiprompt for the first time since bot restart in guild {interaction.guild.name} {interaction.guild.id}. The API key has been retrieved for this guild.")
    else:
        api_key = api_keys[guild_id]
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
        await interaction.response.send_message(completion["choices"][0]["text"])
        await debug_logger.log_command("aiprompt",f"user {interaction.user.name}#{interaction.user.discriminator} used aiprompt with prompt {prompt}")
        await log_use(name)

# Running the bot
bot.run('')
