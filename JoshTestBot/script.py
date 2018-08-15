'''
script.py
The main file that executes the bot
'''

# discord.py module
import discord

# discord.py command module
from discord.ext import commands

prefix = '?'

token = 'NDcyNjk1MTI0MjgzODgzNTQy.Dj3Hfg.QbQrajkO0cH11vG_spUvrAQ6bTk'

# message life time
life_time = 10

bot_extensions = []

# discord command bot
bot = commands.Bot(command_prefix=prefix)

# load all of our commands
for ext in bot_extensions:
    bot.load_extension(ext)

@bot.event
async def on_server_join(server):
	for channel in server.channels:
		if (str(channel) == 'general'):
			return await bot.send_message(channel, "Hello There! Use {}help to see what I do!".format(prefix))

@bot.command(pass_context=True)
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
