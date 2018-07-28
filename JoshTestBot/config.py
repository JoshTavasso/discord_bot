"""
config.py

data needed for bot
just for organization purposes
"""

prefixes = ['!', '?', '&', '`']

help_message = """

Test Bot!

A bot we can use for testing purposes.

?hello ->
    says hello

?purge ->
    Mass Delete Messages that have key prefixes.
    For testing purposes.

?voice ->
    For joining/leaving the author's voice channel

    Simply joins and leaves the voice channel, for now
    Maybe we can use this to plays songs, potentially?

    Example:

    Me: ?voice
    Bot: Joining Your Voice Channel

    Me: ?voice
    Bot: Leaving Your Voice Channel

?play "words here" ->
	Plays a youtube URL

?help ->
    This message.

"""

help_page =  "```" + help_message + "```"

token = 'NDcyNjk1MTI0MjgzODgzNTQy.Dj3Hfg.QbQrajkO0cH11vG_spUvrAQ6bTk'

# message life time
life_time = 10
