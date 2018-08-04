'''
music.py
Contains commands related to music features
'''

# discord.py module
import discord

# discord.py command module
from discord.ext import commands

# Queue to store songs
from utility.Queue import Queue

# youtube functions
import utility.youtube as youtube

class Music:
	def __init__(self, bot):
		# voice object, needed for putting bot in and out 
		# of voice channel
		self.current_voice = None

		# the song player
		self.player = None

		# Eventually set as a dictionary
		# holding video data from the user's
		# latest search
		# key is video title, value is URL
		self.video_data = None

		# The current search that user 
		# asked for
		# Ex: "pokemon black ending theme"
		self.current_search = None

		# The queue which holds the next songs
		# to be played
		# Each "song" in the queue is a list
		# where the first index is the song title
		# and second index is the youtube URL
		self.music_queue = Queue()


	#### HELPER FUNCTIONS ####

	async def _join_voice(self, ctx, channel, to_play = False) -> 'voice object':
	    '''
	    Helper function that joins
	    voice channel
	    for organization purposes since 
	    the process of joining a voice channel
	    is used multiple times

	    returns a voice object, containing info
	    about the voice channel that the bot is
	    currently in
	    '''
	    voice = await ctx.bot.join_voice_channel(channel)
	    if not to_play:
	    	await ctx.bot.say("Joining Your Voice Channel")
	    return voice
    
	async def _leave_voice(self, ctx, to_play = False):
		'''
		Helper function that leaves
		voice channel
		for organization purposes since 
		the process of leaving a voice channel
		is used multiple times
		'''
		if not to_play: 
			await ctx.bot.say("Leaving Your Voice Channel")
		for voice_client in ctx.bot.voice_clients:
			if (voice_client.server == ctx.message.server):
				self.current_voice = None
				return await voice_client.disconnect()

	async def _play_next(self, ctx):
	    '''
	    This function is run when the
	    next song in the queue needs to
	    be played
	    '''
	    member = ctx.message.author
	    channel = member.voice.voice_channel
	    if self.current_voice == None:
	    	self.current_voice = await self._join_voice(ctx, channel)

	    if len(self.music_queue) > 0:
	        video_info = self.music_queue.dequeue()
	        url = video_info[1]
	        await self._play_song(ctx, url)

	    else:
	        await ctx.bot.say('No songs in the Queue!')

	async def _play_from_results(self, ctx, user_choice: int):
		'''
		This function is called when the user inputted
		an input such as: !play 5, meaning they want
		to play a song from the most recent search
		results
		'''

		#first check if search result exists
		if self.current_search == "" or self.current_search == None: 
			return await ctx.bot.say("You didn't specify a search")

		# displaying 10 results for now, so user input
		# needs to be within 1-10
		if user_choice <= 10 and user_choice > 0:
			urls = list(self.video_data.values())
			desired_url = urls[user_choice-1]
			await self._play_song(ctx, desired_url)
		else:
			await ctx.bot.say("That isn't in the video results!")

	async def _play_song(self, ctx, url):
	    '''
	    Given a youtube URL, plays
	    the audio
	    '''
	    if self.player != None:
	        self.player.stop()

	    await ctx.bot.say('...downloading the video')
	    self.player = await self.current_voice.create_ytdl_player(url, ytdl_options=youtube.opts)
	    self.player.start()

	    await ctx.bot.say('{} is playing!'.format(self.player.title))

	async def _display_results(self, ctx, video_data: dict):
	    '''
	    Helper function that
	    displays youtube search results,
	    given a dictionary where the keys 
	    are video titles
	    '''

	    s = "```"
	    for i in range(10):
	        s+="\n{}. {}".format(i+1, list(video_data.keys())[i])
	    s += "\n```"

	    await ctx.bot.say("Here are 10 random results from the first page of results \n" + s)
	    await ctx.bot.say("To play one of these songs, input the command: !play '# of song' ")

	def _format_queue(self, music_queue) -> str:
	    '''
	    given a music queue, formats
	    its contents into a string
	    and returns it
	    '''
	    s = "```"

	    for title,url in music_queue:
	        s+='\n{}'.format(title)
	    s+="\n```"

	    return s


	#### COMMANDS ####

	@commands.command(pass_context = True)
	async def search(self, ctx, *args):
	    '''
	    User specifies key words that
	    they would like the bot to
	    search on youtube, for video
	    results
	    '''

	    self.current_search = ' '.join(args)

	    if self.current_search == '': 
	    	await ctx.bot.say("You didn't specify a search")
	    else:
	    	self.video_data = youtube.front_page_info(self.current_search)
	    	await ctx.bot.say("Your search was accepted!")
	    	await self._display_results(ctx, self.video_data)

	@commands.command(pass_context = True)
	async def results(self, ctx):
	    '''
	    Displays the video results
	    from the latest search 
	    '''

	    if self.video_data == None: 
	    	return await ctx.bot.say("You never searched anything!")

	    await self._display_results(ctx, self.video_data)

	@commands.command(pass_context = True)
	async def playing(self, ctx, *args):
	    '''
	    Lets the user know what song is
	    currently playing
	    '''

	    if self.player == None or self.player.is_done() == True: 
	        return await ctx.bot.say("No song is playing")

	    await ctx.bot.say("Currently playing {}".format(self.player.title))

	@commands.command(pass_context = True)
	async def play(self, ctx, *args):
	    '''
		plays a song from the search results
	    or youtube URL, depending on user input

	    inputting: ?play next:
	    plays next song in queue
	    '''

	    # setup
	    member = ctx.message.author
	    server = ctx.message.server
	    channel = member.voice.voice_channel
	    to_play = False

	    # check if user wants to play next song
	    # in queue
	    try:
	        user_choice = args[0]
	        if user_choice.lower() == 'next':
	        	return await self._play_next(ctx)
	    except IndexError:
	        return await self._play_next(ctx)

	    # Have the bot leave the voice channel
	    # if it is connected, to get rid of the 
	    # the issue of 2 songs being played at once
	    if ctx.bot.is_voice_connected(server): 
	    	to_play = True
	    	await self._leave_voice(ctx, to_play)

	    # Join voice channel, to be able to play audio
	    try:
	        self.current_voice = await self._join_voice(ctx, channel, to_play)
	    except discord.errors.InvalidArgument: 
	        return await ctx.bot.say("You are not in a Voice Channel!")

	    # If the user input is a youtube URL, 
	    # play the song immediately
	    if youtube.is_youtube_url(user_choice):
	        return await self._play_song(ctx, user_choice)

	    # If the user input is not a youtube URL, 
	    # check if the input is an int and check if
	    # it is a valid one.
	    try:
	        user_choice = int(args[0])
	    except ValueError:
	        await ctx.bot.say("Please use !search to search for a song,")
	        return await ctx.bot.say("and then choose a song from !results")

	    # if the program made it here, the user
	    # must want to play something from the 
	    # most recent search result
	    await self._play_from_results(ctx, user_choice)

	@commands.command(pass_context = True)
	async def stop(self, ctx):
	    '''
	    Stops the song that is currently
	    playing
	    '''

	    if self.player != None and self.current_voice != None:
	        self.player.stop()
	        await ctx.bot.say('Stopped the song')

	        # play next song in queue
	        await self._play_next(ctx)

	    else: 
	        await ctx.bot.say('No song is playing!')

	@commands.command(pass_context = True)
	async def queue(self, ctx):
	    '''
	    Displays contents of the
	    music queue
	    '''
	    await ctx.bot.say(self._format_queue(self.music_queue))

	@commands.command(pass_context = True)
	async def enqueue(self, ctx, *args):
	    '''
	    Adds a song to the end of
	    the music queue
	    '''
	    try:
	        song = args[0]
	        if not youtube.is_youtube_url(song):
	            song = int(args[0]) - 1
	            if self.video_data == None: 
	                return await ctx.bot.say("You didn't search for anything")
	    except ValueError:
	        return await ctx.bot.say("Please give me an integer, or a valid video URL")
	    except IndexError:
	        return await ctx.bot.say("You didn't specify a song to add")
		
	    urls = list(self.video_data.values())
	    titles = list(self.video_data.keys())

	    url = urls[song] if type(song) == int else song
	    title = titles[song] if type(song) == int else song

	    self.music_queue.enqueue([title,url])
	    
	    await ctx.bot.say("Enqueued {}!".format(title))

	@commands.command(pass_context=True)
	async def clearqueue(self, ctx, *args):
	    '''
	    clears the queue, if desired
	    '''
	    self.music_queue.clear()
	    await ctx.bot.say("Queue is now empty!")

	@commands.command(pass_context=True)
	async def join(self, ctx):
	    ''' 
	    Joins the voice channel that
	    the user is in
	    '''
	    server = ctx.message.server
	    channel = ctx.message.author.voice_channel

	    if not ctx.bot.is_voice_connected(server):
	        try:
	            self.current_voice = await self._join_voice(ctx, channel)
	        except discord.errors.InvalidArgument: 
	            return await ctx.bot.say("You are not in a Voice Channel!")
	    else: 
	        await ctx.bot.say("I am already in a Voice Channel!")

	@commands.command(pass_context=True)
	async def leave(self, ctx):
	    '''
	    Leaves the voice channel that
	    the user is in
	    '''
	    server = ctx.message.server
	    if ctx.bot.is_voice_connected(server): 
	        await self._leave_voice(ctx)
	    else: 
	        await ctx.bot.say("How can I leave when I am not even in a Voice Channel boi?")

# adds music class to command bot
def setup(bot):
    bot.add_cog(Music(bot))
