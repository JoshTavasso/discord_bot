import discord
import random
from discord.ext import commands

BOT_PREFIX = '&'
TOKEN = "NDcxNzkxNDgxNTMxNjYyMzM3.Dj589w.JT1galpWvN67pex0iOldHdcUhps"

E = ' '
X = 'X'
O = 'O'
BOARD = [
    [E, E, E],
    [E, E, E],
    [E, E, E]
    ]
FIRST = X

REMINDERS = {}

bot = commands.Bot(command_prefix=BOT_PREFIX)

bot.remove_command('help')


@bot.command(pass_context=True)
async def help(ctx):
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
    author = ctx.message.author
    await ctx.bot.say("Hello " + author.mention)


@bot.command(pass_context=True)
async def purge(ctx):
    channel = ctx.message.channel
    check = lambda msg: msg.content == "" or msg.content[0] in ['!', '?', '&'] or msg.content[:3] == "```"

    await ctx.bot.purge_from(channel, limit=1000, check=check)    
    await ctx.bot.say("Purge Complete", delete_after=10)


def board_display():
    board = f'''
   TIC  TAC  TOE

     1   2   3
   -------------
 1 | {BOARD[0][0]} | {BOARD[0][1]} | {BOARD[0][2]} |
   -------------
 2 | {BOARD[1][0]} | {BOARD[1][1]} | {BOARD[1][2]} |
   -------------
 3 | {BOARD[2][0]} | {BOARD[2][1]} | {BOARD[2][2]} |
   -------------
'''
    return "```" + board + "```"


def clear():
    for row in range(3):
        for col in range(3):
            BOARD[row][col] = E


def place(r, c):
    BOARD[r][c] = FIRST


def switch():
    global FIRST
    if FIRST == X:
        FIRST = O
    else:
        FIRST = X


@bot.command(pass_context=True)
async def board(ctx):
    await ctx.bot.say(board_display())


@bot.command(pass_context=True)
async def reset(ctx):
    clear()
    await ctx.bot.say("Board Reset!")


@bot.command(pass_context=True)
async def move(ctx, *args):
    r = int(args[0]) - 1
    c = int(args[1]) - 1
    if BOARD[r][c] == E:
        place(r, c)
        switch()
    else:
        await ctx.bot.say(f"Space ({r}, {c}) is already taken!")
    await ctx.bot.say(board_display())


@bot.command(pass_context=True)
async def nick(ctx):
    author = ctx.message.author
    nicks = [
        "Needed a New Nickname",
        "Melon Lord",
        "GOAT"
    ]
    new_nick = random.choice(nicks)
    await ctx.bot.change_nickname(author, new_nick)
    await ctx.bot.say(f"You have been knighted as {new_nick}, " + author.mention)


def erase_list(author):
    if author in REMINDERS.keys():
        REMINDERS[author] = []


@bot.command(pass_context=True)
async def note(ctx, *args):
    author = ctx.message.author
    if author not in REMINDERS.keys():
        REMINDERS[author] = []
    REMINDERS[author].append(' '.join(args))
    await ctx.bot.say(author.mention + f", I have noted the following: ```{' '.join(args)}```")


@bot.command(pass_context=True)
async def todo(ctx):
    author = ctx.message.author
    await ctx.bot.say(author.mention + f", your to-do list is as follows: ```{', '.join(REMINDERS[author])}```")


@bot.command(pass_context=True)
async def erase(ctx):
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
