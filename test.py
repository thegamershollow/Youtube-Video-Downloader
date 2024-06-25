from pytube import YouTube
import os 

# function to download a single youtube video
def downloadVideo(url):
    # set yt to use the youtube function from pytube
    yt = YouTube(url)
    
    # get the video title
    ytTitle = yt.title
    
    video = yt.streams.first()
    print(video)
    
    streams = yt.streams
    x = streams.filter(adaptive=True,progressive=False)
    #for each in x:
    #    print(each)
    # download video
    #video.download()

downloadVideo("https://m.youtube.com/watch?v=Kq6GO5nNoxM")