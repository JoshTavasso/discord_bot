import discord
import random
from discord.ext import commands

BOT_PREFIX = '&'
TOKEN = "NDcxNzkxNDgxNTMxNjYyMzM3.Dj589w.JT1galpWvN67pex0iOldHdcUhps"

# Reminders (for now) are set in a dictionary using the author of the command as a key,
# with a list of strings as the value
REMINDERS = {}

bot = commands.Bot(command_prefix=BOT_PREFIX)

# adds the test.py commands
bot.load_extension('test')

bot.remove_command('help')


def erase_list(author):
    '''
    Empties the list of reminders from a single user
    '''
    if author in REMINDERS.keys():
        REMINDERS[author] = []


# COMMANDS #


@bot.command(pass_context=True)
async def help(ctx):
    '''
    Displays the help message
    '''
    help_message = '''
tahm test bot

Tom's testing bot.

&hello
    -Says hello.

&purge
    -Purges the following:
        -All commands (!, ?, &)
        -Any empty messages
        -Any text-formatted messages
        
&nick
    -Picks a random nickname.
    -(Coming Soon) Sets nickname
        
&board
    -Creates a Tic-Tac-Toe board.
    
&move
    -Places an X or an O on a space.
    -Format: ROW_NUMBER COL_NUMBER
        -Example: &board 1 1
        
&reset
    -Resets/Clears the board.

&help
    -Shows this message.'''
    help_message_formatted = "```" + help_message + "```"
    await ctx.bot.say(help_message_formatted)


@bot.command(pass_context=True)
async def hello(ctx):
    '''
    Bot responds with "Hello" and mentions the author
    '''
    author = ctx.message.author
    await ctx.bot.say("Hello " + author.mention)


@bot.command(pass_context=True)
async def purge(ctx):
    '''
    Purges any commands beginning with '!', '?', or '&', empty messages, or text-formatted ones (```these```)
    '''
    channel = ctx.message.channel
    check = lambda msg: msg.content == "" or msg.content[0] in ['!', '?', '&'] or msg.content[:3] == "```"

    await ctx.bot.purge_from(channel, limit=1000, check=check)    
    await ctx.bot.say("Purge Complete", delete_after=10)

"""
@bot.command(pass_context=True)
async def board(ctx):
    '''
    Displays the current board
    '''
    await ctx.bot.say(board_display())


@bot.command(pass_context=True)
async def reset(ctx):
    '''
    Resets and clears the entire board
    '''
    clear()
    await ctx.bot.say("Board Reset!")


@bot.command(pass_context=True)
async def move(ctx, *args):
    '''
    Checks if a cell is empty at a given coordinate, then if it is, inserts an X or an O
    '''
    r = int(args[0]) - 1
    c = int(args[1]) - 1
    if BOARD[r][c] == E:
        place(r, c)
        switch()
    else:
        await ctx.bot.say(f"Space ({r}, {c}) is already taken!")
    await ctx.bot.say(board_display()) 
"""


@bot.command(pass_context=True)
async def nick(ctx):
    '''
    STILL IN DEVELOPMENT
    Randomly chooses among a list of nicknames and changes author's nickname to it
    '''
    author = ctx.message.author
    nicks = [
        "Needed a New Nickname",
        "Melon Lord",
        "GOAT",
        "Barack Obama",
        "John Cena"
    ]
    new_nick = random.choice(nicks)
    try:
        await ctx.bot.say(f"You have been knighted as {new_nick}, " + author.mention)
        await ctx.bot.change_nickname(author, new_nick)
    except discord.Forbidden:
        await ctx.bot.say("However, I do not seem to have the rights to change your name.")

@bot.command(pass_context=True)
async def note(ctx, *args):
    '''
    Checks if a user is registered in the dictionary of reminders, then makes a list for them
    From then, the message is *args is appended to the list, and the bot responds saying the message was added
    '''
    author = ctx.message.author
    if author not in REMINDERS.keys():
        REMINDERS[author] = []
    REMINDERS[author].append(' '.join(args))
    await ctx.bot.say(author.mention + f", I have noted the following: ```{' '.join(args)}```")


@bot.command(pass_context=True)
async def todo(ctx):
    '''
    Displays the entire list of reminders the user has made note of
    '''
    author = ctx.message.author
    await ctx.bot.say(author.mention + f", your to-do list is as follows: ```{', '.join(REMINDERS[author])}```")


@bot.command(pass_context=True)
async def erase(ctx):
    '''
    Erases the entire list of reminders
    '''
    author = ctx.message.author
    erase_list(author)
    await ctx.bot.say(author.mention + ", your to-do list has been cleared!")


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')    

bot.run(TOKEN)
