import os
import pytube
from moviepy.editor import *

# Ask user for YouTube video URL
url = input("Enter YouTube video URL: ")

# Create YouTube object and extract audio stream
yt = pytube.YouTube(url)
audio_stream = yt.streams.filter(only_audio=True).first()

# Set output file names
output_mp4 = f"{yt.title}.mp4"
output_mp3 = f"{yt.title}.mp3"

# Download audio stream to MP4 file
audio_stream.download(output_path=os.getcwd(), filename=output_mp4)

# Convert MP4 file to MP3 file and add metadata
with AudioFileClip(output_mp4) as audio_clip:
    audio_clip.write_audiofile(output_mp3, bitrate="192k")
    audio_clip.reader.metadata["title"] = yt.title
    audio_clip.reader.metadata["artist"] = yt.author
    audio_clip.reader.metadata["album"] = yt.title
    audio_clip.reader.metadata.save()

# Delete MP4 file
os.remove(output_mp4)

print(f"Audio saved to {output_mp3}")
