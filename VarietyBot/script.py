'''
script.py
The main file that executes the bot
'''

# discord.py module
import discord

# discord.py command module
from discord.ext import commands

# data needed for bot
from utility.general.data import default_prefix, token, bot_extensions

# helper functions
from utility.general.helper import help_page, send_welcome_msg

# discord command bot
bot = commands.Bot(command_prefix=default_prefix)

# Remove default help command 
# to create a better one
bot.remove_command('help')

# load all of our commands
for ext in bot_extensions:
    bot.load_extension(ext)

@bot.event
async def on_server_join(server):
    '''
    Gives the server a welcome message
    when the bot first joins a server
    '''
    await send_welcome_msg(bot, server)
"""
@bot.event
async def on_command_error(error, ctx):
    '''
    For if a user says a wrong command, or
    an error occurs when a command is inputted.
    This gives them the help page
    '''
    await bot.send_message(ctx.message.channel, 
        "An error occured, maybe you inputted a wrong command.")
    await bot.send_message(ctx.message.channel, 
        "Here is the Help Page:\n{}".format(
            help_page(ctx.bot.command_prefix)))"""

@bot.event
async def on_ready():
    ''' 
    To know if the bot has launched or not 
    For testing purposes
    '''
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    #await send_welcome_msg(bot, list(bot.servers)[0])

if __name__ == '__main__':
	bot.run(token)
