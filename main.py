from telethon import TelegramClient, events
from moviepy.editor import AudioFileClip
import pytube
import os
import mutagen

# replace the values below with your own
api_id = 11169140
api_hash = '4b185d543b0d1a84bed3a462ade1498f'
bot_token = '5542310588:AAEIZ8lDrbRyQGtjOG33Tf8Ly_lpiLBwYsk'

bot = TelegramClient('youtube_downloader', api_id, api_hash).start(bot_token=bot_token)

# Define the function for downloading and converting YouTube videos
def download_and_convert(url):
    # Create YouTube object and extract audio stream
    try:
        yt = pytube.YouTube(url)
    except pytube.exceptions.RegexMatchError:
        return "The provided URL is not supported."
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Set output file names
    output_mp4 = f"{yt.title}.mp4"

    # Download audio stream to MP4 file
    audio_stream.download(output_path=os.getcwd(), filename=output_mp4)

    # Use moviepy to convert the MP4 file to an MP3 file with metadata support, then delete the MP4 file
    audio_clip = AudioFileClip(output_mp4)
    output_mp3 = f"{yt.title}.mp3"
    audio_clip.write_audiofile(output_mp3)
    audio_clip.close()
    os.remove(output_mp4)

    # Get video details from YouTube
    title = yt.title
    artist = yt.author
    album = ""

    # Update metadata of MP3 file
    update_metadata(output_mp3, title, artist, album)

    return output_mp3

# Define the function for updating metadata of MP3 files
def update_metadata(file_path: str, title: str, artist: str, album: str="") -> None:
    # Update the file metadata according to YouTube video details
    with open(file_path, 'r+b') as file:
        media_file = mutagen.File(file, easy=True)
        media_file["title"] = title
        if album:
            media_file["album"] = album
        media_file["artist"] = artist
        media_file.save(file)

# Set up event handler for incoming messages
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Welcome to the YouTube downloader bot! Send me a YouTube video URL and I will convert it to MP3 for you.')

@bot.on(events.NewMessage)
async def handle_message(event):
    if event.message.text.startswith('http'):
        url = event.message.text
        result = download_and_convert(url)
        if result:
            await bot.send_file(event.chat_id, result)
        else:
            await event.respond("Sorry, I couldn't download and convert that YouTube video.")

# Start the bot
bot.run_until_disconnected()
