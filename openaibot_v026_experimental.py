import os
import discord
from discord.ext import commands
from discord import app_commands
import openai
from openai import Completion
import asyncio
import api_key_manager
#from chat import *
bot_token = 'bot_token'
intents = discord.Intents.default()
intents.members = True
intents.dm_messages = True
intents.message_content = True
activity = discord.Activity(name='CoCFire somehow get me to work', type=discord.ActivityType.watching)
bot = commands.Bot(intents=intents,activity=activity,command_prefix="/")


@bot.event
async def on_guild_join(guild):
    owner = guild.owner
    if owner:
        await owner.send("Thank you for adding me to your server! Please use `/setapikey` within your server to finish setup!")

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


@bot.tree.command()
@app_commands.default_permissions(manage_guild=True)
async def setapikey(interaction: discord.Interaction, api_key: str):
    # Check if the user has the manage_guild permission
    if not interaction.user.guild_permissions.manage_guild:
        await interaction.response.send_message("You do not have permission to run this command.")
        return

    # check if the API key is valid
    if not api_key.startswith('sk-'):
        await interaction.response.send_message("That doesn't appear to be a valid API key. Please make sure you're providing an OpenAI API key. This should start with 'sk-'.")

    else:
        guild_id = interaction.guild.id
        api_key_manager.set_server_api_key(guild_id, api_key)
        await interaction.response.send_message("Successfully set the API key for this server.")


@bot.tree.command()
async def direct(interaction: discord.Interaction, prompt: str):
    await interaction.response.send_message("disabled")
@bot.tree.command()
async def openai(interaction: discord.Interaction, prompt: str):
    await interaction.response.send_message("disabled")
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

@bot.tree.command()
async def chat(interaction: discord.Interaction, prompt: str):
    # Extract the prompt and name from the message content
    api_key = await api_key_manager.get_server_api_key(interaction.guild.id)
    category = discord.utils.get(interaction.guild.categories, name="OpenAI")
    if category is None:
        category = await interaction.guild.create_category("OpenAI")
    overwrites = {
        interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }
    channel = await interaction.guild.create_text_channel(name=f"{interaction.user.name}'s chat", category=category, overwrites=overwrites)

    # send the initial message to the channel
    await channel.send(prompt)
    
    def check(m):
        return m.channel == channel
    
    while True:
        try:
            # wait for the next message from the other user
            message = await interaction.client.wait_for('message', check=check, timeout=60.0)
        except asyncio.TimeoutError:
            # if the other user doesn't respond within 60 seconds, end the conversation
            await interaction.response.send_message("The other user didn't respond within 60 seconds. Ending the conversation.")
            break
        else:
            # generate a response using ChatGPT
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"{message.content}\n",
                max_tokens=64,
                temperature=0.5,
                api_key=api_key
            )
            await channel.send(response.text)



bot.run(bot_token)
