# NEEDS TO FUN SIMULTANEOUSLY WITH TEST BOT

import discord
client = discord.Client()

from config import token

from youtube import generate_yt_url

from discord.ext import commands

voice = None

@client.event
async def on_message(message: 'discord message object'):
    member = message.author
    server = message.server
    channel = member.voice.voice_channel
    global voice

    if message.content.startswith('?play'):
        if not client.is_voice_connected(server): voice = await client.join_voice_channel(channel)
        search = message.content[6:]
        if search == "": return await client.send_message(message.channel, "you didn't specify a search")

        # top URL for now
        url = generate_yt_url(search)[0] 
        await client.send_message(message.channel, '...downloading the video')

        # play audio
        player = await voice.create_ytdl_player(url)
        player.start()
        await client.send_message(message.channel, 'The song is playing!')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


if __name__ == '__main__':
    client.run(token)
