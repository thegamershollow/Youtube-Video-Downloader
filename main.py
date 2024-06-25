from pytube import YouTube

def downloadVideo(url):
    yt = YouTube(url)
    ytTitle = yt.title
    video = yt.streams.get_highest_resolution().download()
    print(f"Downloaded '{ytTitle}' succesfully!")

i = input("Type the url of the video you want to download: ")
downloadVideo(i)
