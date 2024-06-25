from pytube import YouTube
import os 

# function to download a single youtube video
def downloadVideo(url):
    yt = YouTube(url)
    ytTitle = yt.title
    print(f"Downloading '{ytTitle}' to {os.getcwd()}")
    video = yt.streams.get_highest_resolution().download()
    print(f"Downloaded '{ytTitle}' succesfully!")