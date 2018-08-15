'''
script.py
The main file that executes the bot
'''

# discord.py module
import discord

# discord.py command module
from discord.ext import commands

# data needed for bot
from utility.general.data import default_prefix, help_page, token, bot_extensions

# discord command bot
bot = commands.Bot(command_prefix=default_prefix)

# Remove default help command 
# to create a better one
bot.remove_command('help')

# load all of our commands
for ext in bot_extensions:
    bot.load_extension(ext)

async def _send_welcome_msg(server):
    '''
    Sends welcome message to server
    '''
    for channel in server.channels:
        if (str(channel) == 'general'):
            return await bot.send_message(
                channel, "Hello There! Use {}help to see what I do!".format(default_prefix))

@bot.event
async def on_server_join(server):
    '''
    Gives the server a welcome message
    when the bot first joins a server
    '''
    await _send_welcome_msg(server)

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
            help_page(ctx.bot.command_prefix)))

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

    await _send_welcome_msg(list(bot.servers)[0])

if __name__ == '__main__':
	bot.run(token)
