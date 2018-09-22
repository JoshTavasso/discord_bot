'''
contains voice commands

Based on the discord.py music example
found @ https://github.com/Rapptz/discord.py/blob/master/examples/playlist.py

'''
# module for Asynchronous funtions
import asyncio

# discord.py module
import discord

# discord command module
from discord.ext import commands

# youtube functions
import utility.voice.youtube as youtube

# voice objects
from utility.voice.VoiceObjects import VoiceEntry, VoiceState

class VoiceCommands:
    '''
    Music/Voice Commands
    '''

    def __init__(self, bot):
        self.bot = bot

        # dict of voice states for hosting bot on multiple servers
        self.voice_states = {} 

    #### HELPER FUNCTIONS ####

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

        await ctx.bot.say("Here are 10 random results from the first page of youtube search results \n" + s)
        await ctx.bot.say("To play one of these songs, input the command: {}play '# of song' ".format(ctx.bot.command_prefix))

    async def _display_queue(self, ctx, music_queue):
        '''
        Helper function that,
        given a music queue,
        displays the contents
        of it
        '''

        s = "```"
        for title in music_queue:
            s+='\n{}'.format(title)
        s+="\n```"

        await ctx.bot.say(s)

    async def _join_voice(self, ctx, channel) -> 'voice object':
        '''
        Helper function that joins
        voice channel

        returns a voice object, containing info
        about the voice channel that the bot is
        currently in
        '''
        voice = await ctx.bot.join_voice_channel(channel)
        await ctx.bot.say("Joining Your Voice Channel")
        return voice

    async def _song_error_msg(self, ctx, error: str) -> None:
        '''
        This function is called if the user input for
        playing a song is invalid

        Bot sends the user error messages depending on
        what type of error was made

        Returns None to represent that the user's input
        was invalid
        '''
        if error == 'ValueError':
            await ctx.bot.say("Please use the search command to search for a song,")
            await ctx.bot.say("and then choose a song from the search results")
            await ctx.bot.say("Or, alternatively, you can give me a youtube url and I can play it for you")

        elif error == 'NoSearch':
        	await ctx.bot.say("You didn't specify a search")

        elif error == 'NotInResults':
        	await ctx.bot.say("That isn't in the video results!")

        return None

    async def _get_song_choice(self, ctx, args) -> 'url or None':
        '''
        checks user input and returns
        either a song url or None, 
        depending on whether the user
        input is valid or not
        '''

        # current voice state
        state = self._get_voice_state(ctx.message.server)

        # check if user input is a number
        try:
            user_choice = int(args[0])
        except ValueError:
            return await self._song_error_msg(ctx, 'ValueError')

        # check if the user actually made a search
        if state.current_search == "" or state.current_search == None: 
        	return await self._song_error_msg(ctx, 'NoSearch')

        # Only allowing 10 results for now, so user input
        # needs to be within 1-10
        if user_choice < 11 and user_choice > 0:
            urls = list(state.video_data.values())
            song = urls[user_choice-1]
            return song
        else:
        	return await self._song_error_msg(ctx, 'NotInResults')

    async def _enqueue_song(self, ctx, song: 'url', state, opts: 'json'):
        '''
        Enqueues a new music player into the queue of
        Voice Entries (music players). 

        The automated task involved with the VoiceState
        object, located in the VoiceObjects module,
        takes care of actually playing the song
        and waiting for the next one in the queue
        '''
        player = await state.voice.create_ytdl_player(song, ytdl_options=opts, 
                                                            after=state.toggle_next)
        entry = VoiceEntry(ctx.message, player)
        await ctx.bot.say('Enqueued ' + str(entry))
        await state.songs.put(entry)
        state.music_queue.enqueue(entry.player.title)

    def _get_voice_state(self, server):
        '''
        Gets the VoiceState object which 
        contains all info about what song
        is currently playing, what song 
        should be played next, etc. 
        Check out the VoiceObjects module
        '''
        state = self.voice_states.get(server.id)
        if state == None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    #### COMMANDS ####

    @commands.command(pass_context = True)
    async def search(self, ctx, *args):
        '''
        User specifies key words that
        they would like the bot to
        search on youtube, for video
        results
        '''

        # current voice state
        state = self._get_voice_state(ctx.message.server)

        state.current_search = ' '.join(args)

        if state.current_search == '': 
            await ctx.bot.say("You didn't specify a search")
        else:
            await ctx.bot.say("Searching...")
            state.video_data = youtube.front_page_info(state.current_search)
            await self._display_results(ctx, state.video_data)

    @commands.command(pass_context = True)
    async def results(self, ctx):
        '''
        Displays the video results
        from the latest search 
        '''

        # current voice state
        state = self._get_voice_state(ctx.message.server)

        if state.video_data == None: 
            return await ctx.bot.say("You never searched anything!")

        await self._display_results(ctx, state.video_data)

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *args):

        # voice channel
        channel = ctx.message.author.voice.voice_channel

        # current voice state
        state = self._get_voice_state(ctx.message.server)

        # parse user input
        # if index error, the command_error
        # function in script.py should
        # cover this, giving the user
        # the help page
        song = args[0]

        # options for youtube downloading
        opts = youtube.opts

        # Join Voice Channel
        if state.voice == None:
            state.voice = await self._join_voice(ctx, channel)


        # If the user input is not a youtube URL, 
        # check if the input valid 
        if not youtube.is_youtube_url(song):
            song = await self._get_song_choice(ctx, args)
            if song == None:
                return
        await self._enqueue_song(ctx, song, state, opts)

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        '''
        Stops the song that is currently
        playing
        '''
        server = ctx.message.server
        state = self._get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()
            await ctx.bot.say('Stopped the song')

        else: 
            await ctx.bot.say('No song is playing!')

    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        '''
        Shows info about the currently played song.
        '''

        state = self._get_voice_state(ctx.message.server)
        if state.current == None or state.current.player.is_done():
            await self.bot.say('Not playing anything.')
        else:
            await self.bot.say('Now playing {}'.format(state.current))

    @commands.command(pass_context=True)
    async def queue(self, ctx):
        '''
        displays the queue of songs
        '''
        state = self._get_voice_state(ctx.message.server)
        await self._display_queue(ctx, state.music_queue)

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
                state = self._get_voice_state(server)
                state.voice = await self._join_voice(ctx, channel)
            except discord.errors.InvalidArgument: 
                return await ctx.bot.say("You are not in a Voice Channel!")
        else: 
            await ctx.bot.say("I am already in a Voice Channel!")

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        '''
        Leaves the voice channel that
        the user is in and clears the 
        music queue
        '''
        server = ctx.message.server
        state = self._get_voice_state(server)

        state.audio_player.cancel()
        del self.voice_states[server.id]
        await state.voice.disconnect()
        await ctx.bot.say("Left voice channel and cleared music queue")


def setup(bot):
    bot.add_cog(VoiceCommands(bot))