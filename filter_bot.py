"""
FilterBot is used to remove non-image messages from Discord guild channel.
"""

import discord
from discord.ext import commands
import aiohttp

Client = discord.Client()
client = commands.Bot(command_prefix="?")

private_response = "Na tym kanale możesz wysyłać tylko obrazy i @wzmianki! " \
                   "Wyślij swoją wiadomość gdzieś indziej:\n\n*"

@client.event
async def on_ready():
    """Bot behaviour on ready state."""
    print("Bot is ready!")


async def get_image(url):
    """Downloads image from specified URL"""
    with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            img = await resp.read()
            with open("img.png", "wb") as file:
                file.write(img)


@client.event
async def on_message(message):
    """Bot behaviour on receiving a message."""
    if message.author.name == client.user.name or message.channel.type.name == 'private':
        return

    try:
        if not message.content:

            contents = message.content.split(" ")
            mentions_list = [""]
            mention_msg = ""
            if not message.mentions:
                for mention_item in message.mentions:
                    mentions_list.append(mention_item.mention)
                    mention_msg += " " + mention_item.mention
            contents_wo_mentions = [x for x in contents if x not in mentions_list]

            if not message.attachments:
                if not contents_wo_mentions:
                    attachment = message.attachments[0]['url']
                    await get_image(attachment)

                    await client.delete_message(message)

                    if not message.mentions:
                        await client.send_message(message.channel,
                                                  message.author.name + " tagged:" + mention_msg)
                        print(message.author.name + " tagged:" + mention_msg)
                    else:
                        await client.send_message(message.channel, message.author.name + " posted:")
                        print(message.author.name + " posted.")

                    await client.send_file(message.channel, "img.png")
                    await client.send_message(message.author,
                                              private_response + message.content + "*")

            else:
                if not message.mentions:
                    if not contents_wo_mentions:
                        await client.send_message(message.channel,
                                                  message.author.name + " tagged:" + mention_msg)
                        print(message.author.name + " tagged:" + mention_msg)
                        await client.send_message(message.author,
                                                  private_response + message.content + "*")
                        print(message.author.name + ": " + message.content)
                        await client.delete_message(message)
                else:
                    await client.delete_message(message)
                    await client.send_message(message.author,
                                              private_response + message.content + "*")
                    print(message.author.name + ": " + message.content)

    except discord.errors.Forbidden:
        return

client.run("NDMxMTQ4MzgwNDUwNzE3NzA2.DaarUg.AcRZNPnHHc5pJ3PrldWVi6wkbzE")
