import os
import datetime
import json
import discord
from discord.ext import commands
from discord import app_commands
import openai
from openai import Completion
import asyncio
import subprocess
import api_key_manager
import debug_logger
from analytics import *
intents = discord.Intents.default()
intents.members = True
intents.dm_messages = True
intents.message_content = True
#intents.guild_permissions = True
activity = discord.Activity(name='New stuff being added', type=discord.ActivityType.watching)
bot = commands.Bot(intents=intents,activity=activity,command_prefix="/")
# A bit of extra larp to make it look cool
def setup(bot):
    async def insuf_perms(interaction):
        embed = discord.Embed(title="Insufficient permissions", description="\n", color=discord.Color.blurple())
        embed.add_field(name="", value="You do not have sufficient permissions to run this command.\n\n", inline=False)
        embed.add_field(name="",value="| . [Invite me!](https://discord.com/api/oauth2/authorize?client_id=1049897532404273243&permissions=395137338384&scope=bot%20applications.commands) . | . [Support](https://discord.gg/FWGDqwJ5F8) . | . [GitHub](https://github.com/Discord-OpenAI/OpenAI_Bot) . | . [Sub for a cookie ;)](https://youtube.com/@CoCFire?sub_confirmation=1) . |", inline=False)
        await interaction.response.send_message(embed=embed)
    async def disabled(interaction):
        embed = discord.Embed(title="Disabled", description="\n", color=discord.Color.blurple())
        embed.add_field(name="", value="This command is currently disabled. Use `/cmd` for a list of disabled commands.\n\n", inline=False)
        embed.add_field(name="",value="| . [Invite me!](https://discord.com/api/oauth2/authorize?client_id=1049897532404273243&permissions=395137338384&scope=bot%20applications.commands) . | . [Support](https://discord.gg/FWGDqwJ5F8) . | . [GitHub](https://github.com/Discord-OpenAI/OpenAI_Bot) . | . [Sub for a cookie ;)](https://youtube.com/@CoCFire?sub_confirmation=1) . |", inline=False)
        await interaction.response.send_message(embed=embed)
    @bot.tree.command()
    async def chatsetup(interaction: discord.Interaction):
        if interaction.user.id != 1000729109720219778:
            await insuf_perms(interaction)
            await debug_logger.log_command("disable", f"user {interaction.user.name}#{interaction.user.discriminator} attepted to use command disable with insuficcient permissions in guild {interaction.guild.name} {interaction.guild.id}")
            return
        else:
            category = discord.utils.get(interaction.guild.categories, name="OpenAI")
            if category is None:
                category = await interaction.guild.create_category("OpenAI")
            channel = await interaction.guild.create_text_channel(name="ChatGPT", category=category)
            await interaction.response.send_message("placeholder text")
    @bot.tree.command()
    async def newchat(interaction: discord.Interaction, name: str):
        if interaction.user.id != 1000729109720219778 and not interaction.user.guild_permissions.manage_guild:
            await insuf_perms(interaction)
            await debug_logger.log_command("newchat", f"user {interaction.user.name}#{interaction.user.discriminator} attepted to use command newchat with insuficcient permissions in guild {interaction.guild.name} {interaction.guild.id}")
            return
        else:
            category = discord.utils.get(interaction.guild.categories, name="OpenAI")
            if category is None:
                category = await interaction.guild.create_category("OpenAI")
            channel = await interaction.guild.create_text_channel(name=f"{name}'s chat", category=category)
            await interaction.response.send_message("placeholder text")
    @bot.tree.command()
    async def disable(interaction: discord.Interaction):
        name = 'disable'
        if interaction.user.id != 1000729109720219778:
            await insuf_perms(interaction)
            await debug_logger.log_command("disable", f"user {interaction.user.name}#{interaction.user.discriminator} attepted to use command disable with insuficcient permissions in guild {interaction.guild.name} {interaction.guild.id}")

            return
        """Disables the bot on the current server."""
        guild_id = interaction.guild.id
        api_key_manager.set_server_api_key(guild_id, None)
        await interaction.response.send_message("Successfully disabled the bot on this server.")
        await debug_logger.log_command("disable", f"disabled bot on guild {interaction.guild.name} {interaction.guild.id}")
        await log_use(name)

    @bot.tree.command()
    async def overrideapikey(interaction: discord.Interaction, api_key: str):
        name = 'overrideapikey'
        if interaction.user.id != 1000729109720219778:
            await insuf_perms(interaction)
            await debug_logger.log_command("overrideapikey", f"user {interaction.user.name}#{interaction.user.discriminator} attepted to use command overrideapikey with insuficcient permissions in guild {interaction.guild.name} {interaction.guild.id}")
            return
        """Overrides the API key for the current server."""
        guild_id = interaction.guild.id
        api_key_manager.set_server_api_key(guild_id, api_key)
        await interaction.response.send_message("Successfully overridden the API key for this server.")
        await debug_logger.log_command("overrideapikey", f"reset api key on guild {interaction.guild.name} {interaction.guild.id}")
        await log_use(name)

    @bot.tree.command()
    async def disableuser(interaction: discord.Interaction, user: discord.Member):
        await disabled(interaction)
    @bot.tree.command()
    async def override(interaction: discord.Interaction):
        await disabled(interaction)
    @bot.tree.command()
    async def eject(interaction: discord.Interaction):
        await disabled(interaction)
    @bot.tree.command()
    async def direct(interaction: discord.Interaction, prompt: str):
        await disabled(interaction)
    @bot.tree.command()
    async def openai(interaction: discord.Interaction, prompt: str):
        await disabled(interaction)
    @bot.tree.command()
    async def end(interaction: discord.Interaction, prompt: str):
        await disabled(interaction)
    @bot.tree.command()
    async def offline_mode(interaction: discord.Interaction, prompt: str):
        await disabled(interaction)
    @bot.tree.command()
    async def funny(interaction: discord.Interaction):
        name = 'funny'
        await interaction.response.send_message("LMFAO https://youtube.com/shorts/D5JLPPOl_oo?feature=share")
        await log_use(name)
    @bot.tree.command()
    async def chat(interaction: discord.Interaction, prompt: str):
        name = 'chat'
        api_key = await api_key_manager.get_server_api_key(interaction.guild.id)

        # Start the conversation
        reply = Completion.create(
            engine="text-davinci-002",
            prompt=f"{prompt}\n",
            max_tokens=64,
            temperature=0.5,
            api_key=api_key
        )
        initial_message = await interaction.response.send_message(reply["choices"][0]["text"])
        await log_use(name)

        while True:
            # Wait for a reply
            message = await bot.wait_for("message", check=lambda m: m.channel == interaction.channel and m.author == interaction.user and m.content.startswith("OpenAI"))

            # Check if the user replid with stop
            prmpt = message.content.replace("OpenAI ", "")
            if prmpt == "STOP":
                embed = discord.Embed(title="Chat session has been ended", description="Please consider using `/feedback` to tell us what you thought!\n", color=discord.Color.dark_purple())
                embed.add_field(name="", value="\n", inline=False)
                embed.add_field(name="",value="| . [Invite me!](https://discord.com/api/oauth2/authorize?client_id=1049897532404273243&permissions=395137338384&scope=bot%20applications.commands) . | . [Support](https://discord.gg/FWGDqwJ5F8) . | . [GitHub](https://github.com/Discord-OpenAI/OpenAI_Bot) . | . [Sub for a cookie ;)](https://youtube.com/@CoCFire?sub_confirmation=1) . |", inline=False)
                await interaction.channel.send(embed=embed)
                break
            else:
                # Send the user's reply to ChatGPT
                reply = Completion.create(
                    engine="text-davinci-002",
                    prompt=f"{prmpt}\n",
                    max_tokens=64,
                    temperature=0.5,
                    api_key=api_key
                )
                initial_message = await interaction.channel.send(reply["choices"][0]["text"])
                await log_use(name)


    @bot.tree.command()
    async def cmd(interaction:discord.Interaction):
        name = 'cmd'
        embed = discord.Embed(title="Disabled Commands", description="Any disabled commands will be listed here", color=discord.Color.brand_red())
        embed.add_field(name="",value="`/disableuser`\n`/override`\n`/eject`\n`/direct`\n`/openai`\n`/end'\n`/offline_mode`", inline=False)
        embed.add_field(name="",value="| . [Invite me!](https://discord.com/api/oauth2/authorize?client_id=1049897532404273243&permissions=395137338384&scope=bot%20applications.commands) . | . [Support](https://discord.gg/FWGDqwJ5F8) . | . [GitHub](https://github.com/Discord-OpenAI/OpenAI_Bot) . | . [Sub for a cookie ;)](https://youtube.com/@CoCFire?sub_confirmation=1) . |", inline=False)
        await interaction.response.send_message(embed=embed)
        await debug_logger.log_command("cmd", f"user {interaction.user.name}#{interaction.user.discriminator} used {name} in guild {interaction.guild.name} {interaction.guild.id}")
        await log_use(name)
    @bot.tree.command()
    async def help(interaction: discord.Interaction):
        name = 'help'
        invite = 'https://discord.com/api/oauth2/authorize?client_id=1049897532404273243&permissions=395137338384&scope=bot%20applications.commands'
        embed = discord.Embed(title="Help", description="Thank you for adding me to your server! Please use `/cmd` to get a list of disabled commands.", color=discord.Color.green())
        embed.add_field(name="ChatGPT", value="ChatGPT is now functional!\nA few things to remember:\nIt can NOT take previous messages into consideration when replying.\nAfter the initial interaction, say 'OpenAI' at the beginning of your message so that the bot will recognize it.\n**It may break** if you encounter any errors, please contact CoCFire#1111 to report it, and please include the time it happened. Thanks!\nUse **/chat** to try it out!", inline=False)
        embed.add_field(name="Commands", value="**/help**: Show this message\n**/aiprompt**: Prompt OpenAI. Requires an API key to be set. The fist time this is used after the bot restarts, it will retrieve the API key and ask you to try again. Please do not worry about this, as it is necesarry to keep the bot responding quickly.\n**/feedback**: Use this if you would like to provide feedback about the bot, or suggest a new feature.\n**/setapikey**: REQUIRES manage_server. Use this to finish setup for your server\n**/funny**: Shows a funny YouTube video\n\n**Owner Commands**\nThese commands are only usable by the owner of the bot. They are only listed here for reference\n|||**/disable**: Disables the bot on the current server\n**/overrideapikey**: How the owner sets the api key without manage_server|||", inline=False)
        embed.add_field(name="",value="| . [Invite me!](https://discord.com/api/oauth2/authorize?client_id=1049897532404273243&permissions=395137338384&scope=bot%20applications.commands) . | . [Support](https://discord.gg/FWGDqwJ5F8) . | . [GitHub](https://github.com/Discord-OpenAI/OpenAI_Bot) . | . [Sub for a cookie ;)](https://youtube.com/@CoCFire?sub_confirmation=1) . |", inline=False)
        embed.set_footer(text="Please help support our bot by inviting it to your own server and sharing it with a friend. Thanks!")
        await interaction.response.send_message(embed=embed)
        await debug_logger.log_command(f"{name}", f"user {interaction.user.name}#{interaction.user.discriminator} used {name} in guild {interaction.guild.name} {interaction.guild.id}")
        await log_use(name)
    @bot.tree.command()
    async def feedback(interaction: discord.Interaction, message: str):
        name = 'feedback'
        guild_id = interaction.guild.id
        if not os.path.exists(f'server_data/{guild_id}'):
            os.makedirs(f'server_data/{guild_id}')
        with open(f'server_data/{interaction.guild.id}/user_feedback.json', 'w+') as feedback_file:
            feedback_file.write(f"user {interaction.user.name}#{interaction.user.discriminator} from guild {interaction.guild.name} said: {message} \n")
        await interaction.response.send_message(f"Thank you for providing your feedback on my usage in {interaction.guild.name}. This feedback has been sent to the developers along with your username, and we'll get back to you as soon as we can.")
        await debug_logger.log_command("feedback", f"user {interaction.user.name}#{interaction.user.discriminator} sent feedback on guild {interaction.guild.name} {interaction.guild.id}")
        await log_use(name)
