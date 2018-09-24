import discord
from discord.ext import commands
import aiohttp
import asyncio
import random
import config
import mods
from bs4 import BeautifulSoup
import datetime
import re
from difflib import SequenceMatcher
import pytesseract
from io import BytesIO
from PIL import Image
import sys
import pyttanko as osu
import pyttanko

sig_colors =['black', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'hex2255ee']

skillLabels = ["Stamina",
                    "Tenacity",
                    "Agility", 
                    "Accuracy", 
                    "Precision",
                    "Reaction", 
                    "Memory"
                ]

osu_api = 'https://osu.ppy.sh/api'
osu_api_key = config.osu_api_key
gatari_api = 'https://osu.gatari.pw/api/v1'

osuservers = ('bancho', 'gatari', 'ripple')

def readableMods(m):
        r = ""
        if m == 0:
            return "NOMOD"
        if m & mods.NOFAIL > 0:
            r += "NF"
        if m & mods.EASY > 0:
            r += "EZ"
        if m & mods.HIDDEN > 0:
            r += "HD"
        if m & mods.HARDROCK > 0:
            r += "HR"
        if m & mods.DOUBLETIME > 0:
            r += "DT"
        if m & mods.HALFTIME > 0:
            r += "HT"
        if m & mods.FLASHLIGHT > 0:
            r += "FL"
        if m & mods.SPUNOUT > 0:
            r += "SO"
        if m & mods.TOUCHSCREEN > 0:
            r += "TD"
        if m & mods.RELAX > 0:
            r += "RX"
        if m & mods.RELAX2 > 0:
            r += "AP"	
        return r

def rank_emoji(rank):
    if rank == 'XH':
        return '<:rankingxh:427498392747376642>'
    if rank == 'SH':
        return '<:rankingsh:427498392353112084>'
    if rank == 'X':
        return '<:rankingX:427498392953028618>'
    if rank == 'S':
        return '<:rankings:427498392759959552>'
    if rank == 'A':
        return '<:rankingA:427498391367319552>'
    if rank == 'B':
        return '<:rankingb:427498389882667037>'
    if rank == 'C':
        return '<:rankingc:427498392596381716>'
    if rank == 'D':
        return '<:rankingd:427498391895801866>'
    if rank == 'F':
        return '<:rankingF:427506956996182041>'

def acc_calc(misses, count50, count100, count300):
    accuracy = str(round(((50*count50+100*count100+300*count300)*100/(300*(misses+count50+count100+count300))),2))
    return accuracy

def star_rating(stars):
    if stars<=1.50:
        return '<:easy:428835676801466370>'
    if stars>1.50 and stars<=2.25:
        return '<:normal:428835676654665730>'
    if stars>2.25 and stars<=3.75:
        return '<:hard:428835676184641547>'
    if stars>3.75 and stars<=5.25:
        return '<:insane:428835681423458304>'
    if stars>5.25:
        return '<:expert:428835677103456256>'

