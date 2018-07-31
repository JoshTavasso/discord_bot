"""
config.py

data needed for bot
just for organization purposes
"""

_help_message = """

Test Bot!

A bot we can use for testing purposes.

?join ->
    Join Voice Channel

?leave ->
    Leave Voice Channel

?play "words here" ->
    User can search for a song on 
    youtube and this plays the first
    video that pops up in the search
    results

    Will try to make this better later

    Possibly add in a queue, and a command
    to view all of the search results so
    the user can choose a video!

    Also, NOTE: Sometimes there is a 
    "ConnectionRefusedError" that happens
    when trying to play a song

    I am not too sure why that happens yet.

?purge ->
    Mass Delete Messages that have key prefixes.
    For testing purposes.

?help ->
    This message.

"""

prefixes = ['!', '?', '&', '`']

help_page =  "```" + _help_message + "```"

token = 'NDcyNjk1MTI0MjgzODgzNTQy.Dj3Hfg.QbQrajkO0cH11vG_spUvrAQ6bTk'

# message life time
life_time = 10
