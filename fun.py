import discord
from discord.ext import commands
import aiohttp
import random
import checks
import config
import json
import time

with open('configuration.json', 'r+') as f:
    configuration = json.load(f)

def file_updating():
    with open('configuration.json', 'w') as a:
        json.dump(configuration, a, indent=4)

class Fun():
    """
    Some fun-only commands.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        pingtime = time.time()
        pingms = await self.bot.say("Pinging... `{}'s` location".format(ctx.message.author.mention))
        ping = time.time() - pingtime
        await self.bot.edit_message(pingms, "The ping time is `{} ms`".format(ping))


    @commands.command(pass_context=True)
    async def poll(self,ctx, *, poll):
        """Creates a poll with the text you've written.\n Example: !poll Do you like memes?"""
        msg = await self.bot.say(poll)
        await self.bot.add_reaction(msg, '\U0001F44D')  # like
        await self.bot.add_reaction(msg, '\U0001F44E')  # dislike

    @commands.command()
    async def cat(self):
        """Sends a cat picture"""
        async with aiohttp.ClientSession() as session:
            async with session.get('http://aws.random.cat/meow') as r:
                if r.status == 200:
                    js = await r.json()
                    em = discord.Embed(description='')
                    em.set_image(url=js['file'])
                    await self.bot.say(embed=em)

    @commands.command()
    async def dog(self):
        """Sends a dog picture"""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://random.dog/woof.json') as r:
                if r.status == 200:
                    js = await r.json()
                    em = discord.Embed(description='')
                    em.set_image(url=js['url'])
                    await self.bot.say(embed=em)

    @commands.command()
    async def roll(self, x: int = None):
        """Rolls a number from 1 to 100(by default). Can be changed. \nExample: !roll 500"""
        if x is None:
            x = 100
        await self.bot.say(random.randint(1, int(x)))

    @commands.command(name="8ball")
    async def _8ball(self):
        await self.bot.say(random.choice(config.choice))

    @commands.command(aliases=['asian', 'бурятка'])
    async def _asian(self):
        """Sends photos of some girls."""
        f = open('asians.txt', 'r')
        a = list(f)
        em = discord.Embed(description='')
        em.set_image(url=random.choice(a))
        await self.bot.say(embed=em)
        f.close()


    @commands.command(pass_context = True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx,*,number):
        """Deletes a given amount of messages. Requires permissions for the bot."""
        try:
            mgs = []  # Empty list to put all the messages in the log
            number = int(number)  # Converting the amount of messages to delete to an integer
            async for x in self.bot.logs_from(ctx.message.channel, limit=number):
                mgs.append(x)
            await self.bot.delete_messages(mgs)
            msg = await self.bot.say('Удалено `'+str(number)+'` сообщений.')
        except discord.errors.Forbidden:
            await self.bot.say('`Нет доступа`')

    @commands.command(pass_context = True)
    async def kiss(self, ctx, user : discord.User):
        """Kisses user."""
        em = discord.Embed(description='{} just kissed {} :flushed:'.format(ctx.message.author.mention, user.mention))
        em.set_image(url=random.choice(config.kiss))
        await self.bot.say(embed=em)


    @commands.command(pass_context = True)
    async def hug(self, ctx, user : discord.User):
        """Gives a hug to user."""
        em = discord.Embed(description='{} hugs {} :relaxed: '.format(ctx.message.author.mention, user.mention))
        em.set_image(url=random.choice(config.hug))
        await self.bot.say(embed=em)


    @commands.command(pass_context = True)
    async def punch(self,ctx, user : discord.User):
        """Punches a user."""
        em = discord.Embed(description='{} just punched {}!'.format(ctx.message.author.mention, user.mention))
        em.set_image(url=random.choice(config.punch))
        await self.bot.say(embed=em)


    @commands.command(pass_context = True)
    async def kill(self,ctx, user : discord.User):
        """Kills a user."""
        em = discord.Embed(description='{} just killed {}!'.format(ctx.message.author.mention, user.mention))
        em.set_image(url=random.choice(config.kill))
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def кнб(self, ctx, user_choice):
        """Камень, ножницы, бумага """
        bot_choice = random.choice(['камень','ножницы','бумага'])
        user_choice = user_choice.lower()
        if bot_choice == user_choice:
            await self.bot.say('Ничья! Я выбрал `'+bot_choice+'`, как и ты!')
        elif user_choice == 'камень' and bot_choice =='ножницы':
            await self.bot.say('Вы выиграли! Я выбрал `'+bot_choice+'`.')
        elif user_choice == 'ножницы' and bot_choice == 'камень':
            await self.bot.say('Вы проиграли! Вы выбрали `'+user_choice+'`, когда я выбрал `'+bot_choice+'`')
        elif user_choice == 'бумага' and bot_choice == 'ножницы':
            await self.bot.say('Вы проиграли! Вы выбрали `'+user_choice+'`, когда я выбрал `'+bot_choice+'`')
        elif user_choice == 'ножницы' and bot_choice == 'бумага':
            await self.bot.say('Вы выиграли! Я выбрал `' + bot_choice + '`.')
        elif user_choice == 'камень' and bot_choice == 'бумага':
            await self.bot.say('Вы проиграли! Вы выбрали `'+user_choice+'`, когда я выбрал `'+bot_choice+'`')
        elif user_choice == 'бумага' and bot_choice == 'камень':
            await self.bot.say('Вы выиграли! Я выбрал `' + bot_choice + '`.')
        elif user_choice == 'камень' and bot_choice == 'бумага':
            await self.bot.say('Вы проиграли! Вы выбрали `' + user_choice + '`, когда я выбрал `' + bot_choice + '`')

    @commands.command(pass_context = True)
    async def createpasta(self, ctx, key, *,value):
        """Creates a copypasta"""
        configuration["pastas"][key].append(value)
        file_updating()
        await self.bot.say('Паста `{}` была создана!'.format(key))

    @commands.command(pass_context=True)
    async def editpasta(self, ctx, key, *, value):
        """Edits a copypasta"""
        configuration["pastas"][key].append(value)
        file_updating()
        await self.bot.say('Паста `{}` была изменена!'.format(key))

    @commands.command(pass_context=True)
    async def delpasta(self, ctx, key):
        """Deletes a copypasta"""
        del configuration["pastas"][key]
        file_updating()
        await self.bot.say('Паста `{}` была удалена!'.format(key))

    @commands.command(pass_context = True)
    async def pasta(self, ctx, key):
        """Sends a copypasta."""
        await self.bot.say(configuration["pastas"][key])

    @commands.command(pass_context = True)
    async def avatar(self, ctx, *, user: discord.User = None):
        """Shows user avatar."""
        if user is None:
            user = ctx.message.author
        em = discord.Embed(description='')
        if user.avatar_url:
            em.set_image(url=str(user.avatar_url))
            await self.bot.say(embed=em)
        else:
            await self.bot.say("This user has no avatar.")

    @commands.command(pass_context=True)
    async def define(self, ctx, *, word):
        """Finds a definition to the given word on Urban Dictionary."""
        async with aiohttp.ClientSession() as session:
            async with session.get("http://api.urbandictionary.com/v0/define", params={'term': word}) as ud:
                ud1 = await ud.json()
                if ud1['result_type'] == 'no_results':
                    await self.bot.say("No results.")
                else:
                    em = discord.Embed(colour=0x1d2439,description='')
                    em.set_author(name='Urban Dictionary: {}'.format(word), url=ud1['list'][0]['permalink'])
                    if len(ud1['tags'])>0:
                        em.add_field(name="Tags", value="{}".format(',\n'.join(ud1['tags'][:3])))
                    em.add_field(name='Definition', value = '{}'.format(ud1['list'][0]['definition']), inline=True)
                    em.add_field(name="Examples", value=ud1['list'][0]['example'], inline=False)
                    em.add_field(name=":thumbsup:", value=ud1['list'][0]['thumbs_up'], inline=True)
                    em.add_field(name=":thumbsdown:", value=ud1['list'][0]['thumbs_down'], inline=True)
                    await self.bot.say(embed=em)

    @commands.command(pass_context = True, hidden = True)
    @checks.is_owner()
    async def add_stream(self, ctx, stream):
        configuration["streams"].append(stream)
        file_updating()
        await self.bot.say('Стример `{}` был добавлен'.format(stream))
    
    @commands.command(pass_context = True, hidden = True)
    @checks.is_owner()
    async def del_stream(self, ctx, stream):
        configuration["streams"].remove(stream)
        file_updating()
        await self.bot.say('Стример `{}` был удалён'.format(stream))


def setup(bot):
    bot.add_cog(Fun(bot))