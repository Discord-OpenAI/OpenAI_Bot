import os
import discord
from discord.ext import commands
from discord import app_commands
import openai
from openai import Completion
import asyncio

bot_token = 
api_key = 
#owner_id = '1019152307688050710'

openai.api_key = api_key

intents = discord.Intents.default()
activity = discord.Activity(name='CoCFire somehow get me to work', type=discord.ActivityType.watching)
bot = commands.Bot(intents=intents,activity=activity,command_prefix="/")

# Connecting to the Server
@bot.event
async def on_ready():
    # Initial message
    channel = bot.get_channel(914720296165077046)
    await channel.send("Initialized openaibot_v021.py")

@bot.tree.command()
async def openai(interaction: discord.Interaction, prompt: str):
    max_tokens = 32
    temperature = 0.4
    completion = Completion.create(
        engine="davinci",
        prompt=prompt[3:],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    # Relaying to Discord
    await interaction.response.send_message(completion["choices"][0]["text"])

    
bot.run(bot_token)

