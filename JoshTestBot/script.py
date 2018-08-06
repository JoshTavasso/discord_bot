'''
script.py
The main file that executes the bot
'''

# discord.py module
import discord

# discord.py command module
from discord.ext import commands

# data needed for bot
from utility.data import prefix, token, bot_extensions

# discord command bot
bot = commands.Bot(command_prefix=prefix)

# load all of our commands
for ext in bot_extensions:
    bot.load_extension(ext)

@bot.event
async def on_ready():
    ''' 
    To know if the bot has launched or not 
    '''
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
if __name__ == '__main__':
	bot.run(token)
