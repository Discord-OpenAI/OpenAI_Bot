"""

Hey! I've been working on cleaning up my code a bit, so a few things may look different.
First of all, I'm compacting all of my import statements to keep that nice and tidy.
Second, I've created a variable for the embed footer, since it takes up a lot of space to
copy/paste the entire thing everywhere, and it also makes it easier to edit.
Third, I've started using this method for long comments.

"""

import os, datetime, json, asyncio, discord, openai, api_key_manager, debug_logger
from discord.ext import commands
from discord import app_commands, Embed
from openai import Completion
from chatgpttest import *
from analytics import *
import trainingDataCollector as tdc

intents = discord.Intents.default()
intents.members = True
intents.dm_messages = True
intents.message_content = True
activity = discord.Activity(name='New stuff being added', type=discord.ActivityType.watching)
bot = commands.Bot(intents=intents,activity=activity,command_prefix="/")


cmd_setup(bot)

async def analytics_loop():

    """

    records analytics every 30 minutes
    also keeps the bot labled as "active" because of a free hosting site lol

    """
    
    while True:
        await analytics(bot)
        await debug_logger.log_command("analytics_loop", "recording analytics automatically")
        await asyncio.sleep(1800)

api_keys = {}

@bot.event
async def on_ready():
    loop = asyncio.get_event_loop()
    loop.create_task(analytics_loop())


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
    await debug_logger.log_command("on_guild_remove", f"bot left guild {guild.name}")


def embed_suffix(embed):
    embed.add_field(name="",value="| . [Invite me!](https://discord.com/api/oauth2/authorize?client_id=1049897532404273243&permissions=274878188560&scope=bot%20applications.commands) . | . [Support](https://discord.gg/FWGDqwJ5F8) . | . [Review us!](https://top.gg/bot/1049897532404273243) . | . [GitHub](https://github.com/Discord-OpenAI/OpenAI_Bot) . | . [Sub for a cookie ;)](https://youtube.com/@CoCFire?sub_confirmation=1) . |", inline=False)


@bot.tree.command()
async def run_analytics(interaction: discord.Interaction):

    """

    This can be used to manually record the bot's analytics.
    it is only usable by the bot owner

    """
    
    name = 'run_analytics'
    if interaction.user.id != 1000729109720219778:
        embed = discord.Embed(title="Insufficient permissions", description="\n", color=discord.Color.blurple())
        embed.add_field(name="", value="You do not have sufficient permissions to run this command.\n\n", inline=False)
        embed_suffix(embed)
        await interaction.response.send_message(embed=embed)
        await debug_logger.log_command("run_analytics", f"user {interaction.user.name}#{interaction.user.discriminator} attepted to use command run_analytics with insuficcient permissions in guild {interaction.guild.name} {interaction.guild.id}")
        return

    await interaction.response.send_message("Recording analytics for all guilds")
    await analytics(bot)
    await debug_logger.log_command("run_analytics", "successfully recorded analytics")
    await log_use(name)

