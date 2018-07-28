import discord
from discord.ext import commands

BOT_PREFIX = ('&')
TOKEN = "NDcxNzkxNDgxNTMxNjYyMzM3.Dj589w.JT1galpWvN67pex0iOldHdcUhps"

E = '.'
X = 'X'
O = 'O'
BOARD = [
    [E, E, E],
    [E, E, E],
    [E, E, E]
    ]

bot = commands.Bot(command_prefix=BOT_PREFIX)

bot.remove_command('help')

@bot.command(pass_context=True)
async def help(ctx):
    help_message ='''
tahm test bot

tahm's testing bot.

&hello
    -Says hello.

&purge
    -Purges the following:
        -All commands (!, ?, &)
        -Any empty messages
        -Any text-formatted messages

&help
    -Shows this message.'''
    H = "```" + help_message + "```"
    await ctx.bot.say(H)

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
    BOARD[r][c] = X

@bot.command(pass_context=True)
async def board(ctx):
    await ctx.bot.say(board_display())

@bot.command(pass_context=True)
async def reset(ctx):
    clear()
    await ctx.bot.say("Board Reset!")

'''
@bot.command(pass_context=True)
async def move(ctx):
    
    await ctx.bot.say(board())
'''

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')    

bot.run(TOKEN)
