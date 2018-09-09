import asyncio
import discord
from discord.ext import commands
import datetime

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')



def embed_msg(description, author:str = None):
    em = discord.Embed(description = description, color = 0x1E90FF)
    if author:
        em.set_author(name = author)
    return em

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '**{0.title}** uploaded by **{0.uploader}** and requested by **{1.display_name}**'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())
        

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    def playlist(self):
        pass

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            em = discord.Embed(description = str(self.current), color = 0x1E90FF)
            em.set_author(name = "Now playing")
            await self.bot.send_message(self.current.channel, embed = em)
            self.current.player.start()
            await self.play_next_song.wait()

class Music:
    """Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def timer(self):
        now = time.time()
        timeout = 60

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state
            # self.voice_states[server_id][time]

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass


    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx, *, channel : discord.Channel):
        """Joins a voice channel."""
        try:
            await self.create_voice_client(channel)
        except discord.ClientException:
            await self.bot.say(embed = embed_msg('Already in a voice channel...'))
        except discord.InvalidArgument:
            await self.bot.say(embed = embed_msg('This is not a voice channel...'))
        else:
            await self.bot.say(embed = embed_msg(description = str(channel.name), author= 'Ready to play audio in '))

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say(embed = embed_msg(description = 'You are not in a voice channel.'))
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)
            await self.bot.say(embed = embed_msg(description = str(summoned_channel), author = "Joined"))

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        """Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'format' : 'bestaudio/best',
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:        
            await self.bot.send_message(ctx.message.channel, embed = embed_msg(description='{}: {}'.format(type(e).__name__, e), author="An error occurred while processing this request"))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say(embed = embed_msg(description = str(entry), author = 'Enqueued '))
            await state.songs.put(entry)

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int):
        """Sets the volume of the currently playing song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            await self.bot.say(embed = embed_msg('Set the volume to **{:.0%}**'.format(player.volume)))

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        """Pauses the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """Resumes the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say(embed = embed_msg('Not playing any music right now...'))
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await self.bot.say(embed = embed_msg('Requester requested skipping song...'))
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 23190:
                await self.bot.say(embed = embed_msg('Skip vote passed, skipping song...'))
                state.skip()
            else:
                await self.bot.say(embed = embed_msg('Skip vote added, currently at [{}/3]'.format(total_votes)))
        else:
            await self.bot.say(embed = embed_msg('You have already voted to skip this song.'))

    @commands.command(pass_context=True, no_pm=True)
    async def np(self, ctx):
        """Shows info about the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say(embed = embed_msg('Not playing anything.'))
        else:
            await self.bot.say(embed = embed_msg(description = str(state.current), author = "Now playing"))
    
    @commands.command(pass_context=True, name = "playlist")
    async def _playlist(self, ctx):
        """Shows playlist."""
        playlist = []
        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say(embed = embed_msg('Not playing anything.'))
        else:
            playl = list(state.songs._queue)
            for i,s in enumerate(playl, 1):
                playlist.append("**{}** - {}".format(i, s.player.title))
            await self.bot.say(embed = embed_msg(description = "\n".join(playlist), author = "Playlist"))


def setup(bot):
    bot.add_cog(Music(bot))

