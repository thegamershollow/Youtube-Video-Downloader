# imports
from pytube import YouTube
from pytube import Playlist
import os
import sys
import re
import requests
import shutil

# function to remove emojis and other unicode characters that could throw errors
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

# function to convert a string into alphanumeric text.
def make_alpha_numeric(string):
    return ''.join(char for char in string if char.isalnum())

# function to download a single youtube video
def downloadVideo(url):
    # set 'yt' variable to Youtube function
    yt = YouTube(url)
    # removes emoji from the title of the video
    ytTitle = remove_emojis(yt.title)
    print(f"Downloading '{ytTitle}' to {os.getcwd()}")
    # get the thumbnail url
    thumbnail = yt.thumbnail_url
    # get the thumbnail from url using requests
    response = requests.get(thumbnail, stream=True)
    # open the file that is grabbed from requests and saves it
    with open(f"{ytTitle}.jpg", 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    # get the video stream
    video = yt.streams.filter(file_extension='mp4',only_audio=False)
    # get the highest res of the video 
    dVideo = video[1]
    # downloads the video
    dVideo.download(filename=f"{ytTitle}.mp4")
    print(f"Downloaded '{ytTitle}' succesfully!")

# function to download an entire youtube playlist
def downloadPlaylist(url):
    # set 'ytPlaylist' variable to the Playlist function
    ytPlaylist = Playlist(url)
    # converts the video title to an alphanumeric string
    folderName = make_alpha_numeric(ytPlaylist.title)
    # creates an empty folder to save the videos to
    os.mkdir(folderName)
    # gets total video count in playlist
    totalVideoCount = len(ytPlaylist.videos)
    print("Total videos in playlist: ", totalVideoCount)
    for index, video in enumerate(ytPlaylist.videos, start=1):
        print(f"Downloading: {video.title}")
        # removes the emojis from the video title
        ytTitle = remove_emojis(video.title)
        # gets the thumbnail url
        thumbnail = video.thumbnail_url
        # get the thumbnail from url using requests
        response = requests.get(thumbnail, stream=True)
        # open the file that is grabbed from requests and saves it
        with open(f"{ytTitle}.jpg", 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        # gets the video stream
        videos = video.streams.filter(file_extension='mp4',only_audio=False)
        # gets the highest res of the video
        dVideo = videos[1]
        # downloads the video
        dVideo.download(filename=f"{ytTitle}.mp4",output_path=folderName)
    print("Downloaded all videos succesfully.")

# prompt for the programs terminal interface.
prompt = input("YouTube Video/Playlist Downloader\n\n1. Download a video\n2. Download a playlist\n3. Exit\n: ")
# if statement to get the value inputed in the prompt
if prompt == "1":
    i = input("Enter the video URL: ")
    downloadVideo(i)
elif prompt == "2":
    i = input("Enter the playlist url: ")
    downloadPlaylist(i)
elif prompt == "3":
    sys.exit("Exited.")
elif int(prompt) >= 3:
    print("Not a valid option.")