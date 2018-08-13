"""
data.py

Some data needed for the bot

"""

token = 'NDc1Nzk4MjcxNzk3ODg3MDA4.Dklzww.TrpO2-ztzajhpqnWInluqoia7xU'

# message life time
life_time = 10

bot_extensions = [
                  'utility.music.commands', 
                  'utility.emoji.commands', 
                  'utility.general.commands'
                  ]

prefix = '!'

_emoji_message = f"""

Emoji Commands:

{prefix}emoji <emoji name>
    creates an emoji, given an 
    image in jpg or png format

{prefix}remove <emoji name>
    removes the emoji
"""

_music_message = f"""

Music Commands:

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

{prefix}enqueue <song> ->
    add a song to a queue

{prefix}clearqueue ->
    clears the queue

{prefix}play <song> ->
    play a song from the search results
    or paste in a youtube URL

    play OR play next ->
        plays next song in queue

{prefix}stop ->
    stops the song that is currently playing
    and plays next song in queue

{prefix}playing ->
    Displays the song that is currently playing

"""
_help_message = f"""

Variety Bot!

A Multi Purpose Bot

{prefix}purge "words here"->
    Mass Delete Messages that have key prefixes.
    For testing purposes.
    Ex uses:
    ?purge
    -> deletes every message that starts with '!'
    ?purge all
    -> deletes all messages in channel
    ?purge cool
    -> deletes every message that has 'cool' in it

{prefix}help music ->
    Shows Music related commands

{prefix}help emoji ->
    Shows Emoji related commands

{prefix}help ->
    This message.

"""

music_help = "```" + _music_message + "```"

emoji_help =  "```" + _emoji_message + "```"

help_page =  "```" + _help_message + "```"
