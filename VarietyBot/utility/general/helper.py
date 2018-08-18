'''
Helper.py

Helper functions
'''

async def send_welcome_msg(bot, server):
    '''
    Sends welcome message to server
    '''
    for channel in server.channels:
        if (str(channel) == 'general'):
            return await bot.send_message(
                channel, "Hello There! Use {}help to see what I do!".format(bot.command_prefix))

def emoji_help(prefix):
    _emoji_message = f"""

Emoji Commands:

{prefix}emoji <emoji name>
    creates an emoji, given an 
    image in jpg or png format

    User needs to upload an image
    for this to work!

    Ex:
        -> User uploads pikachu image
        -> In the description of the image,
            user inputs: {prefix}emoji pikachu

{prefix}remove <emoji name>
    removes the emoji
"""

    return "```" + _emoji_message + "```"


def music_help(prefix):
    _music_message = f"""

Music/Voice Commands:

{prefix}join ->
    Join Voice Channel

{prefix}leave ->
    Leave Voice Channel

{prefix}search <key words> ->
    specify key words to search on youtube

{prefix}results ->
    see results from latest search

{prefix}queue ->
    displays songs in queue

{prefix}play <song> ->
    play a song from the search results
    or paste in a youtube URL

    If a song is currently playing,
    this commands adds the requested song
    to the queue

{prefix}stop ->
    stops the song that is currently playing
    and plays next song in queue

{prefix}playing ->
    Displays the song that is currently playing

"""

    return "```" + _music_message + "```"

def help_page(prefix):
    _help_message = f"""

~Variety Bot~

A Multi Purpose Bot

{prefix}prefix <arg> ->
    User can change the prefix 
    of this bot

{prefix}purge <args> ->
    Mass Delete Messages that have key prefixes.
    For testing purposes.
    Ex uses:
    {prefix}purge
    -> deletes every message that starts with '{prefix}'
    {prefix}purge all
    -> deletes all messages in channel
    {prefix}purge cool
    -> deletes every message that has 'cool' in it

{prefix}help music ->
    Shows Music related commands

{prefix}help emoji ->
    Shows Emoji related commands

{prefix}help ->
    This message.

"""

    return "```" + _help_message + "```"