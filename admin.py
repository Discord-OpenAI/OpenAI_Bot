# Add some extra larp to make the bot look cool
import os
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import api_key_manager
from admin_commands import *
bot_token = ''
intents = discord.Intents.default()
intents.members = True
intents.dm_messages = True
intents.message_content = True
activity = discord.Activity(name='CoCFire somehow get me to work', type=discord.ActivityType.watching)
bot = commands.Bot(intents=intents,activity=activity,command_prefix="/")
setup(bot)
bot.run(bot_token)
