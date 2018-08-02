#### IMPORTS ####

# discord.py module
import discord

# discord.py command module
from discord.ext import commands

'''
Testing using a separate file 
for commands

This is the general format:
'''
class test:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def yo(self, ctx):
        await self.bot.say('yo')

    @commands.command(pass_context = True)
    async def sup(self, ctx):
        await self.bot.say('sup')

def setup(bot):
    bot.add_cog(test(bot))