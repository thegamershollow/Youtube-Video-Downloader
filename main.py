from pytube import YouTube
from pytube import Playlist
import os 
import sys

def make_alpha_numeric(string):
    return ''.join(char for char in string if char.isalnum())

# function to download a single youtube video
def downloadVideo(url):
    yt = YouTube(url)
    ytTitle = yt.title
    print(f"Downloading '{ytTitle}' to {os.getcwd()}")
    video = yt.streams.get_highest_resolution().download()
    print(f"Downloaded '{ytTitle}' succesfully!")

# function to download an entire youtube playlist
def downloadPlaylist(url):
    ytPlaylist = Playlist(url)
    folderName = make_alpha_numeric(ytPlaylist.title)
    os.mkdir(folderName)
    totalVideoCount = len(ytPlaylist.videos)
    print("Total videos in playlist: ", totalVideoCount)
    for index, video in enumerate(ytPlaylist.videos, start=1):
        print("Downloading:", video.title)
        video.streams.get_highest_resolution().download(output_path=folderName)
    print("Downloaded all videos succesfully.")

prompt = input("YouTube Video/Playlist Downloader\n\n1. Download a video\n2. Download a playlist\n3. Exit\n: ")
if prompt == "1":
    i = input("Enter the video URL: ")
    downloadVideo(i)
if prompt == "2":
    i = input("Enter the playlist url: ")
    downloadPlaylist(i)
if prompt == "3":
    sys.exit("Exited.")
if int(prompt) <= 3:
    print("Not a valid option.")
