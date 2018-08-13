'''
emoji commands

commands that deal with emojis
'''

# discord.py command module
from discord.ext import commands

# needed for extracting message attachments
import aiohttp

class Emoji:
    async def _get_image(self, url: str) -> 'string of image bytes':
        '''
        retrieves image given a url to
        of an image
        '''
        async with aiohttp.get(url) as response:
            if response.status == 200:
                return await response.read()

    def _save_image(self, image:'string of image bytes'):
        file = open('utility/emoji/img.png', 'wb')
        file.write(image)
        file.close()

    async def _create_emoji(self, ctx, msg_info: dict, emoji_name: str, server):
        img = await self._get_image(msg_info['url'])
        self._save_image(img)
        img_file = open('utility/emoji/img.png', 'rb')
        await ctx.bot.create_custom_emoji(server, name = emoji_name, image = img_file.read())
        await ctx.bot.say(f"{emoji_name} emoji created!")
        img_file.close()

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
        server = ctx.message.server
        for e in server.emojis:
            if name == e.name:
                await ctx.bot.delete_custom_emoji(e)
                return await ctx.bot.say(f"{name} deleted")

        await ctx.bot.say(f"{name} doesn't exist")

# adds general class to command bot
def setup(bot):
    bot.add_cog(Emoji())
