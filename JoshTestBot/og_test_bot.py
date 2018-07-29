# THE VERSION THAT PLAYS OFF YOUTUBE RATHER THAN DIRECTLY FROM MP3
# THIS VERSION MIGHT ACTUALLY STILL WORK BECAUSE MP3 STILL LAGS I THINK!!!! :/

import discord
from discord.ext import commands

# some extra data needed for bot
from config import prefixes, help_page, token, life_time

# helper youtube function 
from youtube import generate_yt_url

# needed for putting bot in and out of voice channel
current_voice = None

# discord command bot
bot = commands.Bot(command_prefix='?', description = "test bot")

# Remove default help command, created our own 
bot.remove_command('help')

@bot.command(pass_context = True)
async def play(ctx, *args):
    # setup
    member = ctx.message.author
    server = ctx.message.server
    channel = member.voice.voice_channel
    global current_voice

    # Have the bot leave the voice channel
    # if it is connected, to hopefully get rid 
    # of the overlapping sound issue earlier
    if ctx.bot.is_voice_connected(server):
        await ctx.bot.say("Leaving Your Voice Channel")
        for voice_client in ctx.bot.voice_clients:
            if (voice_client.server == ctx.message.server):
                await voice_client.disconnect()
                break

    current_voice = await ctx.bot.join_voice_channel(channel)
    await ctx.bot.say("Now joining Your Voice Channel")

    # parse arguments
    search = ' '.join(args)
    print(search)

    if search == "": 
        return await bot.say("you didn't specify a search")

    # top URL for now
    url = generate_yt_url(search)[0] 
    await bot.say('...downloading the video')

    # play audio
    player = await current_voice.create_ytdl_player(url)
    player.start()
    await ctx.bot.say('The song is playing!')

@bot.command(pass_context = True)
async def help(ctx):
    await ctx.bot.say(help_page)

@bot.command(pass_context = True)
async def hello(ctx):
    """
    Says hello
    Me: !hello
    Bot: hello
    """
    await ctx.bot.say("hello")

@bot.command(pass_context=True)
async def purge(ctx, *args):
    """
    Mass Delete Messages that have key prefixes

    For testing purposes
    """
    channel = ctx.message.channel
    global prefixes

    if len(args) > 0 and args[0] == 'all':
        await ctx.bot.purge_from(channel, limit=1000)
    else:
        check = lambda msg: msg.content == "" or msg.content[0] in prefixes
        await ctx.bot.purge_from(channel, limit=1000, check=check)

    await ctx.bot.say("Messages have been purged", delete_after=life_time)


@bot.command(pass_context=True)
async def voice(ctx):
    """
    For joining/leaving the author's voice channel

    Example:

    Me: !voice
    Bot: Joining Your Voice Channel

    Me: !voice
    Bot: Leaving Your Voice Channel

    """
    global current_voice
    
    server = ctx.message.server
    channel = ctx.message.author.voice_channel

    if ctx.bot.is_voice_connected(server):
        await ctx.bot.say("Leaving Your Voice Channel")
        for voice_client in ctx.bot.voice_clients:
            if (voice_client.server == ctx.message.server):
                return await voice_client.disconnect()
    else:
        current_voice = await ctx.bot.join_voice_channel(channel)
        await ctx.bot.say("Joining Your Voice Channel")



# commented out for now, during debugging phase
'''
@bot.event
async def on_command_error(error, ctx):
    """
    For if a user says a wrong command, or
    an error occurs when a command is inputted.

    This gives them the help page
    """
    await bot.send_message(ctx.message.channel, "An error occured, maybe you inputted a wrong command\n{}".format(help_page))'''

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

if __name__ == '__main__':
	bot.run(token)
