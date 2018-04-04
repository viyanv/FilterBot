import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import aiohttp

Client = discord.Client()
client = commands.Bot(command_prefix="?")

@client.event
async def on_ready():
    print("Bot is ready!")

@client.event
async def on_message(message):

    #print(message)

    print(len(message.attachments))
    print(len(message.content))
    # if len(message.attachments) > 0 and len(message.content) > 0:
    #     attachment = message.attachments[0]['url']
    #     print(attachment)
    #
    #     with aiohttp.ClientSession() as session:
    #         async with session.get(attachment) as resp:
    #             test = await resp.read()
    #             with open("img.png", "wb") as f:
    #                 f.write(test)
    #
    #     #await client.send_message(message.channel, attachment)
    #     await client.send_file(message.channel, "img.png")
    #
    if len(message.content) > 0:
        if len(message.attachments) > 0:
            attachment = message.attachments[0]['url']
            # print(attachment)

            with aiohttp.ClientSession() as session:
                async with session.get(attachment) as resp:
                    test = await resp.read()
                    with open("img.png", "wb") as f:
                        f.write(test)

            await client.send_file(message.channel, "img.png")
            await client.delete_message(message)

        #TODO delete_msg

client.run("NDMwOTY1NTM5MjgwNjUwMjQz.DaYRjw.-4NmCNlJw-u8PFWsz1mwaZHejhg")