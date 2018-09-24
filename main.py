import discord
from discord.ext import commands
import aiohttp
import random
import time
import config
import checks
import json
import asyncio
import mods
from cogs.osu import star_rating
from cogs.osu import acc_calc, star_rating, readableMods, rank_emoji
import datetime
import logging

startup_extensions = ["osu", "nsfw", "fun", 'voice']

bot = commands.Bot(command_prefix='!', pm_help = True, owner_id='106833067708051456')


with open('configuration.json', 'r+') as f:
    configuration = json.load(f)

@bot.event
async def on_ready():
    print('Logged in as:')
    print(bot.user.name)
    print(bot.user.id)
    print('Currently working on '+str(len(bot.servers))+' servers')
    print('------')
    # url='https://twitch.tv/tryonelove1'
    game = discord.Game(type=1, name="with your mom's dick")
    await bot.change_presence(game=game)

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        pass

@bot.command(pass_context = True, hidden=True)
@checks.is_owner()
async def load_asian(ctx):
        count = 1
        f = open('asians.txt', 'w')
        for tweet in (ts.search_tweets_iterable(tuo)):
                f.write(tweet['entities']['media'][0]['media_url']+ '\n')
                count = count+1
                print(count)
        f.close()
        print('OK')

@bot.command()
async def invite():
    await bot.say('https://discordapp.com/oauth2/authorize?&client_id=247651906032369665&scope=bot&permissions=0')    

@bot.group(pass_context=True, hidden=True)
async def set(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say('Invalid command passed...')

@set.command(pass_context=True, hidden=True)
async def game(ctx, t, *, games:str):
        if games is None:
            await bot.say('No games to set.')
        game = discord.Game(type=int(t), name=games)
        await bot.change_presence(game=game)

@checks.is_owner()
@bot.command(pass_context=True, hidden = True)
async def reload(ctx, *, cog_name: str):
    """Reloads a cog
    Example: reload voice"""
    try:
        bot.unload_extension(cog_name)
        bot.load_extension(cog_name)
        await bot.say('Cog `{}` has been reloaded.'.format(cog_name))
    except Exception as e:
        print("Reload error: "+str(e))
        await bot.say("Error, check console")

async def is_live_stream():
    online = []
    await bot.wait_until_ready()
    while not bot.is_closed:
        for name in configuration['streams']:
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.twitch.tv/kraken/streams/' + name,
                                       params={'client_id': config.twitch_client_id}) as r:
                    try:
                      js = await r.json()
                      if js['stream'] is not None:
                        if name not in online:
                          online.append(name)
                          msg = await bot.send_message(discord.Object(id='352547955347030036'), '***{}*** is now online!\nPlaying: ***{}***\nCheck it out: {}'.format(name.capitalize(),js['stream']['game'], 'https://twitch.tv/'+name))
                          if msg:
                              pass
                        elif name in online:
                          pass
                        elif js['stream'] is None and name in online:
                          online.remove(name)
                    except Exception as error:
                        print('Error: ',error)
                        print('JS: ', r)
            await asyncio.sleep(5)


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension("cogs."+extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    loop = asyncio.get_event_loop()
    loop.create_task(is_live_stream()) #не работает нихуя (а может и работает)
    bot.run(config.bot_token)