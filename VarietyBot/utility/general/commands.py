'''
contains general commands 
'''

# discord.py module
import discord

# discord.py command module
from discord.ext import commands

# data needed for bot
from utility.general.data import life_time

# helper functions
from utility.general.helper import help_page, emoji_help, music_help

class General:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def help(self, ctx, *args):
        '''
        Displays Help Page
        '''

        prefix = ctx.bot.command_prefix

        if len(args) == 0:
            await ctx.bot.say(help_page(prefix))
            
        elif args[0] == 'music':
            await ctx.bot.say(music_help(prefix))

        elif args[0] == 'emoji':
            await ctx.bot.say(emoji_help(prefix))

    @commands.command(pass_context = True)
    async def prefix(self, ctx, *args):
        '''
        changes the prefix 
        of the bot
        '''

        if len(args) == 0:
            return await ctx.bot.say("Please specify a prefix")

        ctx.bot.command_prefix = args[0]
        await ctx.bot.say(f"Prefix now set to {ctx.bot.command_prefix}")
    
    @commands.command(pass_context=True)
    async def purge(self, ctx, *args):
        '''
        Mass Delete Messages.
        For testing purposes

        Ex uses:
        purge
        -> deletes every message that starts with '!'

        purge all
        -> deletes all messages in channel

        purge cool
        -> deletes every message that has 'cool' in it
        '''

        channel = ctx.message.channel
        if len(args) == 0:
        	check = lambda msg: msg.content == "" or msg.content[0] == ctx.bot.command_prefix
        	await ctx.bot.purge_from(channel, limit=1000, check=check)
        elif args[0].lower() == 'all':
        	await ctx.bot.purge_from(channel, limit=1000)
        else:
        	thing_to_delete = ' '.join(args)
        	check = lambda msg: msg.content == "" or thing_to_delete.lower() in msg.content.lower()
        	await ctx.bot.purge_from(channel, limit=1000, check=check)
        await ctx.bot.say("Purge Complete", delete_after=life_time)

# adds general class to command bot
def setup(bot):
    bot.add_cog(General(bot))