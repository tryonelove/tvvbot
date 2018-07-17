import discord
from discord.ext import commands
import aiohttp
import random
import time
from TwitterSearch import *
import re
import config
import checks
import json
import asyncio
import mods
from osu import star_rating

startup_extensions = ["osu", "weather", "nsfw", "fun", 'img']
tuo = TwitterUserOrder('aceasianbot')
tuo.set_count(100)

ts = TwitterSearch(
    consumer_key=config.consumer_key,
    consumer_secret=config.consumer_secret,
    access_token=config.access_token,
    access_token_secret=config.access_token_secret
)

help=''

bot = commands.Bot(command_prefix='!', pm_help=help, owner_id='106833067708051456')

with open('configuration.json', 'r+') as f:
    configuration = json.load(f)

bot.remove_command("help")

osu_api = 'https://osu.ppy.sh/api'

osu_api_key=config.osu_api_key

gatari_api = 'https://osu.gatari.pw/api/v1'

weather_key = config.weather_key



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

@bot.command(pass_context = True)
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

@bot.event
async def on_message(message):
    if message.content.startswith('!8ball'):
        await bot.send_message(message.channel, random.choice(config.choice))
    s = re.search(r'https?:\/\/(osu|new)\.(?:gatari|ppy).(?:pw|sh)/([bs]|beatmapsets)/(\d+)(#(\w+)/(\d+))?', message.content)
    modsEnum = 0
    mods_str = ''
    if s:
        if '+' in message.content:
                for i in message.content.split()[2:]:
                                if i == "NF":
                                    modsEnum += mods.NOFAIL
                                    mods_str += i
                                elif i == "EZ":
                                    modsEnum += mods.EASY
                                    mods_str += i
                                elif i == "HD":
                                    modsEnum += mods.HIDDEN
                                    mods_str += i
                                elif i == "HR":
                                    modsEnum += mods.HARDROCK
                                    mods_str += i
                                elif i == "DT":
                                    modsEnum += mods.DOUBLETIME
                                    mods_str += i
                                elif i == "HT":
                                    modsEnum += mods.HALFTIME
                                    mods_str += i
                                elif i == "NC":
                                    modsEnum += mods.NIGHTCORE
                                    mods_str += i
                                elif i == "FL":
                                    modsEnum += mods.FLASHLIGHT
                                    mods_str += i
                                elif i == "SO":
                                    modsEnum += mods.SPUNOUT
                                    mods_str += i
                                elif i == "V2":
                                    modsEnum += mods.SCOREV2
                                    mods_str += i
                                elif i == "RX":
                                    modsEnum += mods.RELAX
                                    mods_str += i
                                elif i == "AP":
                                    modsEnum += mods.RELAX2	
                                    mods_str += i
        if '/b/' or '/beatmapsets/' in str(s.group(0)):
                    b = str(s.group(0))
                    if '/b/' in b:
                        b_mapa = b.find('/b/')
                        b_mapa = b[b_mapa+3:]
                    elif 'beatmapsets' in b:
                        b_mapa = b.rfind('/')
                        b_mapa = b[b_mapa +1:]
                    #http://osu.gatari.pw/api/v1/pp b= c= a= m= x(misses)=
                    async  with aiohttp.ClientSession() as session:
                        async with session.get('http://osu.gatari.pw/api/v1/pp', params={'b':b_mapa, 'm':modsEnum}) as r1:
                            a = await r1.json()
                        async with session.get(osu_api+'/get_beatmaps', params = {'k': osu_api_key, 'b' : b_mapa}) as r:
                            js = await r.json()
                            em = discord.Embed(description=('**Mapper: **{}   **BPM: **{}\n**AR: **{}   **OD: **{}   **HP: **{}   **Stars:** {}{}'.format(js[0]['creator'],
                                                                                                                                                            js[0]['bpm'], 
                                                                                                                                                            js[0]['diff_approach'],
                                                                                                                                                            js[0]['diff_overall'],
                                                                                                                                                            js[0]['diff_drain'], 
                                                                                                                                                            str(round(float(js[0]['difficultyrating']), 2)),
                                                                                                                                                            star_rating(float(js[0]['difficultyrating'])))), colour = 0xCC5288)
                            if 'pp' in a:                                                                                                          
                                em.add_field(name='----------------PP: {}--------------------'.format(mods_str),value='**100%:** {}pp **99%:** {}pp **98%:** {}pp **95%:** {}pp'.format(a['pp'][0],a['pp'][1],a['pp'][2],a['pp'][3]))
                            em.set_author(name=('{} - {} [{}] (Clickable)'.format(js[0]['artist'],js[0]['title'],js[0]['version'])), url=b)
                            em.set_thumbnail(url='https://b.ppy.sh/thumb/'+str(js[0]['beatmapset_id'])+'.jpg')
                            await bot.send_message(message.channel, embed=em)
        elif '/s/' in str(s.group(0)):
                    s = str(s.group(0))
                    if '/s/' in s:
                        s_mapa = s.find('/s/')
                        s_mapa = s[s_mapa+3:]
                    async  with aiohttp.ClientSession() as session:
                        async with session.get(osu_api + '/get_beatmaps', params = {'k': osu_api_key, 's' : s_mapa}) as r:
                            js = await r.json()
                        async with session.get('http://osu.gatari.pw/api/v1/pp', params={'b':js[0]['beatmap_id'], 'm':modsEnum}) as r1:
                            a = await r1.json()
                            em = discord.Embed(description=('**Mapper: **' + js[0]['creator']) +
                                                        '   **BPM: **' + js[0]['bpm'] +'   **Stars:**  '+str(round(float(js[0]['difficultyrating']), 2))+star_rating(float(js[0]['difficultyrating']))+
                                                        '\n**AR: **' + js[0]['diff_approach'] +
                                                        '   **OD: **' + js[0]['diff_overall'] +
                                                        '   **HP: **' + js[0]['diff_drain']+
                                                        '   **Max Combo: **' + js[0]['max_combo'], colour = 0xCC5288)
                            em.add_field(name='----------------PP: {}--------------------'.format(mods_str),value='**100%:** {}pp **99%:** {}pp **98%:** {}pp **95%:** {}pp'.format(a['pp'][0],a['pp'][1],a['pp'][2],a['pp'][3]))
                            em.set_author(name=(js[0]['artist']+' - '+js[0]['title']+' ['+js[0]['version']+'] (Clickable)'), url=s)
                            em.set_thumbnail(url='https://b.ppy.sh/thumb/' + str(js[0]['beatmapset_id']) + '.jpg')
                            await bot.send_message(message.channel, embed=em)
    else:
        pass
    t = re.search(r'https?:\/\/(osu)\.(?:gatari|ppy).(?:pw|sh)/(u|users)/(\w.+)', message.content)
    if t:
        u = str(t.group(0))
        if '/u/' in u:
            u_id = u.find('/u/')
            u_id = ((u[u_id+3:]).replace('%20', ' ')).replace('?','&')
        elif '/users/' in u:
            u_id = u.find('/users/')
            u_id = ((u[u_id+7:]).replace('%20', ' ')).replace('?','&')
        if 'osu.ppy.sh' in t.group(0):
            async  with aiohttp.ClientSession() as session:
                async with session.get(osu_api + '/get_user', params={'k': osu_api_key, 'u': u_id}) as r:
                        js = await r.json()
                        em = discord.Embed(description=('**PP: **'+js[0]['pp_raw']+
                                                        '\n**Rank:** #'+js[0]['pp_rank']+
                                                        '\n**Country rank:** #'+js[0]['pp_country_rank']+
                                                        '\n**Accuracy:** '+str(round(float(js[0]['accuracy']), 2))
                                                        )
                                           , colour = 0xCC5288)
                        em.set_thumbnail(url='https://a.ppy.sh/'+js[0]['user_id']+'_1.png')
                        em.set_author(icon_url='https://s.ppy.sh/images/flags/'+(js[0]['country']).lower()+'.gif', name=js[0]['username'], url='https://osu.ppy.sh/u/'+js[0]['user_id'])
                        em.set_footer(text='osu!',icon_url='https://upload.wikimedia.org/wikipedia/commons/4/41/Osu_new_logo.png')
                        await bot.send_message(message.channel,embed=em)
        elif 'osu.gatari.pw' in t.group(0):
            async  with aiohttp.ClientSession() as session:
                async with session.get(gatari_api + '/users/stats', params={'u': u_id}) as r:
                    js = await r.json()
                    em = discord.Embed(description=('**PP: **'+str(js['stats']['pp'])+
                                        '\n**Accuracy: **'+str(round(js['stats']['accuracy'],2))+
                                        '\n**Play count: **'+str(js['stats']['playcount'])+
                                       '\n**Rank: **#'+str(js['stats']['rank']))
                                       ,color=0x901354)
                    em.set_thumbnail(url="https://a.gatari.pw/" + str(js['stats']['id']))
                    em.set_author(name=str(js['stats']['username'] + " (clickable)"), url='https://osu.gatari.pw/u/' +str(js['stats']['id']), )
                    em.set_footer(text='osu!Gatari',icon_url='https://b.catgirlsare.sexy/Ghtc.png')
                    await bot.send_message(message.channel, embed=em)
    else:
        pass
    await bot.process_commands(message)



