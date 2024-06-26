from pytube import YouTube

url = 'https://m.youtube.com/watch?v=X9SoIejJjwA'
yt = YouTube(url)
download = yt.streams.filter(file_extension='mp4',only_audio=False)
#for each in download:
#    print(each)
dVideo = download[1]
print(dVideo)
dVideo.download(filename="video.mp4")
#dVideo = download
#dVideo.download()