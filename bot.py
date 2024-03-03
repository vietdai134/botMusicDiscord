import discord
from discord.ext import commands
import yt_dlp
import asyncio
import traceback
import time
import math

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# FFmpeg options
ffmpeg_options = {
    'options': '-vn -reconnect 1 -loglevel debug',
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!play'):
        # Get YouTube URL from the message
        url = message.content.split(' ', 1)[1]

        # # Call the play_music function
        # await play_music(message, url)
        bot.loop.create_task(play_music(message, url))

# async def play_music(message, url):
#     voice_channel = message.author.voice.channel

#     if not voice_channel.permissions_for(message.guild.me).connect or \
#        not voice_channel.permissions_for(message.guild.me).speak or \
#        not voice_channel.permissions_for(message.guild.me).use_voice_activation:
#         await message.channel.send("I don't have the necessary permissions.")
#         return

#     # Connect directly to the specified channel
#     vc = await voice_channel.connect()

#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#         'ffmpeg': 'C:\\ffmpeg',  # Update with the correct path to FFmpeg
#         'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save the downloaded file
#     }

#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(url, download=False)
#             audio_url = info['url']
#             duration = info.get('duration', 0)

#         print(f'The direct media URL is: {audio_url}')

#         vc.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_options), after=lambda e: print('Playback finished'))

#         # Display progress bar
#         progress_bar_length = 20
#         start_time = time.time()
#         playback_finished = False
#         while not playback_finished:
#             elapsed_time = time.time() - start_time
#             progress = min(int(elapsed_time / duration * progress_bar_length), progress_bar_length)
#             progress_bar = f'[{progress * "="}{(progress_bar_length - progress) * "-"}] {math.floor(elapsed_time)}/{duration}'
#             print(progress_bar, end='\r')
#             await asyncio.sleep(1)

#             # Check if the bot has finished playing
#             playback_finished = not vc.is_playing()

#         print()  # Move to a new line after the progress bar
        
#         # Disconnect after playback
#         while vc.is_playing():
#             await asyncio.sleep(1)
#         await vc.disconnect()
#         await message.channel.send(f'Finished playing: {info["title"]}' if "title" in info else 'Finished playing: Unknown Title')

#     except Exception as e:
#         error_message = f'An error occurred: {str(e)}'
#         print(error_message)
#         traceback.print_exc()  # Print traceback for debugging
#         await message.channel.send(error_message)

async def play_music(message, url):
    voice_channel = message.author.voice.channel

    if not voice_channel.permissions_for(message.guild.me).connect or \
       not voice_channel.permissions_for(message.guild.me).speak or \
       not voice_channel.permissions_for(message.guild.me).use_voice_activation:
        await message.channel.send("I don't have the necessary permissions.")
        return

    # Connect directly to the specified channel
    vc = await voice_channel.connect()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg': 'C:\\ffmpeg',  # Update with the correct path to FFmpeg
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save the downloaded file
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
            duration = info.get('duration', 0)

        print(f'The direct media URL is: {audio_url}')

        def after_play(error):
            if error:
                print(f"Error in playback: {error}")

            # Disconnect after playback
            asyncio.run_coroutine_threadsafe(vc.disconnect(), bot.loop)
            print('Playback finished')

        audio_source = discord.FFmpegPCMAudio(audio_url, **ffmpeg_options)
        vc.play(audio_source, after=after_play)

        # Display progress bar
        progress_bar_length = 20
        start_time = time.time()
        playback_finished = False

        while not playback_finished:
            elapsed_time = time.time() - start_time
            progress = min(int(elapsed_time / duration * progress_bar_length), progress_bar_length)
            progress_bar = f'[{progress * "="}{(progress_bar_length - progress) * "-"}] {math.floor(elapsed_time)}/{duration}'
            print(progress_bar, end='\r')

            # Check if the bot has finished playing
            playback_finished = not vc.is_playing() and not vc.source  # Ensure both is_playing and source are False

            # Sleep for a shorter interval
            await asyncio.sleep(0.5)

        print()  # Move to a new line after the progress bar

    except Exception as e:
        error_message = f'An error occurred: {str(e)}'
        print(error_message)
        traceback.print_exc()  # Print traceback for debugging
        await message.channel.send(error_message)

bot.run('MTE4Njg5NDQwMjc5MTE2NjAwMw.GEUBsf.Sq8BlT4moX3MV6KtzTpCwJuGE215KQB2txZFV0')