@bot.command(pass_context=True)
async def ping(ctx):
    pingtime = time.time()
    pingms = await bot.say("Pinging... `{}'s` location".format(ctx.message.author.mention))
    ping = time.time() - pingtime
    await bot.edit_message(pingms, "The ping time is `%.01f seconds`" % ping)

@bot.command()
async def invite():
    await bot.say('https://discordapp.com/oauth2/authorize?&client_id=247651906032369665&scope=bot&permissions=0')    

@bot.group(pass_context=True)
async def set(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say('Invalid command passed...')

@set.command(pass_context=True)
async def game(ctx, t, *, games:str):
        if games is None:
            await bot.say('No games to set.')
        game = discord.Game(type=int(t), name=games)
        await bot.change_presence(game=game)

@bot.command(pass_context=True)
async def help(ctx):
    em = discord.Embed(description='Личное сообщение с командами было отправлено!', colour=0x3297AC)
    await bot.send_message(ctx.message.author, "Привет, вот список моих команд(все они выполняются с префиксом !):"
                                               "```"
                                               "\ncat - присылает рандомного кота"
                                               "\ndog - рандомная псина"
                                               "\nping - пинг"
                                               "\nroll - random number (0..1000)"
                                               "\nlast <count> <username (optional), default value is discord username> - <count> last score for <username> player"
                                               "\nosu <username(optional)> - osu!std profile stats"
                                               "\nmania <username(optional)> - osu!mania profile stats"
                                               "\nctb <username(optional)> - osu!ctb profile stats"
                                               "\ntaiko <username(optional)> - osu!taiko profile stats"
                                               "\ngatari <username - osu!gatari std stats>"
                                               "\nripple <username - osu!gatari std stats>"
                                               "\ntop <server (bancho/gatari/ripple)> <username(optional), defaults set to discord username> - user osu!std top score stats"
                                               "\nversus <player1> <player2> - osu!Skills comparison"
                                               "\ndefine <word/phrase/etc> - Urban Dictionary definition of the phrase"
                                               "\nroll - рандомное чисто от 1 до 1000"
                                               "\nboobs - грудь"
                                               "\nbutt - жёппа"
                                               "\nhello - Hello @message author"
                                               "\nбурятка - присылает бурятку"
                                               "\nпогода/weather <city> - показывает погоду в городе (если указана страна, то показывает погоду в столице)"
                                               "\nclear <count> - удаляет count сообщений"
                                               "\nкнб <камень\ножницы\бумага> - камень, ножницы, бумага"
                                               "\navatar <@user> - показывает аватарку указанного пользователя"
                                               "\nkiss/hug/punch/kill <@user>"
                                               "```"
                                               "\nСервер поддержки: https://discord.gg/jjzEJVD")

    await bot.send_message(ctx.message.channel, embed=em)


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
            await asyncio.sleep(2)


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    bot.loop.create_task(is_live_stream())
    bot.run(config.bot_token)
    


