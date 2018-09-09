import discord
from discord.ext import commands
import aiohttp
import asyncio
import random
import config
import mods
from bs4 import BeautifulSoup
import datetime


sig_colors =['black', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'hex2255ee']

skillLabels = ["Stamina",
                    "Tenacity",
                    "Agility", 
                    "Accuracy", 
                    "Precision",
                    "Reaction", 
                    "Memory"
                ]


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

    @commands.command(pass_context=True)
    async def osuchan(self, ctx, *, name:str=None):
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
    @commands.command(pass_context= True)
    async def versus(self, ctx, player1, player2):
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
    
    @commands.group(pass_context=True)
    async def last1(self,ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_typing(ctx.message.channel)
            message = ctx.message.content.lower().split()
            nick = "".join(message[1:])
            # https://osu.gatari.pw/api/v1/users/scores/recent?id=1021&l=20&f=0&p=1&mode=0
            async with aiohttp.ClientSession() as session:
                async with session.get('https://osu.ppy.sh/api/get_user_recent', params={'k': config.osu_api_key, 'u': nick, 'limit': '1'}) as r:
                    if r.status == 200:
                        js = await r.json()
                        scores = len(js)
                        if scores>0:
                            bm = js[0]['beatmap_id']
                            score = js[0]['score']
                            combo =  js[0]['maxcombo']
                            count50 = js[0]['count50']
                            count100 = js[0]['count100']
                            count300 = js[0]['count300']
                            misses = js[0]['countmiss']
                            rank = js[0]['rank']
                            m = js[0]['enabled_mods']
                            accuracy = acc_calc(int(misses),int(count50),int(count100),int(count300))
                            user_id = js[0]['user_id']
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

    
    @last1.command()
    async def gatari(self, *, nick):
        await self.bot.send_typing(ctx.message.channel)
        async with aiohttp.ClientSession() as session:
            async with session.get('https://osu.gatari.pw/api/v1/users/scores/recent?id={}&l=1&f=0&p=1&mode=0'.format(nick)) as gt:
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
                    await self.bot.say(embed=em)
        
        
        
def setup(bot):
    bot.add_cog(Osu(bot))