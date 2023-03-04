import os
import telethon.sync
from telethon import TelegramClient, events, functions, types
from pytube import YouTube
from moviepy.editor import *
import mutagen

# replace the values below with your own
api_id = 11169140
api_hash = '4b185d543b0d1a84bed3a462ade1498f'
bot_token = '5542310588:AAEIZ8lDrbRyQGtjOG33Tf8Ly_lpiLBwYsk'

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='^/start'))
async def start(event):
    await event.respond('Hello, please send me a YouTube link.')

@client.on(events.NewMessage)
async def convert_video(event):
    try:
        url = event.message.text
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        output_mp4 = f"{yt.title}.mp4"
        audio_stream.download(output_path='./downloads', filename=output_mp4)
        output_mp3 = f"{yt.title}.mp3"
        audio_clip = AudioFileClip(os.path.join('./downloads', output_mp4))
        audio_clip.write_audiofile(os.path.join('./downloads', output_mp3))
        audio_clip.close()
        os.remove(os.path.join('./downloads', output_mp4))
        title = yt.title
        artist = yt.author
        album = ""
        update_metadata(os.path.join('./downloads', output_mp3), title, artist, album)
        await client.send_file(event.chat_id, os.path.join('./downloads', output_mp3))
    except Exception as e:
        print(e)
        await event.respond('Sorry, an error occurred while processing your request.')

def update_metadata(file_path: str, title: str, artist: str, album: str="") -> None:
    # Update the file metadata according to YouTube video details
    with open(file_path, 'r+b') as file:
        media_file = mutagen.File(file, easy=True)
        media_file["title"] = title
        if album:
            media_file["album"] = album
        media_file["artist"] = artist
        media_file.save(file)

client.run_until_disconnected()
