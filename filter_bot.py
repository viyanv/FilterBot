import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import aiohttp

Client = discord.Client()
client = commands.Bot(command_prefix="?")

private_response = "Na tym kanale możesz wysyłać tylko obrazy i @wzmianki! Wyślij swoją wiadomość gdzieś indziej:\n\n*"

@client.event
async def on_ready():
    print("Bot is ready!")


async def get_image(url):
    with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            img = await resp.read()
            with open("img.png", "wb") as f:
                f.write(img)


@client.event
async def on_message(message):

    if message.author.name == client.user.name or message.channel.type.name == 'private':
        print(message.channel)
        print("Blocking...")
        # print("Tę wiadomość: " + message.content + " wysłał: " + message.author.name)
        # print("message.author: " + message.author.name)
        # print("client.user: " + client.user.name)
        return

  #  print(message.author.name)
  #  print(client.user.name)
    print(message.channel)

    #print(message.content)
   # print(client.user)

    try:
        if len(message.content) > 0:

            contents = message.content.split(" ")
            mentions_list = [""]
            mention_msg = ""
            if len(message.mentions) > 0:
                for mention_item in message.mentions:
                    mentions_list.append(mention_item.mention)
                    mention_msg += " " + mention_item.mention
            contents_wo_mentions = [x for x in contents if x not in mentions_list]

            if len(message.attachments) > 0:
                if len(contents_wo_mentions) > 0:
                    attachment = message.attachments[0]['url']
                    await get_image(attachment)

                    await client.delete_message(message)

                    if len(message.mentions) > 0:
                        await client.send_message(message.channel, message.author.name + " tagged:" + mention_msg)
                    else:
                        await client.send_message(message.channel, message.author.name + " posted:")

                    await client.send_file(message.channel, "img.png")
                    await client.send_message(message.author, private_response + message.content + "*")

            else:
                if len(message.mentions) > 0:
                    if len(contents_wo_mentions) > 0:
                        await client.send_message(message.channel, message.author.name + " tagged:" + mention_msg)
                        await client.send_message(message.author, private_response + message.content + "*")
                        await client.delete_message(message)
                else:
                    await client.delete_message(message)
                    await client.send_message(message.author, private_response + message.content + "*")

    except discord.errors.Forbidden:
        return

client.run("NDMxMTQ4MzgwNDUwNzE3NzA2.DaarUg.AcRZNPnHHc5pJ3PrldWVi6wkbzE")