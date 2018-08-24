'''
VoiceObjects.py

Voice objects used for voice commands

Based on the discord.py music example
found @ https://github.com/Rapptz/discord.py/blob/master/examples/playlist.py

'''

# module for Asynchronous functions
import asyncio

# discord.py module
import discord

# Queue implementation
from utility.voice.Queue import Queue


class VoiceEntry:
    '''
    A VoiceEntry represents a 'song' object
    '''
    def __init__(self, message, pleayer):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        '''
        A VoiceState deals with
        VoiceEntry objects. Uses
        the VoiceEntries to play and
        store songs
        '''
        # current VoiceEntry
        self.current = None

        # discord.py voice object
        self.voice = None

        # discord command bot
        self.bot = bot

        # Asyncio event that deals with playing next song
        self.play_next_song = asyncio.Event()

        # the current search that was made
        self.current_search = None

        # a dictionary of youtube search results
        # where the key represents a video title
        # and the value represents the video url
        self.video_data = None

        # Queue of VoiceEntries
        self.songs = asyncio.Queue()

        # Queue of Song titles
        self.music_queue = Queue()

        # Deals with playing/waiting for next song
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self) -> bool:
        '''
        returns boolean on whether a song is playing
        currently
        '''
        if self.voice == None or self.current == None:
            return False
        return not self.current.player.is_done()

    @property
    def player(self):
        '''
        returns the music player object
        '''
        return self.current.player

    def toggle_next(self):
        '''
        plays next song
        '''
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        '''
        An ongoing loop that waits for 
        the song to be finished, and plays
        the next song in the queue
        '''
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            self.music_queue.dequeue()
            await self.bot.send_message(self.current.channel, 'Now playing ' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()