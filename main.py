import os
import pytube
from moviepy.editor import *
import mutagen
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

# Convert MP4 file to MP3 file
print("Converting audio file...")
with AudioFileClip(output_mp4) as audio_clip:
    audio_clip.write_audiofile(output_mp3, bitrate="192k")
print("Conversion complete.")

# Update file metadata
update_metadata(output_mp3, yt.title, yt.author)
def update_metadata(file_path: str, title: str, artist: str, album: str="") -> None:
# Update the file metadata according to YouTube video details
with open(output_mp3, 'r+b') as file:
    media_file = mutagen.File(file, easy=True)
    media_file["title"] = yt.title
    media_file["artist"] = artist
    media_file["album"] = album
    media_file.save()

# Delete MP4 file
os.remove(output_mp4)

print(f"Audio saved to {output_mp3}")
