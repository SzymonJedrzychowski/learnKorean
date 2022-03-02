import discord
import asyncio
import platform
import json


def load(lastFileTime: int):
    """Load file from the discord channel

    :param lastFileTime: time of last save of save file
    """

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    with open("data/json/discordData.json") as f:
        discordData = json.load(f)

    client = discord.Client()

    @client.event
    async def on_ready():
        file = (await client.get_channel(discordData["channelId"]).history(limit=1).flatten())[0]
        await file.attachments[0].save(fp="data/json/tempData.json")
        with open("data/json/tempData.json") as f:
            data = json.load(f)
            thisFileTime = data["time"]
            if thisFileTime > lastFileTime:
                await file.attachments[0].save(fp="data/json/data.json")

        await client.close()

    client.run(discordData["token"])

    with open("data/json/tempData.json") as f:
        data = json.load(f)
        thisFileTime = data["time"]

    if thisFileTime < lastFileTime:
        return [False, 0]
    elif thisFileTime == lastFileTime:
        return [False, 1]

    return [True]


def save():
    """Save data on discord channel"""

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    with open("data/json/discordData.json") as f:
        discordData = json.load(f)

    client = discord.Client()

    @client.event
    async def on_ready():
        await client.get_channel(discordData["channelId"]).send(file=discord.File("data/json/data.json"))
        await client.close()

    client.run(discordData["token"])
