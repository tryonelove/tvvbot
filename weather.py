import discord
from discord.ext import commands
import config
import aiohttp

weather_key = config.weather_key

class Weather():
    def __init__(self, bot):
        self.bot = bot
# aliases=['погода', 'weather']
    @commands.command(pass_context=True, aliases=['погода', 'weather'])
    async def _weather(self,ctx, *, city):
        emoji = ''
        descr = ''
        async with aiohttp.ClientSession() as session:
            async with session.get('http://api.openweathermap.org/data/2.5/weather',
                                   params={'q': city, 'APPID': weather_key}) as r:
                js = await r.json()
                C = round(float(js['main']['temp']) - 273, 2)
                wind = round(js['wind']['speed'] * 1.6093, 0)
                if js['weather'][0]['main'] == 'Clear':
                    emoji = ':mountain: '
                    descr = 'Clear'
                elif js['weather'][0]['main'] == 'Clouds':
                    emoji = ':cloud:'
                    descr = 'Clouds'
                elif js['weather'][0]['main'] == 'Rain':
                    emoji = ':umbrella:'
                    descr = 'Rain'
                elif js['weather'][0]['main'] == 'Thunderstorm':
                    emoji = ':cloud_lightning:'
                    descr = 'Thunderstorm'
                elif js['weather'][0]['main'] == 'Fog':
                    emoji = ':foggy:'
                    descr = 'Fog'
                elif js['weather'][0]['main'] == 'Drizzle':
                    emoji = ':umbrella:'
                    descr = 'Drizzle'
                elif js['weather'][0]['main'] == 'Snow':
                    emoji = ':cloud_snow:'
                    descr = 'Snow'
                em = discord.Embed(description=(emoji + descr +
                                                '\n**Temperature:** ' + str(C) +
                                                '\n**Humidity:** ' + str(js['main']['humidity']) + '%' +
                                                '\n**Wind speed:** ' + str(wind) + 'km/h'
                                                ))
                em.set_author(name=(city.capitalize() + ', ' + js['sys']['country']))
                await self.bot.say(embed=em)

def setup(bot):
    bot.add_cog(Weather(bot))