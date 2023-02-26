import os
import pytube
from moviepy.editor import AudioFileClip
import mutagen

def download_audio(url):
    # Create YouTube object and extract audio stream
    yt = pytube.YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Set output file names
    output_mp4 = f"{yt.title}.mp4"
    output_mp3 = f"{yt.title}.mp3"

    # Download audio stream to MP4 file
    audio_stream.download(output_path=os.getcwd(), filename=output_mp4)

    # Use moviepy to convert an mp4 to an mp3 with metadata support. Delete mp4 afterwards
    audio_clip = AudioFileClip(output_mp4)
    output_mp3_with_metadata = output_mp3.replace(".mp3", "-with-metadata.mp3")
    audio_clip.write_audiofile(output_mp3_with_metadata)
    audio_clip.close()
    os.remove(output_mp4)

    update_metadata(output_mp3_with_metadata, yt.title, yt.author)

def update_metadata(file_path, title, artist, album=""):
    # Update the file metadata according to YouTube video details
    with open(file_path, 'r+b') as file:
        media_file = mutagen.File(file, easy=True)
        media_file["title"] = title
        if album: media_file["album"] = album
        media_file["artist"] = artist
        media_file.save()


print(Audio saved)
