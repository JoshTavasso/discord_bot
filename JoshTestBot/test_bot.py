# THE VERSION THAT PLAYS OFF YOUTUBE RATHER THAN DIRECTLY FROM MP3
# THIS VERSION IS THE DEFINITIE ONE SINCE MP3 LAGS TOO!!!

import discord
from discord.ext import commands

# some extra data needed for bot
from config import prefixes, help_page, token, life_time

# helper youtube function 
from youtube import generate_yt_url

# needed for putting bot in and out of voice channel
current_voice = None

# the song player, needed as global so
# the user can stop the player when calling
# the stop command
player = None

# discord command bot
bot = commands.Bot(command_prefix='?', description = "test bot")

#### Helper Functions ####

async def _join_voice_channel(ctx, channel):
    '''
    Helper function that joins
    voice channel
    for organization purposes since 
    the process of joining a voice channel
    is used multiple times
    '''
    global current_voice

    current_voice = await ctx.bot.join_voice_channel(channel)
    await ctx.bot.say("Joining Your Voice Channel")

async def _leave_voice_channel(ctx):
    '''
    Helper function that leaves
    voice channel
    for organization purposes since 
    the process of leaving a voice channel
    is used multiple times
    '''
    await ctx.bot.say("Leaving Your Voice Channel")
    for voice_client in ctx.bot.voice_clients:
        if (voice_client.server == ctx.message.server):
            return await voice_client.disconnect()

#### Commands ####

# Remove default help command, created my own 
bot.remove_command('help')

@bot.command(pass_context = True)
async def help(ctx):
    '''
    Displays Help Page
    '''
    await ctx.bot.say(help_page)

@bot.command(pass_context = True)
async def play(ctx, *args):
    '''
    User can search for a song on 
    youtube and this plays the first
    video that pops up in the search
    results

    Will try to make this better later
    '''
    # setup
    member = ctx.message.author
    server = ctx.message.server
    channel = member.voice.voice_channel
    global current_voice
    global player

    # Have the bot leave the voice channel
    # if it is connected, to hopefully get rid 
    # of the overlapping sound issue 
    if ctx.bot.is_voice_connected(server): 
        await _leave_voice_channel(ctx)

    # Have the bot join voice channel
    # to play song
    try:
        await _join_voice_channel(ctx, channel)
    except discord.errors.InvalidArgument: 
        return await ctx.bot.say("You are not in a Voice Channel!")

    # parse arguments
    search = ' '.join(args)
    print(search)

    if search == "": 
        return await bot.say("you didn't specify a search")

    # top video for now
    url = generate_yt_url(search)[0] 
    await bot.say('...downloading the video')

    # play audio
    player = await current_voice.create_ytdl_player(url)
    player.start()
    await ctx.bot.say('The song is playing!')

@bot.command(pass_context = True)
async def stop(ctx):
    '''
    Stops the song that is currently
    playing
    '''
    global player

    if player != None: 
        player.stop()
        player = None
        await ctx.bot.say('Stopped the song')
    else: 
        await ctx.bot.say('No song is playing!')

@bot.command(pass_context=True)
async def join(ctx):
    ''' 
    Joins the voice channel that
    the user is in
    '''
    global current_voice
    server = ctx.message.server
    channel = ctx.message.author.voice_channel

    if not ctx.bot.is_voice_connected(server):
        try:
            await _join_voice_channel(ctx, channel)
        except discord.errors.InvalidArgument: 
            return await ctx.bot.say("You are not in a Voice Channel!")
    else: 
        await ctx.bot.say("I am already in a Voice Channel!")

@bot.command(pass_context=True)
async def leave(ctx):
    '''
    Leaves the voice channel that
    the user is in
    '''
    server = ctx.message.server
    if ctx.bot.is_voice_connected(server): 
        await _leave_voice_channel(ctx)
    else: 
        await ctx.bot.say("How can I leave when I am not even in a Voice Channel boi?")

@bot.command(pass_context=True)
async def purge(ctx, *args):
    '''
    Mass Delete Messages that have key prefixes

    For testing purposes
    '''
    channel = ctx.message.channel
    global prefixes

    if len(args) > 0 and args[0] == 'all':
        await ctx.bot.purge_from(channel, limit=1000)
    else:
        check = lambda msg: msg.content == "" or msg.content[0] in prefixes
        await ctx.bot.purge_from(channel, limit=1000, check=check)

    await ctx.bot.say("Messages have been purged", delete_after=life_time)

# commented out for now, during debugging phase
'''
@bot.event
async def on_command_error(error, ctx):
    """
    For if a user says a wrong command, or
    an error occurs when a command is inputted.

    This gives them the help page
    """
    await bot.send_message(ctx.message.channel, "An error occured, maybe you inputted a wrong command\n{}".format(help_page))
'''

@bot.event
async def on_ready():
    ''' 
    To know if the bot has launched or not 
    '''
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

if __name__ == '__main__':
	bot.run(token)
