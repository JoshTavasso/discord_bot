"""
data.py

Some data needed for the bot

"""

_music_message = """

Music Commands:

?join ->
    Join Voice Channel

?leave ->
    Leave Voice Channel

?queue ->
    displays songs in queue

?enqueue "words here" ->
    add a song to a queue

?clearqueue ->
    clears the queue

?search "words here" ->
    specify key words to search on youtube

?results ->
    see results from latest search

?play "words here" ->
    play a song from the search results
    or paste in a youtube URL

    ?play OR ?play next ->
        plays next song in queue

?stop ->
    stops the song that is currently playing
    and plays next song in queue

?playing ->
    Displays the song that is currently playing

"""
_help_message = """

Test Bot

?purge "words here"->
    Mass Delete Messages that have key prefixes.
    For testing purposes.
    Ex uses:
    ?purge
    -> deletes every message that starts with '!'
    ?purge all
    -> deletes all messages in channel
    ?purge cool
    -> deletes every message that has 'cool' in it

?help music ->
    Music related commands

?help ->
    This message.

"""

prefix = '?'

music_help = "```" + _music_message + "```"

help_page =  "```" + _help_message + "```"

token = 'NDcyNjk1MTI0MjgzODgzNTQy.Dj3Hfg.QbQrajkO0cH11vG_spUvrAQ6bTk'

# message life time
life_time = 10

bot_extensions = ['commands.music', 'commands.general']
