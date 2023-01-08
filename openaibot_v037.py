import os
import datetime
import json
import discord
from discord.ext import commands
from discord import app_commands
import openai
from openai import Completion
#import asyncio
#import subprocess
import api_key_manager
import command_setup
import debug_logger
#subprocess.Popen(['python', 'backup.py'])
bot_token = 'MTA0OTg5NzUzMjQwNDI3MzI0Mw.GRh1Ub.wk35-7aQwUZlqXJWuhJlvQ150o4YeA4vSwSuOc'
intents = discord.Intents.default()
intents.members = True
intents.dm_messages = True
intents.message_content = True
activity = discord.Activity(name='CoCFire somehow get me to work', type=discord.ActivityType.watching)
bot = commands.Bot(intents=intents,activity=activity,command_prefix="/")

command_setup.setup(bot)

@bot.event
async def on_guild_join(guild):
    guild_id = guild.id
    if not os.path.exists(f'server_data/{guild_id}'):
        os.makedirs(f'server_data/{guild_id}')
    owner = guild.owner
    if owner:
        await owner.send("Thank you for adding me to your server! Please use `/setapikey` within your server to finish setup!")
    await debug_logger.log_command("on_guild_join", f"bot joined guild {guild.name}")
@bot.event
async def on_guild_remove(guild):
    owner = guild.owner
    if owner:
        await owner.send(f"Hello! I'm sorry that I have been removed from your guild {guild.name}. \n"
                         "Could you please take a moment to give us some feedback on why you decided to remove the bot? \n"
                         "We would really appreciate it if you could let us know how we can improve. \n"
                         "Thank you for using our bot!")

        try:
            message = await client.wait_for('message', check=lambda message: message.author == owner, timeout=600.0)
        except asyncio.TimeoutError:
            print(f"No response from the owner of guild {guild.name}")
        else:
            # If the owner responds, write their feedback to a file
            with open(f'server_data/{guild.id}/feedback.json', 'w+') as feedback_file:
                feedback_file.write(message.content)
    await debug_logger.log_command("on_guild_remove", f"bot left guild {guild.name}")

async def analytics(client: discord.Client):
    # Create the `server_data` directory if it doesn't exist
    if not os.path.exists('server_data'):
        os.makedirs('server_data')

    # Iterate over all servers the bot is in
    for guild in client.guilds:
        # Create a subdirectory for this server
        guild_dir = f'server_data/{guild.id}'
        if not os.path.exists(guild_dir):
            os.makedirs(guild_dir)

        # Write the analytics data for this server to a file
        analytics_file = f'{guild_dir}/analytics.json'
        with open(analytics_file, 'w') as f:
            # Calculate the time that the bot has been in the server
            join_time = datetime.datetime.utcfromtimestamp(guild.me.joined_at.timestamp())
            now = datetime.datetime.utcnow()
            bot_uptime = now - join_time

            # Calculate the time that the server has existed
            creation_time = datetime.datetime.utcfromtimestamp(guild.created_at.timestamp())
            server_uptime = now - creation_time

            # Write the analytics data to the file
            data = {
                'server_name': guild.name,
                'member_count': guild.member_count,
                'server_uptime': str(server_uptime),
                'bot_uptime': str(bot_uptime)
            }
            json.dump(data, f, indent=4)

        # Write the list of members to a file
        members_file = f'{guild_dir}/members.json'
        with open(members_file, 'w') as f:
            # Write the list of members to the file
            member_list = [f"{member.name}#{member.discriminator} ID: {member.id}" for member in guild.members]
            json.dump(member_list, f, indent=4)
@bot.tree.command()
async def run_analytics(interaction: discord.Interaction):
    if interaction.user.id != 1000729109720219778:
        await interaction.response.send_message("Insufficient permissions. This event has been logged")
        await debug_logger.log_command("run_analytics", f"user {interaction.user.name}#{interaction.user.discriminator} attepted to use command run_analytics with insuficcient permissions in guild {interaction.guild.name} {interaction.guild.id}")
        return

    # Run the analytics function
    await interaction.response.send_message("Recording analytics for all guilds")
    await analytics(bot)
    await debug_logger.log_command("run_analytics", "successfully recorded analytics")
@bot.tree.command()
@app_commands.default_permissions(manage_guild=True)
async def setapikey(interaction: discord.Interaction, api_key: str):
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("You do not have permission to run this command. This event has been logged")
        await debug_logger.log_command("setapikey", f"user {interaction.user.name}#{interaction.user.discriminator} attepted to use command setapikey with insuficcient permissions in guild {interaction.guild.name} {interaction.guild.id}")
        return

    if not api_key.startswith('sk-'):
        await interaction.response.send_message("That doesn't appear to be a valid API key. Please make sure you're providing an OpenAI API key. This should start with 'sk-'.")
        await debug_logger.log_command("setapikey", f"user {interaction.user.name}#{interaction.user.discriminator} provided an invalid api key when running setapikey in guild {interaction.guild.name} {interaction.guild.id}")

    else:
        guild_id = interaction.guild.id
        api_key_manager.set_server_api_key(guild_id, api_key)
        await interaction.response.send_message("Successfully set the API key for this server.")
        await debug_logger.log_command("setapikey", f"user {interaction.user.name}#{interaction.user.discriminator} set the api key for guild {interaction.guild.name} {interaction.guild.id}")

@bot.tree.command()
async def aiprompt(interaction: discord.Interaction, prompt: str):
    api_key = await api_key_manager.get_server_api_key(interaction.guild.id)
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
    await debug_logger.log_command("aiprompt",f"user {interaction.user.name}#{interaction.user.discriminator} used aiprompt with prompt {prompt} and output {completion}")



bot.run(bot_token)
