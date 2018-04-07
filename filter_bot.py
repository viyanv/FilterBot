"""
FilterBot is used to remove non-image messages from Discord guild channel.
"""

import discord
from discord.ext import commands
from time import ctime

Client = discord.Client()
client = commands.Bot(command_prefix="?")


async def strip_msg(contents, mentions):
    """Strips contents of message from mentions."""
    contents_l = contents.split(" ")
    mentions_l = [""]
    for elem in mentions:
        mentions_l.append(elem.mention)
    return [x for x in contents_l if x not in mentions_l]


@client.event
async def on_ready():
    """Bot behaviour on ready state."""
    print("Bot is ready!")


@client.event
async def on_message(message):
    """Bot behaviour upon receiving a message."""
    if message.author.name == client.user.name or message.channel.type.name == 'private':
        return

    try:
        if message.content and not message.attachments:
            print(ctime(), message.author.name, message.content)
            if message.mentions:
                stripped = await strip_msg(message.content, message.mentions)
                if stripped:
                    await client.delete_message(message)
            else:
                await client.delete_message(message)
    except discord.errors.Forbidden:
        return

client.run("NDMxMTQ4MzgwNDUwNzE3NzA2.DaarUg.AcRZNPnHHc5pJ3PrldWVi6wkbzE")
