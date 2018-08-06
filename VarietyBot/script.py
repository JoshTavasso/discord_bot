'''
script.py
The main file that executes the bot
'''

# discord.py module
import discord

# discord.py command module
from discord.ext import commands

# data needed for bot
from utility.data import prefix, help_page, token, bot_extensions

# discord command bot
bot = commands.Bot(command_prefix=prefix)

# Remove default help command 
# to create a better one
bot.remove_command('help')

# load all of our commands
for ext in bot_extensions:
    bot.load_extension(ext)

'''
Error message is commented out for now
so we can see the errors in our terminal
while debugging
This will be uncommented once bot is completely finished
'''
"""
@bot.event
async def on_command_error(error, ctx):
    '''
    For if a user says a wrong command, or
    an error occurs when a command is inputted.
    This gives them the help page
    '''
    await bot.send_message(ctx.message.channel, "An error occured, maybe you inputted a wrong command\n{}".format(help_page))
"""

@bot.event
async def on_ready():
    ''' 
    To know if the bot has launched or not 
    '''
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    
    # greet the server
    for server in bot.servers: 
        for channel in server.channels:
        	try: 
	            if channel.permissions_for(server.me).send_messages:
	                await bot.send_message(channel, "Hello There! Use {}help to see what I do!".format(prefix))
	                break
	        except discord.errors.HTTPException:
	        	pass

if __name__ == '__main__':
	bot.run(token)