class Osu():
    """
    osu! related commands.
    """
    def __init__(self, bot):
        self.bot = bot    


    @commands.command(pass_context=True)
    async def osu(self,ctx, *, name: str = None):
        """Sends an osu!std picture for given username."""
        if name is None:
            name = ctx.message.author.name
        await self.bot.send_typing(ctx.message.channel)
        em = discord.Embed(description='')
        em.set_author(name='{} profile'.format(name), url='https://osu.ppy.sh/u/{}'.format(name.replace(' ', '%20')))
        em.set_image(url='http://lemmmy.pw/osusig/sig.php?colour={}&uname={}&pp=1&darktriangles&onlineindicator=undefined&xpbar&xpbarhex'.format(random.choice(sig_colors),name.replace(' ', '%20')))
        em.set_footer(text='Image provided by https://lemmmy.pw/osusig', icon_url='https://upload.wikimedia.org/wikipedia/commons/4/41/Osu_new_logo.png')
        await self.bot.say(embed=em)
    
    @commands.command(pass_context=True)
    async def gatari(self,ctx, *, name: str = None):
        """Sends a gatari picture for given username."""
        if name is None:
            name = ctx.message.author.name
        await self.bot.send_typing(ctx.message.channel)
        em = discord.Embed(description='')
        em.set_author(name='{} profile'.format(name), url='https://osu.gatari.pw/u/{}'.format(name.replace(' ', '%20')))
        em.set_image(url='http://sig.gatari.pw/sig.php?colour={}&uname={}&pp=1&darktriangles'.format(random.choice(sig_colors),name.replace(' ', '%20')))
        em.set_footer(text='Image provided by http://sig.gatari.pw/', icon_url='https://upload.wikimedia.org/wikipedia/commons/4/41/Osu_new_logo.png')
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def ripple(self,ctx, *, name: str = None):
        """Sends a ripple picture for given username."""
        if name is None:
            name = ctx.message.author.name
        await self.bot.send_typing(ctx.message.channel)
        em = discord.Embed(description='')
        em.set_author(name='{} profile'.format(name), url='https://ripple.moe/u/{}'.format(name.replace(' ', '%20')))
        em.set_image(url='http://sig.ripple.moe/sig.php?colour={}&uname={}&pp=1&darktriangles'.format(random.choice(sig_colors),name.replace(' ', '%20')))
        em.set_footer(text='Image provided by http://sig.ripple.moe/', icon_url='https://b.catgirlsare.sexy/E3YS.png')
        await self.bot.say(embed=em)    

    @commands.command(pass_context=True)
    async def taiko(self,ctx, *, name: str = None):
        """Sends an osu!taiko picture for given username."""
        if name is None:
            name = ctx.message.author.name
        await self.bot.send_typing(ctx.message.channel)
        em = discord.Embed(description='')
        em.set_author(name='{} profile'.format(name), url='https://osu.ppy.sh/u/{}'.format(name.replace(' ', '%20')))
        em.set_image(url='http://lemmmy.pw/osusig/sig.php?colour={}&uname={}&mode=1&pp=1&darktriangles&onlineindicator=undefined&xpbar&xpbarhex'.format(random.choice(sig_colors),name.replace(' ', '%20')))
        em.set_footer(text='Image provided by https://lemmmy.pw/osusig',
                      icon_url='https://upload.wikimedia.org/wikipedia/commons/4/41/Osu_new_logo.png')
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def mania(self,ctx, *, name: str = None):
        """Sends an osu!mania picture for given username."""
        if name is None:
            name = ctx.message.author.name
        await self.bot.send_typing(ctx.message.channel)
        em = discord.Embed(description='')
        em.set_author(name='{} profile'.format(name), url='https://osu.ppy.sh/u/{}'.format(name.replace(' ', '%20')))
        em.set_image(url='http://lemmmy.pw/osusig/sig.php?colour={}&uname={}&mode=3&pp=1&darktriangles&onlineindicator=undefined&xpbar&xpbarhex'.format(random.choice(sig_colors),name.replace(' ', '%20')))
        em.set_footer(text='Image provided by https://lemmmy.pw/osusig', icon_url='https://upload.wikimedia.org/wikipedia/commons/4/41/Osu_new_logo.png')
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def ctb(self,ctx, *, name:str = None):
        """Sends an osu!ctb picture for given username."""
        if name is None:
            name = ctx.message.author.name
        await self.bot.send_typing(ctx.message.channel)
        em = discord.Embed(description='')
        em.set_author(name='{} profile'.format(name), url='https://osu.ppy.sh/u/{}'.format(name.replace(' ', '%20')))
        em.set_image(url='http://lemmmy.pw/osusig/sig.php?colour={}&uname={}&mode=2&pp=1&darktriangles&onlineindicator=undefined&xpbar&xpbarhex'.format(random.choice(sig_colors),name.replace(' ', '%20')))
        em.set_footer(text='Image provided by https://lemmmy.pw/osusig', icon_url='https://upload.wikimedia.org/wikipedia/commons/4/41/Osu_new_logo.png')
        await self.bot.say(embed=em)

    @commands.command(pass_context=True, name="osuchan", aliases=["oc"])
    async def _osuchan(self, ctx, *, name:str=None):
        """Some stats from https://syrin.me/osuchan/"""
        if name is None:
            name = ctx.message.author.name
        await self.bot.send_typing(ctx.message.channel)
        async with aiohttp.ClientSession() as session:
            async with session.get('https://syrin.me/osuchan/u/{}/?m=0'.format(name.replace(' ','%20'))) as r:
                osuchan = await r.text()
            async with session.get('https://syrin.me/osuchan/u/{}/nochoke/?m=0&nec_unchoke=yes'.format(name.replace(' ','%20'))) as r:
                nochoke = await r.text()
        soup_main = BeautifulSoup(osuchan, 'html.parser')
        soup_nochoke = BeautifulSoup(nochoke, 'html.parser')
        nochoke_stats = soup_nochoke.find(id="results_panel").text
        nc = nochoke_stats.splitlines()
        tables = soup_main.find_all('td')
        username = soup_main.h1.text
        level = tables[4].text[:-3]
        playcount = tables[6].text
        accuracy = tables[8].text
        fav_mappers = tables[10].text
        fav_mappers_pp = tables[13].text
        best_mod = tables[15].text
        best_bpm = tables[17].text
        best_ar = tables[19].text
        best_length = tables[21].text
        avatar = soup_main.find('div', {'class':'col-md-4'}).img['src']
        rank = soup_main.h3.text
        country_rank = soup_main.find_all('h4')[2].text
        flag = soup_main.find_all('h4')[2].img['title']
        pp = soup_main.h5.text
        em = discord.Embed(description='', colour = 0x222C48)
        em.add_field(name='**General Stats**', value = ':flag_{}:\n**PP:** {}\n**Level:** {}\n**Play Count:** {}\n**Accuracy:** {}\n\n**Fav. Mappers:** {}\n**(Unweighted) Fav. Mappers:** {}\n'.format(flag.lower(),pp,level, playcount, accuracy,fav_mappers,fav_mappers_pp))
        em.add_field(name='**Score Style**', value = '**Best mod:** {}\n**Best BPM:** {}     **Best AR:** {}     **Best Length:** {}'.format(best_mod, best_bpm, best_ar, best_length))
        em.add_field(name='**No-choke stats**', value = '**{}** {}\n**{}** {}'.format(nc[1], nc[2], nc[3], nc[4]))
        em.set_author(name='{} {} ({} {})'.format(username, rank, country_rank, flag), url='https://syrin.me/osuchan/u/{}/?m=0'.format(name.replace(' ','%20')))
        em.set_thumbnail(url=avatar)
        em.set_footer(text='osu!chan',icon_url='https://syrin.me/static/img/oc_logo_light_bold-100.png')
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def top(self, ctx, server: str = None, *, nick: str = None):
        """Top score of the given user. Supports bancho, ripple, gatari.
            Example: !top gatari cookiezi, !top cookiezi"""
        if server not in osuservers:
            nick = ' '.join(ctx.message.content.split()[1:])
            if nick == '':
                nick = ctx.message.author.name
            server = 'bancho'
        elif server in osuservers:
            nick = ' '.join(ctx.message.content.split()[2:])
            if nick == '':
                nick = ctx.message.author.name
        server = server.lower()
        bm = None
        score = None
        pp = None
        combo = None
        count50 = None
        count100 = None
        count300 = None
        misses = None
        rank = None
        await self.bot.send_typing(ctx.message.channel)
        if server == 'bancho':
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://osu.ppy.sh/api/get_user_best', params={'k': config.osu_api_key, 'u': nick, 'limit' : '1'}) as r:
                        if r.status == 200:
                            js = await r.json()
                            bm = js[0]['beatmap_id']
                            score = js[0]['score']
                            pp = js[0]['pp']
                            combo =  js[0]['maxcombo']
                            count50 = js[0]['count50']
                            count100 = js[0]['count100']
                            count300 = js[0]['count300']
                            misses = js[0]['countmiss']
                            rank = js[0]['rank']
                            m = js[0]['enabled_mods']
                            user_id = js[0]['user_id']
                    async with session.get('https://osu.ppy.sh/api/get_user', params={'k': config.osu_api_key, 'u': nick}) as r:
                        js1 = await r.json()
                    async with session.get('https://osu.ppy.sh/api/get_beatmaps', params={'k': config.osu_api_key, 'b' : bm}) as s:
                        if s.status == 200:
                            js2 = await s.json()
                            title =  js2[0]['artist'] + ' - '+ js2[0]['title']+' ('+js2[0]['version']+')'
                            em = discord.Embed(description=('[{}](https://osu.ppy.sh/b/{}){} **{}**\n  **Score:** {}   **Accuracy:**  {}\n  <:hit300:427941500035268608>{} <:hit100:427941500274475039>{}  <:hit50:427941499846787084>{}  <:hit0:427941499884535829>{}\n  **Combo:** {}/{}   **Rank:** {}   **PP:** {}'.format(
                                                            title,
                                                            bm,
                                                            star_rating(float(js2[0]['difficultyrating'])), 
                                                            readableMods(int(m)), 
                                                            score, 
                                                            acc_calc(int(misses),int(count50),int(count100),int(count300)), 
                                                            count300, 
                                                            count100, 
                                                            count50, 
                                                            misses, 
                                                            combo,
                                                            js2[0]['max_combo'], 
                                                            rank_emoji(rank),
                                                            pp)
                                                            ), colour = 0xDA70D6
                                                )
                            em.set_author(name=("{} {}pp #{} ({}#{})".format(js1[0]['username'],js1[0]['pp_raw'],js1[0]['pp_rank'], js1[0]['country'],js1[0]['pp_country_rank'])), url='https://osu.ppy.sh/u/{}'.format(user_id), icon_url='https://a.ppy.sh/{}_1.png'.format(user_id))
                            em.set_thumbnail(url='https://b.ppy.sh/thumb/{}.jpg'.format(js2[0]['beatmapset_id']))
                            em.set_footer(text="osu!",icon_url="https://upload.wikimedia.org/wikipedia/commons/4/41/Osu_new_logo.png")
                            await self.bot.send_message(ctx.message.channel, embed=em)
        elif server== 'gatari':
            async with aiohttp.ClientSession() as session:
                async with session.get('https://osu.gatari.pw/api/v1/users/stats', params = {'u':nick}) as g:
                    n = await g.json()
                    user_id = n['stats']['id']
                    nick = n['stats']['username']
                async with session.get('https://osu.gatari.pw/api/v1/users/scores/best?id={}&l=1&f=0&p=1&mode=0'.format(str(user_id))) as gt:
                    js3 = await gt.json()
                    bm = js3['scores'][0]['beatmap']['beatmap_id']
                    score = js3['scores'][0]['score']
                    pp = js3['scores'][0]['pp']
                    combo = js3['scores'][0]['max_combo']
                    count50 = js3['scores'][0]['count_50']
                    count100 = js3['scores'][0]['count_100']
                    count300 = js3['scores'][0]['count_300']
                    misses = js3['scores'][0]['count_miss']
                    max_combo = js3['scores'][0]['fc']
                    m = js3['scores'][0]['mods']
                async with session.get('https://osu.ppy.sh/api/get_beatmaps', params={'k': config.osu_api_key, 'b' : bm}) as g:
                 if g.status == 200:
                    js2 = await g.json()
                    title =  js2[0]['artist'] + ' - '+ js2[0]['title']+' ('+js2[0]['version']+')'
                    em = discord.Embed(description=('[{}](https://osu.ppy.sh/b/{}){} **{}**\n  **Score:** {}   **Accuracy:**  {}\n  **<:hit300:427941500035268608>**{} **<:hit100:427941500274475039>**{} **<:hit50:427941499846787084>**{} **<:hit0:427941499884535829>**{}\n   **Combo:** {}**x{}**   **PP:**{}'.format(str(title),
                                                                                                                                                        bm, 
                                                                                                                                                        star_rating(float(js2[0]['difficultyrating'])),
                                                                                                                                                        readableMods(int(m)), 
                                                                                                                                                        str(score), 
                                                                                                                                                        acc_calc(int(misses),int(count50),int(count100),int(count300)),
                                                                                                                                                        str(count300),
                                                                                                                                                        str(count100),
                                                                                                                                                        str(count50),
                                                                                                                                                        str(misses),
                                                                                                                                                        str(combo),
                                                                                                                                                        str(max_combo),
                                                                                                                                                        str(pp)
                                                                                                                                                            )
                                                    ), colour=0x87104D
                                    )
                    em.set_author(name=("{} {}pp #{}".format(nick, n['stats']['pp'],n['stats']['rank'])), url='https://osu.gatari.pw/u/{}'.format(str(user_id)), icon_url='https://a.gatari.pw/{}'.format(str(user_id)))
                    em.set_footer(text="osu!gatari", icon_url="https://osu.gatari.pw/favicon-32x32.png")
                    em.set_thumbnail(url='https://b.ppy.sh/thumb/{}.jpg'.format(js2[0]['beatmapset_id']))
                    await self.bot.send_message(ctx.message.channel, embed=em)
        elif server== 'ripple':
            async with aiohttp.ClientSession() as session:
                async with session.get('http://ripple.moe/api/get_user_best', params={'u':nick}) as rp:
                    js4 = await rp.json()
                    bm = js4[0]['beatmap_id']
                    score = js4[0]['score']
                    pp = js4[0]['pp']
                    combo = js4[0]['maxcombo']
                    count50 = js4[0]['count50']
                    count100 = js4[0]['count100']
                    count300 = js4[0]['count300']
                    misses = js4[0]['countmiss']
                    rank = js4[0]['rank']
                    m = js4[0]['enabled_mods']
                    max_combo = js4[0]['maxcombo']
                    user_id = js4[0]['user_id']
                async with session.get('http://ripple.moe/api/get_user', params={'u':nick}) as rp1:
                    gu = await rp1.json()
                async with session.get('https://osu.ppy.sh/api/get_beatmaps', params={'k': config.osu_api_key, 'b' : bm}) as g:
                 if g.status == 200:
                    js2 = await g.json()
                    title =  js2[0]['artist'] + ' - '+ js2[0]['title']+' ('+js2[0]['version']+')'
                    em = discord.Embed(description=('[{}](https://osu.ppy.sh/b/{}){} **{}**\n  **Score:** {}   **Accuracy:**  {}\n  **<:hit300:427941500035268608>**{} **<:hit100:427941500274475039>**{} **<:hit50:427941499846787084>**{} **<:hit0:427941499884535829>**{}\n   **Combo:** {}**x{}**   **PP:**{}'.format(str(title),
                                                                                                                                                        bm, 
                                                                                                                                                        star_rating(float(js2[0]['difficultyrating'])),
                                                                                                                                                        readableMods(int(m)), 
                                                                                                                                                        str(score), 
                                                                                                                                                        acc_calc(int(misses),int(count50),int(count100),int(count300)),
                                                                                                                                                        str(count300),
                                                                                                                                                        str(count100),
                                                                                                                                                        str(count50),
                                                                                                                                                        str(misses),
                                                                                                                                                        str(combo),
                                                                                                                                                        str(max_combo),
                                                                                                                                                        str(pp)
                                                                                                                                                            )), colour = 0xE95092
                    )
                    em.set_author(name=("{} {}pp #{} ({}#{})".format(gu[0]['username'], gu[0]['pp_raw'],gu[0]['pp_rank'], gu[0]['country'], gu[0]['pp_country_rank'])), url='https://ripple.moe/u/'+user_id, icon_url='https://a.ripple.moe/{}.png'.format(user_id))
                    em.set_footer(text="osu!ripple", icon_url='https://i.imgur.com/0pWEFGs.png')
                    em.set_thumbnail(url='https://b.ppy.sh/thumb/' + str(js2[0]['beatmapset_id']) + '.jpg')
                    await self.bot.send_message(ctx.message.channel, embed=em)

    @commands.command(pass_context=True)
    #http://osu.gatari.pw/api/v1/pp b= c= a= m= x(misses)=
    async def last(self, ctx, limit: str = None, *, nick: str = None):
        """Last score for the given user."""
        if limit is None:
            limit = '1'
        if limit.isdigit()==False:
            nick = ' '.join(ctx.message.content.split()[1:])
            if nick == '':
                nick = ctx.message.author.name
            limit = '1'
        elif limit.isdigit():
            nick = ' '.join(ctx.message.content.split()[2:])
            if nick == '':
                nick = ctx.message.author.name
        await self.bot.send_typing(ctx.message.channel)
        async with aiohttp.ClientSession() as session:
                async with session.get('https://osu.ppy.sh/api/get_user_recent', params={'k': config.osu_api_key, 'u': nick, 'limit': limit}) as r:
                    if r.status == 200:
                        js = await r.json()
                        scores = len(js)
                        if scores>0:
                            lim = int(limit)-1
                            bm = js[lim]['beatmap_id']
                            score = js[lim]['score']
                            combo =  js[lim]['maxcombo']
                            count50 = js[lim]['count50']
                            count100 = js[lim]['count100']
                            count300 = js[lim]['count300']
                            misses = js[lim]['countmiss']
                            rank = js[lim]['rank']
                            m = js[lim]['enabled_mods']
                            accuracy = acc_calc(int(misses),int(count50),int(count100),int(count300))
                            user_id = js[lim]['user_id']
                            """
                            print(rank)
                            print(misses)
                            print(count300)
                            print(count100)
                            print(count50)
                            print(combo)
                            print(score)
                            print(bm)
                            """
                        else:
                            await self.bot.say('No recent scores for `{}`.'.format(nick))
                            return
                #http://osu.gatari.pw/api/v1/pp b= c= a= m= x(misses)=
                async with session.get('http://osu.gatari.pw/api/v1/pp', params={'b':bm, 'm':m, 'c':combo, 'a': accuracy, 'x':misses}) as r:
                    js = await r.json()
                async with session.get('https://osu.ppy.sh/api/get_user', params={'k': config.osu_api_key, 'u': nick}) as r:
                    js1 = await r.json()
                async with session.get('https://osu.ppy.sh/api/get_beatmaps', params={'k': config.osu_api_key, 'b' : bm}) as s:
                        if s.status == 200:
                            if scores>0:

                                js2 = await s.json() 
                                title =  js2[0]['artist'] + ' - '+ js2[0]['title']+' ('+js2[0]['version']+')'
                                em = discord.Embed(description=('[{}](https://osu.ppy.sh/b/{}/) {} **{}**\n  **Score:** {}   **Accuracy:** {}\n  **<:hit300:427941500035268608>**{} **<:hit100:427941500274475039>**{} **<:hit50:427941499846787084>**{} **<:hit0:427941499884535829>**{}\n  **Combo:** {}/{}   **Rank:** {}   **PP:** ~{}'.format(title,bm, star_rating(float(js2[0]['difficultyrating'])),readableMods(int(m)),score, accuracy,count300, count100, count50,misses,combo,js2[0]['max_combo'],rank_emoji(rank), js['pp'][0])))
                                em.set_author(name=("{} {}pp #{} ({}#{})".format(js1[0]['username'],js1[0]['pp_raw'],js1[0]['pp_rank'], js1[0]['country'],js1[0]['pp_country_rank'])), url='https://osu.ppy.sh/u/{}'.format(user_id), icon_url='https://a.ppy.sh/{}_1.png'.format(user_id))
                                em.set_thumbnail(url='https://b.ppy.sh/thumb/' + str(js2[0]['beatmapset_id']) + '.jpg')
                                em.set_footer(text="  osu!",icon_url="https://upload.wikimedia.org/wikipedia/commons/4/41/Osu_new_logo.png")
                await self.bot.send_message(ctx.message.channel, embed=em)
    @commands.command(pass_context= True, name="osuskills", aliases=["os"])
    async def _osuSkills(self, ctx, player1, player2):
        """http://osuskills.tk comparison for 2 given users."""
        await self.bot.send_typing(ctx.message.channel)
        skillValue1 = []
        skillValue2 = []
        stats = {}
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://osuskills.tk/user/{0}/vs/{1}'.format(player1, player2)) as r:
                source = await r.text()
                soup = BeautifulSoup(source, "html.parser")
                s = soup.find_all('output' , {"class":"skillValue"})
                username = soup.find_all('h3', {"class" : "userName"})
                for e in range(7):
                    skillValue1.append(s[e].text)
                for i in range(7,14):
                    skillValue2.append(s[i].text)
        stats[player1] = dict(zip(skillLabels, skillValue1))
        stats[player2] = dict(zip(skillLabels, skillValue2))
        em = discord.Embed(title='osu!Skills compare', url='http://osuskills.tk/user/{0}/vs/{1}'.format(player1.replace(' ', '%20'), player2.replace(' ', '%20')))
        em.add_field(name="".join(username[0].text.splitlines()), inline =True, value = '**Stamina:** {} \n**Tenacity:** {} \n**Agility:** {} \n**Accuracy:** {} \n**Precision:** {} \n**Reaction:** {} \n**Memory:** {}'.format(stats[player1]['Stamina'],stats[player1]['Tenacity'],stats[player1]['Agility'],stats[player1]['Accuracy'],stats[player1]['Precision'],stats[player1]['Reaction'],stats[player1]['Memory']))
        em.add_field(name="".join(username[1].text.splitlines()), inline =True, value = '**Stamina:** {} \n**Tenacity:** {} \n**Agility:** {} \n**Accuracy:** {} \n**Precision:** {} \n**Reaction:** {} \n**Memory:** {}'.format(stats[player2]['Stamina'],stats[player2]['Tenacity'],stats[player2]['Agility'],stats[player2]['Accuracy'],stats[player2]['Precision'],stats[player2]['Reaction'],stats[player2]['Memory']))
        em.set_footer(icon_url='http://osuskills.tk/template/images/favicons/android-chrome-192x192.png', text='osu!Skills')
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def compare(self, ctx, *, player: str = None):
        """Sends a score for the last map in chat.
        Example: !compare cookiezi"""
        if player is None:
            player = ctx.message.author.name
        async for message in self.bot.logs_from(ctx.message.channel, limit=100):
            if message.embeds:
                score = message.embeds
                break
        reg = score[0]['description'].find('<:')
        title = score[0]['description'][:reg] 
        b = title.find('/b/')
        beatmap = title[b+3:-1]
        async with aiohttp.ClientSession() as session:
            async with session.get('https://osu.ppy.sh/api/get_scores', params={'k': config.osu_api_key, 'b' : beatmap, 'u': player}) as r:
                d = await r.json()
                if len(d)>0:
                    score = d[0]['score']
                    pp = d[0]['pp']
                    combo =  d[0]['maxcombo']
                    count50 = d[0]['count50']
                    count100 = d[0]['count100']
                    count300 = d[0]['count300']
                    misses = d[0]['countmiss']
                    rank = d[0]['rank']
                    m = d[0]['enabled_mods']
                    user_id = d[0]['user_id']
                    accuracy = acc_calc(int(misses),int(count50),int(count100),int(count300))
                else:
                    await self.bot.say('No scores for `{}` on the map'.format(player))
                    return
            async with session.get('https://osu.ppy.sh/api/get_user', params={'k': config.osu_api_key, 'u': player}) as r:
                js1 = await r.json()
            async with session.get('https://osu.ppy.sh/api/get_beatmaps', params={'k':config.osu_api_key, 'b':beatmap}) as s:
                js2 = await s.json() 
                em = discord.Embed(description=('{}{} **{}**\n  **Score:** {}   **Accuracy:** {}\n  <:hit300:427941500035268608>{} <:hit100:427941500274475039>{}  <:hit50:427941499846787084>{}  <:hit0:427941499884535829>{}\n  **Combo:** {}/{}   **Rank:** {}   **PP:** {}'.format(title, 
                star_rating(float(js2[0]['difficultyrating'])),
                readableMods(int(m)),
                score,
                accuracy,
                count300,
                count100,
                count50,
                misses,
                combo,
                js2[0]['max_combo'],
                rank_emoji(rank),
                pp)))             
                em.set_author(name=("{} {}pp #{} ({}#{})".format(js1[0]['username'],js1[0]['pp_raw'],js1[0]['pp_rank'], js1[0]['country'],js1[0]['pp_country_rank'])), url='https://osu.ppy.sh/u/{}'.format(user_id), icon_url='https://a.ppy.sh/{}_1.png'.format(user_id))
                em.set_thumbnail(url='https://b.ppy.sh/thumb/' + str(js2[0]['beatmapset_id']) + '.jpg')
                em.set_footer(text="  {}".format(datetime.datetime.now().strftime('%c')),icon_url="https://upload.wikimedia.org/wikipedia/commons/4/41/Osu_new_logo.png")
        await self.bot.say(embed=em)

    async def process_user(self, message):
        search_for_user = re.search(r'https?:\/\/(osu)\.(?:gatari|ppy).(?:pw|sh)/(u|users)/(\w.+)', message.content)
        if search_for_user:
            u = search_for_user.group(0)
            if '/u/' in u:
                u_id = u.find('/u/')
                u_id = ((u[u_id+3:]).replace('%20', ' ')).replace('?','&')
            elif '/users/' in u:
                u_id = u.find('/users/')
                u_id = ((u[u_id+7:]).replace('%20', ' ')).replace('?','&')
            if 'osu.ppy.sh' in search_for_user.group(0):
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
                            await self.bot.send_message(message.channel,embed=em)
            elif 'osu.gatari.pw' in search_for_user.group(0):
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
                        await self.bot.send_message(message.channel, embed=em)


    async def process_beatmap(self, message):
        link = re.search(r'https?:\/\/(osu|new)\.(?:gatari|ppy).(?:pw|sh)/([bs]|beatmapsets)/(\d+)(/#(\w+)/(\d+))?', message.content)
        modsEnum = 0
        mods_str = ''
        if link:
            link = link.group(0)
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
            if '/b/' in link:
                map_id = link[link.rindex("/") + 1:]
                await self.bot.send_message(message.channel, embed= await self.beatmap_process(map_id, modsEnum, mods_str))
                return
            if '/s/' in link:
                map_id = link[link.rindex("/") + 1:]
                await self.bot.send_message(message.channel, embed= await self.beatmapset_process(map_id, modsEnum, mods_str))
                return
            if 'beatmapsets' in link.split("/"):
                link_parse = link.split("/")
                if (len(link_parse)==7):
                    await self.bot.send_message(message.channel, embed= await self._beatmap(link_parse[-1], modsEnum, mods_str))
                else:
                    await self.bot.send_message(message.channel, embed= await self._beatmapset(link_parse[-1], modsEnum, mods_str))
                return
            
    # processing if a beatmap
    async def _beatmap(self, beatmap_id, modsEnum, mods_str):
        #http://osu.gatari.pw/api/v1/pp b= c= a= m= x(misses)=
        async  with aiohttp.ClientSession() as session:
            async with session.get('http://osu.gatari.pw/api/v1/pp', params={'b':beatmap_id, 'm':modsEnum}) as r1:
                a = await r1.json()
            async with session.get(osu_api+'/get_beatmaps', params = {'k': osu_api_key, 'b' : beatmap_id}) as r:
                js = await r.json()
                em = discord.Embed(description=('**Mapper: **{}   **BPM: **{}\n**AR: **{}   **OD: **{}   **HP: **{}   **Stars:** {}{}'.format(js[0]['creator'],
                                                                                                                                                a['bpm'], 
                                                                                                                                                js[0]['diff_approach'],
                                                                                                                                                js[0]['diff_overall'],
                                                                                                                                                js[0]['diff_drain'], 
                                                                                                                                                str(round(float(a["stars"]), 2)),
                                                                                                                                                star_rating(float(a["stars"])))), colour = 0xCC5288)
                if 'pp' in a:                                                                                                          
                    em.add_field(name='----------------PP: {}--------------------'.format(mods_str),value='**100%:** {}pp **99%:** {}pp **98%:** {}pp **95%:** {}pp'.format(a['pp'][0],a['pp'][1],a['pp'][2],a['pp'][3]))
                em.set_author(name=('{} - {} [{}] (Clickable)'.format(js[0]['artist'],js[0]['title'],js[0]['version'])), url="https://osu.ppy.sh/b/"+beatmap_id)
                em.set_thumbnail(url='https://b.ppy.sh/thumb/'+str(js[0]['beatmapset_id'])+'.jpg')
                return em

    # processing if a mapset
    async def _beatmapset(self, beatmapset_id, modsEnum, mods_str):
        #http://osu.gatari.pw/api/v1/pp b= c= a= m= x(misses)=
                async  with aiohttp.ClientSession() as session:
                    async with session.get(osu_api + '/get_beatmaps', params = {'k': osu_api_key, 's' : beatmapset_id}) as r:
                        js = await r.json()
                    async with session.get('http://osu.gatari.pw/api/v1/pp', params={'b':js[0]['beatmap_id'], 'm':modsEnum}) as r1:
                        a = await r1.json()
                        em = discord.Embed(description=('**Mapper: **' + js[0]['creator']) +
                                                    '   **BPM: **' + js[0]['bpm'] +'   **Stars:**  '+str(round(float(a["stars"]), 2))+star_rating(float(a["stars"]))+
                                                    '\n**AR: **' + js[0]['diff_approach'] +
                                                    '   **OD: **' + js[0]['diff_overall'] +
                                                    '   **HP: **' + js[0]['diff_drain']+
                                                    '   **Max Combo: **' + js[0]['max_combo'], colour = 0xCC5288)
                        em.add_field(name='----------------PP: {}--------------------'.format(mods_str),value='**100%:** {}pp **99%:** {}pp **98%:** {}pp **95%:** {}pp'.format(a['pp'][0],a['pp'][1],a['pp'][2],a['pp'][3]))
                        em.set_author(name=(js[0]['artist']+' - '+js[0]['title']+' ['+js[0]['version']+'] (Clickable)'), url="https://osu.ppy.sh/b/"+beatmapset_id)
                        em.set_thumbnail(url='https://b.ppy.sh/thumb/' + str(js[0]['beatmapset_id']) + '.jpg')
                        return em

    # --- osu screenshot ---
    async def find_url(self, message):
        search_for_pic_url = re.search(r'http[s]?://.*.(?:png|jpg|gif|svg|jpeg)', message.content)
        # --- image isn't a link ---
        if message.attachments:
            msg = await self.bot.send_message(message.channel, "Found an image, processing...")
            async  with aiohttp.ClientSession() as session:
                async with session.get(message.attachments[0]["url"]) as r1:
                    try:
                        await self.bot.send_message(message.channel, embed=await self.ocr_for_attach(r1))
                    except discord.errors.HTTPException as e:
                        print(str(e)+ "\nURL:"+search_for_pic_url.group(0))
                    finally:
                        await self.bot.delete_message(msg)

        # --- image is a link ---
        if search_for_pic_url:
            msg = await self.bot.send_message(message.channel, "Found an image, processing...")
            async  with aiohttp.ClientSession() as session:
                async with session.get(search_for_pic_url.group(0)) as r1:
                    try:
                        await self.bot.send_message(message.channel, embed=await self.ocr_for_attach(r1))
                    except discord.errors.HTTPException as e:
                        print(str(e)+ "\nURL:"+search_for_pic_url.group(0))
                    finally:
                        await self.bot.delete_message(msg)

            
    # --- scanning image ---
    async def ocr_for_attach(self, r1):
        ratio = 0
        index = None
        buffer = BytesIO(await r1.read())
        im = Image.open(buffer)
        height = im.height
        width = im.width
        im = im.crop((0, 0, width, 0.125*height))
        text = pytesseract.image_to_string(im)
        if "Played by" in text:
                start = text.rfind("Played by") + 9
                finish = text.rfind("on")
                nick = text[start:finish]
                text = text.split("\n")
                print(text)
                beatmap_title = text[0]
                nick, beatmap_title = self.replaces(nick, beatmap_title)
                async  with aiohttp.ClientSession() as session:
                    async with session.get("http://api.gatari.pw/beatmaps/search", params={'q': beatmap_title}) as r:
                        beatmaps_search = await r.json()
                        beatmap = beatmaps_search["result"][0]
                title_by_request = beatmap["artist"] + " — " + beatmap["title"]
                for _index, _map in enumerate(beatmap["beatmaps"]):
                    temp_title =  "{} [{}]".format(title_by_request, _map["version"]) 
                    s = SequenceMatcher(None, beatmap_title, temp_title)
                    if s.ratio() > ratio:
                        ratio = s.ratio()
                        index = _index
                beatmap_id = beatmap["beatmaps"][index]["beatmap_id"]
                title =  "{} [{}]".format(title_by_request, beatmap["beatmaps"][index]["version"]) 
                async  with aiohttp.ClientSession() as session:
                    async with session.get(osu_api + '/get_user', params={'k': osu_api_key, 'u': nick.strip()}) as r:
                        js = await r.json()
                        u_id = js[0]["user_id"]
                        nick = js[0]["username"]
                        pp_raw = js[0]["pp_raw"]
                        pp_rank = js[0]["pp_rank"]
                        country = js[0]["country"]
                        pp_country_rank = js[0]["pp_country_rank"]
                    async with session.get('https://osu.ppy.sh/api/get_scores', params={'k': osu_api_key, 'b' : beatmap_id, 'u': u_id}) as r:
                        d = await r.json()
                        if len(d)>0: # если больше одного скора, то выбирает скор, который отображается на оффе
                            score = d[0]['score']
                            pp = d[0]['pp']
                            combo =  d[0]['maxcombo']
                            count50 = d[0]['count50']
                            count100 = d[0]['count100']
                            count300 = d[0]['count300']
                            misses = d[0]['countmiss']
                            rank = d[0]['rank']
                            m = d[0]['enabled_mods']
                            user_id = d[0]['user_id']
                            accuracy = acc_calc(int(misses),int(count50),int(count100),int(count300))
                        else:
                            return
                    async with session.get('https://osu.ppy.sh/api/get_beatmaps', params={'k':config.osu_api_key, 'b':beatmap_id}) as s:
                        js2 = await s.json() 
                        em = discord.Embed(description=('[{}](https://osu.ppy.sh/b/{}){} **{}**\n  **Score:** {}   **Accuracy:** {}\n  <:hit300:427941500035268608>{} <:hit100:427941500274475039>{}  <:hit50:427941499846787084>{}  <:hit0:427941499884535829>{}\n  **Combo:** {}/{}   **Rank:** {}   **PP:** {}'.format(title, 
                        beatmap_id,
                        star_rating(float(js2[0]['difficultyrating'])),
                        readableMods(int(m)),
                        score,
                        accuracy,
                        count300,
                        count100,
                        count50,
                        misses,
                        combo,
                        js2[0]['max_combo'],
                        rank_emoji(rank),
                        pp)))             
                        em.set_author(name=("{} {}pp #{} ({}#{})".format(nick, pp_raw, pp_rank, country, pp_country_rank)), url='https://osu.ppy.sh/u/{}'.format(u_id), icon_url='https://a.ppy.sh/{}_1.png'.format(u_id))
                        em.set_thumbnail(url='https://b.ppy.sh/thumb/' + str(js2[0]['beatmapset_id']) + '.jpg')
                        em.set_footer(text="  {}".format(datetime.datetime.now().strftime('%c')),icon_url="https://upload.wikimedia.org/wikipedia/commons/4/41/Osu_new_logo.png")
                        return em

    def replaces(self, nick, beatmap_title):
        nick = nick.replace(",", "_")
        nick = nick.replace("—", "-")
        nick = nick.replace("><", "x", 1)
        nick = nick.replace("|<", "k")
        nick = nick.replace("l<", "k")
        nick = nick.replace("'", "")
        beatmap_title = beatmap_title.replace("{", "[")
        beatmap_title = beatmap_title.replace("}", "]")
        return nick, beatmap_title


def setup(bot):
    osu = Osu(bot)
    bot.add_listener(osu.process_user, "on_message")
    bot.add_listener(osu.process_beatmap, "on_message")
    bot.add_listener(osu.find_url, "on_message")
    bot.add_cog(osu)