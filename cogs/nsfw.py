import discord
from discord.ext import commands
import aiohttp

butt = 'http://media.obutts.ru/'
boob = 'http://media.oboobs.ru/'

class NSFW():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def boobs(self,ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://api.oboobs.ru/noise/1') as r:
                if r.status == 200:
                    js = await r.json()
                    em = discord.Embed(description='')
                    em.set_image(url=boob + js[0]['preview'])
                    await self.bot.say(embed=em)

    @commands.command()
    async def butt(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://api.obutts.ru/noise/1') as r:
                if r.status == 200:
                    js = await r.json()
                    em = discord.Embed(description='')
                    em.set_image(url=butt + js[0]['preview'])
                    await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(NSFW(bot))
