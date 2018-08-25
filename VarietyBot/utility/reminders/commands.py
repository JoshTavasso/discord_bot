'''
commands related to reminders
'''

from discord.ext import commands

class Reminders:

    def __init__(self):
        '''
        Reminders (for now) are set in a 
        dictionary using the author of the command as a key,
        with a list of strings as the value
        '''
        self._reminders = {}   

    #### HELPER FUNCTIONS ####

    def _erase_list(self, author):
        '''
        Empties the list of reminders from a single user
        '''
        if author in self._reminders.keys():
            del self._reminders[author]

    def _erase_entry(self, author, entry):
        '''
        Removes a specific entry from the 
        author's to-do list
        '''
        try:
            self._reminders[author].remove(entry)
        except ValueError:
            return False
        else:
            return True
        finally:
            if len(self._reminders[author]) == 0:
                del self._reminders[author]

    def _get_todo_list(self, author):
        '''
        converts the to-do list into
        a string to display to user
        '''
        todo_list = "```"

        for entry in self._reminders[author]:
            todo_list += "\n" + entry
        todo_list += "```"

        return todo_list

    #### COMMANDS ####
    
    @commands.command(pass_context=True)
    async def note(self, ctx, *args):
        '''
        Checks if a user is registered in the dictionary 
        of reminders, then makes a list for them.
        From then, the message is *args is appended to the 
        list, and the bot responds saying the message was added
        '''
        author = ctx.message.author
        if len(args) == 0:
            return await ctx.bot.say("You didn't note anything")

        if author not in self._reminders.keys():
            self._reminders[author] = []

        self._reminders[author].append(' '.join(args))
        await ctx.bot.say(author.mention + f", I have noted the following: ```{' '.join(args)}```")


    @commands.command(pass_context=True)
    async def todo(self, ctx):
        '''
        Displays the entire list of 
        reminders the user has made note of
        '''
        author = ctx.message.author

        if author not in self._reminders.keys():
            await ctx.bot.say("You haven't created a to-do list!")

        else:
            todo_list = self._get_todo_list(author)
            await ctx.bot.say(f"Your ({author.mention}) to-do list is as follows:") 
            await ctx.bot.say(todo_list)

    @commands.command(pass_context=True)
    async def erase(self, ctx, *args):
        '''
        Erases the entire list of reminders
        '''

        author = ctx.message.author

        if len(args) == 0: 
            return await ctx.bot.say(
                "Please specify what entry from your to-do list that want to erase")
        if author not in self._reminders.keys():
            return await ctx.bot.say("You haven't created a to-do list!")

        entry = ' '.join(args)
        if entry.lower() == 'all':
            self._erase_list(author)
            await ctx.bot.say(f"Your ({author.mention}) to-do list has been cleared!")
        else:
            if self._erase_entry(author, entry):
                await ctx.bot.say(f"'{entry}' has been deleted from your to-do list!")
            else:
                await ctx.bot.say(f"{entry} is not listed in your to-do list!")


def setup(bot):
    bot.add_cog(Reminders())
