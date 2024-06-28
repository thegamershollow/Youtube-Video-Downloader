from pytube import YouTube, Playlist
import os
import re
import requests
import shutil
import argparse

# Function to remove emojis and other unicode characters that could throw errors
def remove_emojis(data):
    emoj = re.compile("["
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u"\U0001F680-\U0001F6FF"  # transport & map symbols
                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      u"\U00002500-\U00002BEF"  # chinese char
                      u"\U00002702-\U000027B0"
                      u"\U000024C2-\U0001F251"
                      u"\U0001f926-\U0001f937"
                      u"\U00010000-\U0010ffff"
                      u"\u2640-\u2642"
                      u"\u2600-\u2B55"
                      u"\u200d"
                      u"\u23cf"
                      u"\u23e9"
                      u"\u231a"
                      u"\ufe0f"  # dingbats
                      u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

# Function to convert a string into alphanumeric text
def make_alpha_numeric(string):
    return ''.join(char for char in string if char.isalnum())

# Function to download a single YouTube video
def download_video(url):
    yt = YouTube(url)

    # Removes emoji from the title of the video
    yt_title = remove_emojis(yt.title)

    print(f"Downloading '{yt_title}' to {os.getcwd()}")

    # Get the thumbnail url
    thumbnail = yt.thumbnail_url

    # Get the thumbnail from url using requests
    response = requests.get(thumbnail, stream=True)

    # Open the file that is grabbed from requests and save it
    with open(f"{yt_title}.jpg", 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

    # Get the video stream
    video_streams = yt.streams.filter(file_extension='mp4', only_audio=False)
    
    if video_streams:
        # Get the highest resolution of the video
        d_video = video_streams.get_highest_resolution()

        # Download the video
        d_video.download(filename=f"{yt_title}.mp4")

        print(f"Downloaded '{yt_title}' successfully!")
    else:
        print(f"No suitable streams found for '{yt_title}'")

# Function to download an entire YouTube playlist
def download_playlist(url):
    yt_playlist = Playlist(url)

    # Convert the playlist title to an alphanumeric string
    folder_name = make_alpha_numeric(yt_playlist.title)

    # Create an empty folder to save the videos to
    os.makedirs(folder_name, exist_ok=True)

    total_video_count = len(yt_playlist.videos)

    print("Total videos in playlist: ", total_video_count)

    # For loop to download all the videos
    for index, video in enumerate(yt_playlist.videos, start=1):
        print(f"Downloading: {video.title}")

        yt_title = remove_emojis(video.title)

        thumbnail = video.thumbnail_url

        response = requests.get(thumbnail, stream=True)
        with open(os.path.join(folder_name, f"{yt_title}.jpg"), 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        video_streams = video.streams.filter(file_extension='mp4', only_audio=False)
        
        if video_streams:
            d_video = video_streams.get_highest_resolution()
            d_video.download(filename=f"{yt_title}.mp4", output_path=folder_name)
        else:
            print(f"No suitable streams found for '{yt_title}'")

    print("Downloaded all videos successfully.")

# Create parser
parser = argparse.ArgumentParser(description="A YouTube video downloader")

# Add arg for video download
parser.add_argument('-v', '--video', type=str, help="Downloads a video if a valid URL is provided.")

# Add arg for playlist download
parser.add_argument('-p', '--playlist', type=str, help="Downloads a YouTube playlist if a valid URL is provided.")
args = parser.parse_args()

# Executes function if arg called
if args.video:
    download_video(args.video)

# Executes function if arg called
if args.playlist:
    download_playlist(args.playlist)
