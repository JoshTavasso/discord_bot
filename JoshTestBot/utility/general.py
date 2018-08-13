'''
general.py

contains general commands 
'''

# discord.py module
import discord

# discord.py command module
from discord.ext import commands

# data needed for bot
from utility.data import prefix, life_time

class General:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def purge(self, ctx, *args):
        '''
        Mass Delete Messages.
        For testing purposes

        Ex uses:
        !purge
        -> deletes every message that starts with '!'

        !purge all
        -> deletes all messages in channel

        !purge cool
        -> deletes every message that has 'cool' in it
        '''

        channel = ctx.message.channel
        if len(args) == 0:
        	check = lambda msg: msg.content == "" or msg.content[0] == prefix
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