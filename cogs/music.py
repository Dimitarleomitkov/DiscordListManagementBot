import discord
from youtube_dl import YoutubeDL
from discord.ext import commands


async def setup(bot):
    await bot.add_cog(music(bot))


class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        self.YDL_OPTIONS = {'noplaylist': 'True',
                            'quiet': 'True',
                            'audio-quality': '0',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '320'
                            }]}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                                'options': '-vn'}
        self.vc = None


    @commands.Cog.listener()
    async def on_ready(self):
        print("music module is loaded.")


    @commands.command(  name = 'mplay',
                        help = 'The bot will connect to the voice chat and play the song.',
                        brief = '- The bot will connect to the voice chat and play the song.')
    async def play_func(self, ctx, *args):
        try:
            voice_channel = ctx.author.voice.channel
        except Exception as e:
            await ctx.send("Please, connect to a voice channel.")
            return

        query = " ".join(args)
        songs = query.split(',')
        for song in songs:
            if self.is_paused:
                self.vc.resume()
            else:
                song = self.search_yt(song)

                if type(song) == type(True):
                    await ctx.send("Could not download the song. Incorrect format, try a different keyword")
                else:
                    self.music_queue.append([song, voice_channel])
                    await ctx.send(f"{song['title']} added to the queue")

                    if self.is_playing == False:
                        await self.check_and_connect(ctx)
                        self.play_next('play_func')
                        self.is_playing = True


    def search_yt(self, search_str):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{search_str}", download = False)['entries'][0]
            except Exception:
                return False

        def find_index (the_list):
            i = 0
            save = 0
            for attribute in the_list:
                if attribute["format_id"] == '251':
                    return i
                i += 1

        index = find_index(info['formats'])

        return {'source': info['formats'][index]['url'], 'title': info['title']}


    def play_next(self, from_where):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            if from_where != 'skip':
                self.music_queue.pop(0)
            
            source = discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS)
            self.vc.play(source, after = lambda e: self.play_next('callback'))
        else:
            self.is_playing = False


    async def check_and_connect(self, ctx):
        if len(self.music_queue) > 0:
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel.")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
        else:
            self.is_playing = False
            await self.vc.disconnect()


    @commands.command(  name = 'mpause',
                        help = 'pause the music.',
                        brief = '- Pause the music.')
    async def pause(self, ctx):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()


    @commands.command(  name = 'mresume',
                        help = 'resume the music.',
                        brief = '- Resume the music.')
    async def resume(self, ctx):
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()


    @commands.command(  aliases = ['mskip', 'mnext'],
                        help = 'skip the song.',
                        brief = '- Skip the song.')
    async def skip(self, ctx):
        if len(self.music_queue) <= 0:
            await self.vc.disconnect()

        if self.vc != None and self.vc:
            self.vc.stop()
            self.play_next('skip')


    @commands.command(  aliases = ['mqueue', 'mlist'],
                        help = 'displays all the songs currently in the queue.',
                        brief = '- Displays all the songs currently in the queue.')
    async def queue(self, ctx):
        retval = ""

        for i in range(0, len(self.music_queue)):
            if i > 10:
                break

            retval += self.music_queue[i][0]['title'] + '\n'

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in the queue.")


    @commands.command(  aliases = ['mbin', 'mclear'],
                        help = 'Stops the current song and clears the queue.',
                        brief = '- Stops the current song and clears the queue.')
    async def clear(self, ctx, *args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Music queue cleared.")


    @commands.command(  aliases = ['mleave', 'mdisconnect'],
                        help = 'Kicks the bot from the voice channel.',
                        brief = '- Kicks the bot from the voice channel.')
    async def leave(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
    