import os
import pytube
from moviepy.editor import *
from mutagen.mp3 import MP3, ID3, TIT2, TPE1, TALB

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
audio_clip = AudioFileClip(output_mp4)
audio_clip.write_audiofile(output_mp3, bitrate="192k")
audio_clip.close()

# Add metadata to the output MP3 file
audio = MP3(output_mp3, ID3=ID3)
audio["TIT2"] = TIT2(encoding=3, text=yt.title)
audio["TPE1"] = TPE1(encoding=3, text=yt.author)
audio["TALB"] = TALB(encoding=3, text=yt.title)
audio.save()


# Delete MP4 file
os.remove(output_mp4)

print(f"Audio saved to {output_mp3}")
