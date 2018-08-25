import discord
from discord.ext import commands

prefix = '?'
token = 'NDcyNjk1MTI0MjgzODgzNTQy.Dj3Hfg.QbQrajkO0cH11vG_spUvrAQ6bTk'
life_time = 10
bot_extensions = []
bot = commands.Bot(command_prefix=prefix)

@bot.command(pass_context=True)
async def purge(ctx, *args):
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
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    
if __name__ == '__main__':
	bot.run(token)
