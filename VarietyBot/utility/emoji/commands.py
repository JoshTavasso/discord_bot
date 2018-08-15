'''
commands that deal with emojis
'''

# discord.py command module
from discord.ext import commands

# needed for extracting message attachments
import aiohttp

class Emoji:

    #### HELPER FUNCTIONS ####

    async def _get_image_info(self, url: str) -> 'string of image bytes':
        '''
        retrieves image info given a url to
        an image
        '''
        async with aiohttp.get(url) as response:
            if response.status == 200:
                return await response.read()

    async def _create_emoji(self, ctx, msg_info: dict, emoji_name: str, server):
        '''
        Given a dictionary of info regarding the user's
        message attachments, this function retrieves 
        info of the attachment (assuming it is a jpg or
        png file), and creates a custon emoji using the file
        '''
        img_info = await self._get_image_info(msg_info['url'])
        await ctx.bot.create_custom_emoji(server, name = emoji_name, image = img_info)
        await ctx.bot.say(f"{emoji_name} emoji created!")

    #### COMMANDS ####

    @commands.command(pass_context=True)
    async def emoji(self, ctx, *args):
        '''
        given an image, this command
        converts it into an emoji
        '''

        if len(args) == 0: 
            return await ctx.bot.say("Please specify an emoji name")

        if len(ctx.message.attachments) == 0:
            return await ctx.bot.say("Please give me an image in jpg or png format")

        else:
            await ctx.bot.say('creating emoji...')
            await self._create_emoji(ctx,
                                    ctx.message.attachments[0],
            						args[0],
            						ctx.message.server)

    @commands.command(pass_context=True)
    async def remove(self, ctx, name):
        '''
        Removes the specified emoji
        '''
        
        server = ctx.message.server
        for e in server.emojis:
            if name == e.name:
                await ctx.bot.delete_custom_emoji(e)
                return await ctx.bot.say(f"{name} deleted")

        await ctx.bot.say(f"{name} doesn't exist")

# adds general class to command bot
def setup(bot):
    bot.add_cog(Emoji())
