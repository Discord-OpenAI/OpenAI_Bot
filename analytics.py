# openaibot_v037.py
# Made by CoCFire#1111

# Importing first libraries
import os
import datetime
import json
import asyncio

# Importing Discord and OpenAI
#import functools
import discord
from discord.ext import commands
from discord import app_commands

# Importing custom modules
import debug_logger

# Setting up bot intents
intents = discord.Intents.default()
intents.members = True
intents.dm_messages = True
intents.message_content = True
activity = discord.Activity(name='CoCFire somehow get me to work', type=discord.ActivityType.watching)
bot = commands.Bot(intents=intents,activity=activity,command_prefix="/")

async def log_use(name):
    # Create the `server_data/bot` directory if it doesn't exist
    path = 'server_data/bot'
    if not os.path.exists(path):
        os.makedirs(path)
    #Open the cmd_usage.json or create one if doesn't exist
    file = f'{path}/total.json'
    if os.path.exists(file):
        with open(file, 'r') as f:
            total_commands = json.load(f)
    else:
        total_commands = 0

    #Increment the value and write it back
    total_commands += 1
    with open(file, 'w') as f:
        json.dump(total_commands, f)
def total_usage():
    with open("server_data/bot/total.json", 'r') as f:
        cmd_usage = json.load(f)
    return cmd_usage
async def analytics(client: discord.Client):
    # Create the `server_data` directory if it doesn't exist
    if not os.path.exists('server_data'):
        os.makedirs('server_data')
    if not os.path.exists('server_data/bot'):
        os.makedirs('server_data/bot')
    
    now = datetime.datetime.now()
    bot_analytics_file = f'server_data/bot/{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}.json'
    server_analytics = {}
    bot_analytics = {}
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
            server_analytics[guild.id] = data

        # Write the list of members to a file
        members_file = f'{guild_dir}/members.json'
        with open(members_file, 'w') as f:
            # Write the list of members to the file
            member_list = [f"{member.name}#{member.discriminator} ID: {member.id}" for member in guild.members]
            json.dump(member_list, f, indent=4)

    bot_analytics["total_servers"] = len(client.guilds)
    bot_analytics["total_commands_run"] = total_usage()
#    bot_analytics["uptime"] = datetime.datetime.utcnow() - client.uptime
#    bot_analytics["per_server_commands"] = server_analytics
    with open(bot_analytics_file, 'w') as f:
        json.dump(bot_analytics, f, indent=4)
    await debug_logger.log_command("analytics", "analytics were recorded")
