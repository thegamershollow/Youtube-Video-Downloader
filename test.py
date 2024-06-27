from pytube import YouTube
import re
import requests
import shutil
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


url = 'https://m.youtube.com/watch?v=gK-RF5CVu_M'
yt = YouTube(url)
download = yt.streams.filter(file_extension='mp4',only_audio=False)
ytTitle = remove_emojis(yt.title)
thumbnail = yt.thumbnail_url
response = requests.get(thumbnail, stream=True)
with open(f"{ytTitle}.jpg", 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response