@bot.tree.command()
@app_commands.default_permissions(manage_guild=True)
async def setapikey(interaction: discord.Interaction, api_key: str):

    """

    Allows guild admins to set an API key for their guild
    Only usable by members with manage_server permissions
    to prevent someone from wiping the API key

    """
    
    name = 'setapikey'
    if not interaction.user.guild_permissions.manage_guild:
        embed = discord.Embed(title="Insufficient permissions", description="\n", color=discord.Color.blurple())
        embed.add_field(name="", value="You do not have sufficient permissions to run this command.\n\n", inline=False)
        embed_suffix(embed)
        await interaction.response.send_message(embed=embed)
        await debug_logger.log_command("setapikey", f"user {interaction.user.name}#{interaction.user.discriminator} attepted to use command setapikey with insuficcient permissions in guild {interaction.guild.name} {interaction.guild.id}")
    elif not api_key.startswith('sk-'):
        embed = discord.Embed(title="Invalid API key", description="\n", color=discord.Color.blurple())
        embed.add_field(name="", value="That doesn't appear to be a valid API key. Please make sure you're providing an OpenAI API key. This should start with 'sk-'.\nIf you do not have an API key, you can generate one at https://beta.openai.com/. Please note that you must have credits on your account for the bot to work\nWARNING: WE WILL NEVER ASK YOU TO DISCLOSE YOUR API KEY OUTSIDE OF THIS COMMAND. IF ANYONE CLAIMING TO BE FROM OPENAI DM'S YOU ASKING FOR YOUR API KEY, PLEASE REPORT THEM TO THE BOT'S SUPPORT SERVER OR THE OFFICIAL OPENAI DISCORD SERVER.\n\n", inline=False)
        embed_suffix(embed)
        await interaction.response.send_message(embed=embed)
        await debug_logger.log_command("setapikey", f"user {interaction.user.name}#{interaction.user.discriminator} provided an invalid api key when running setapikey in guild {interaction.guild.name} {interaction.guild.id}")
    else:
        guild_id = interaction.guild.id
        api_key_manager.set_server_api_key(guild_id, api_key)
        embed = discord.Embed(title="API key set", description="\n", color=discord.Color.blurple())
        embed.add_field(name="", value="Successfully set the API key for this server.\n\n", inline=False)
        embed_suffix(embed)
        await interaction.response.send_message(embed=embed)
        await debug_logger.log_command("setapikey", f"user {interaction.user.name}#{interaction.user.discriminator} set the api key for guild {interaction.guild.name} {interaction.guild.id}")
        await log_use(name)

@bot.tree.command()
async def aiprompt(interaction: discord.Interaction, prompt: str):

    """

    The first command added to the bot
    It's amazing how far we've come!

    """
    
    name = 'aiprompt'
    guild_id = interaction.guild.id
    if guild_id not in api_keys:
        if not os.path.exists(f'server_data/{guild_id}/api_key.json'):
            embed = discord.Embed(title="No API key", description="\n", color=discord.Color.blurple())
            embed.add_field(name="", value="There is no API key set for this guild. Please ask an admin to set one with /setapikey, or contact CoCFire#1111 for help.\n\n", inline=False)
            embed_suffix(embed)
            await interaction.response.send_message(embed=embed)
            await debug_logger.log_command("aiprompt", f"user {interaction.user.name}#{interaction.user.discriminator} used aiprompt in guild {interaction.guild.name} {interaction.guild.id} with invalid API key set.")
        else:
            api_keys[guild_id] = await api_key_manager.get_server_api_key(guild_id)
            if not api_keys[guild_id].startswith('sk-'):
                await interaction.response.send_message("The API key set for this guild seems to be invalid. Please ask an admin to reset it using /setapikey, or contact CoCFire#1111 for help")
                await debug_logger.log_command("aiprompt", f"user {interaction.user.name}#{interaction.user.discriminator} used aiprompt in guild {interaction.guild.name} {interaction.guild.id} with invalid API key set.")
            else:
                embed = discord.Embed(title="", description="This is the first time the bot has been used in this server since bot restart. The API key has been retrieved.", color=discord.Color.blurple())
                embed.add_field(name="", value="Please use `/help` for more info.\n\n", inline=False)
                embed_suffix(embed)
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
        output = completion["choices"][0]["text"]
        await interaction.response.send_message(output)
        filename = await tdc.getFile('default')
        await tdc.logPrompt(filename, False, prompt, output)
        await debug_logger.log_command("aiprompt",f"user {interaction.user.name}#{interaction.user.discriminator} used aiprompt with prompt {prompt} in guild {interaction.guild.name} {interaction.guild.id}")
        await log_use(name)

@bot.tree.command()
async def chat(interaction: discord.Interaction, prompt: str):

    """

    The actual chat command is on the bot instance hosted by botshard. It was removed here to prevent the bot from responding twice
    since chat doesn't use interaction.response.send_message, which is what keeps the bot from responding twice in other commands.

    """
    
    name = 'chat'
    filename = await tdc.getFile('default')
    await tdc.logPrompt(filename, False, prompt, 'null')
    await debug_logger.log_command(name, f"User {interaction.user.name}#{interaction.user.discriminator} used chat with prompt {prompt} in guild {interaction.guild.name} {interaction.guild.id}. Check BotShard console for more info")
    



# Running the bot
bot.run('')

