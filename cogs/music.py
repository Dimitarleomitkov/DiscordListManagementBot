import discord
import urllib
import re
import pafy
from youtube_dl import YoutubeDL
from discord.ext import commands
from discord import FFmpegPCMAudio
import nacl

async def setup(bot):
    await bot.add_cog(music(bot))

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio/best'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("music module is loaded.")

    @commands.command(  name = 'mplay',
                        help = 'The bot will connect to the voice chat and play the song.',
                        brief = '- The bot will connect to the voice chat and play the song.')
    async def play_func(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel

        if voice_channel is None:
            await ctx.send("Please, connect to a voice channel.")
        elif self.is_paused:
            self.vc.resume()
        else:
            song_link = self.search_yt(query)

            # I need to see what happens if I find nothing
            await ctx.send("Song added to the queue")
            self.music_queue.append([song_link, voice_channel])

            if self.is_playing == False:
                await self.play_music(ctx)

    def search_yt(self, search_str):
        url = urllib.parse.quote(search_str)
        html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={url}")
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        link = f"https://www.youtube.com/watch?v={video_ids[0]}"
        return link

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel.")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            song = pafy.new(self.music_queue[0][0])
            audio = song.getbestaudio()
            source = FFmpegPCMAudio(audio.url, **self.FFMPEG_OPTIONS)
            self.music_queue.pop(0)

            self.vc.play(source, after = lambda e: self.play_next())
        else:
            self.is_playing = False




    # def play_next(self):
    #     if len(self.music_queue) > 0:
    #         self.is_playing = True

    #         m_url = self.music_queue[0][0]['source']

    #         self.music_queue.pop(0)
    #         self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
    #     else:
    #         self.is_playing = False

    

    

    # @commands.command(  name = 'mpause',
    #                     help = 'pause the music.',
    #                     brief = '- Pause the music.')
    # async def pause(self, ctx, *args):
    #     if self.is_playing:
    #         self.is_playing = False
    #         self.is_paused = True
    #         self.vc.pause()
    #     elif self.is_paused:
    #         self.is_playing = True
    #         self.is_paused = False
    #         self.vc.resume()

    # @commands.command(  name = 'mresume',
    #                     help = 'resume the music.',
    #                     brief = '- Resume the music.')
    # async def resume(self, ctx, *args):
    #     if self.is_paused:
    #         self.is_playing = True
    #         self.is_paused = False
    #         self.vc.resume()

    # @commands.command(  name = 'mskip',
    #                     help = 'skip the song.',
    #                     brief = '- Skip the song.')
    # async def skip(self, ctx, *args):
    #     if self.vc != None and self.vc:
    #         self.vc.stop()
    #         await self.play_music(ctx)

    # @commands.command(  name = 'mqueue',
    #                     help = 'displays all the songs currently in the queue.',
    #                     brief = '- Displays all the songs currently in the queue.')
    # async def queue(self, ctx):
    #     retval = ""

    #     for i in range(0, len(self.music_queue)):
    #         if i > 10:
    #             break

    #         retval += self.music_queue[i][0]['title'] + '\n'

    #     if retval != "":
    #         await ctx.send(retval)
    #     else:
    #         await ctx.send("No music in the queue.")

    # @commands.command(  aliases = ['mbin', 'mclear'],
    #                     help = 'Stops the current song and clears the queue.',
    #                     brief = '- Stops the current song and clears the queue.')
    # async def clear(self, ctx, *args):
    #     if self.vc != None and self.is_playing:
    #         self.vc.stop()
    #     self.music_queue = []
    #     await ctx.send("Music queue cleared.")

    # @commands.command(  aliases = ['mleave', 'mdisconnect'],
    #                     help = 'Kicks the bot from the voice channel.',
    #                     brief = '- Kicks the bot from the voice channel.')
    # async def leave(self, ctx):
    #     self.is_playing = False
    #     self.is_paused = False
    #     await self.vc.disconnect()