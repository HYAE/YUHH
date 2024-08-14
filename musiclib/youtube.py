import discord
import yt_dlp as youtube_dl
import re
import urllib.request
import requests


class Track():
    def __init__(self, audiosource, title, duration=0, url=None, streamURL=None, ytdl_info=None, yt_id=None):
        self.source = audiosource
        self.title = title
        self.duration = duration
        self.url = url
        self.streamURL = streamURL
        self.ytdl_info = ytdl_info
        self.yt_id = yt_id


def url_to_ytdl(yt_url):
    """Return None: URL Doesn't Exist."""
    if requests.get(f"https://www.youtube.com/oembed?url={yt_url}").status_code != 200:  # Status code 400 if url doesn't exist
        return None

    ytdl_options = {"format": "bestaudio/best"}
    ytdl = youtube_dl.YoutubeDL(ytdl_options)
    ytdl_info = ytdl.extract_info(yt_url, download=False)  # creates a new pafy object

    return ytdl_info


def streamURL_to_DCsource(streamURL):
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
    DC_audio_source = discord.FFmpegPCMAudio(streamURL, **FFMPEG_OPTIONS)  # converts the youtube audio source into a source discord can use
    return DC_audio_source


def ytdl_to_track(ytdl_info):
    audio_source = streamURL_to_DCsource(ytdl_info["url"])

    url = f"https://youtu.be/{ytdl_info['id']}"
    return Track(audio_source, ytdl_info["title"], int(ytdl_info["duration"]), url, ytdl_info["url"], ytdl_info, yt_id=ytdl_info['id'])


def search(searchTerm):
    """Return 1st URL."""
    query = urllib.parse.quote_plus(searchTerm, encoding="utf-8")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + query)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return "https://www.youtube.com/watch?v="+video_ids[0]

def sendMP3(yt_id):
    """Return None: URL Doesn't Exist."""
    if requests.get(f"https://www.youtube.com/oembed?url=https://youtu.be/{yt_id}").status_code != 200:  # Status code 400 if url doesn't exist
        return None

    # We will make use of the api at https://www.yt-download.org/api/button/{ftype: mp3/mp4/etc}/{YouTube video ID}
    # The site gives us a bunch of buttons, but we will scrape the exact link of each buttons instead
    # because pressing the buttons on the site gives ads.
