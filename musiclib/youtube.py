import discord
import pafy
import re, urllib.request
import requests

class Track():
    def __init__(self, audiosource, title, duration, url):
        self.source = audiosource
        self.title = title
        self.duration = duration
        self.url = url


def url_to_track(yt_url):
    # Return None: URL Doesn't Exist
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

    try:
        urllib.request.urlopen(f"https://www.youtube.com/oembed?url={yt_url}")  # Returns a json with details of the video, raise error 400 if url doesn't exist
    except urllib.error.HTTPError:
        return None

    pafy_obj = pafy.new(yt_url)  # creates a new pafy object

    audio_stream = pafy_obj.getbestaudio()  # gets a stream object
    audio_source = discord.FFmpegPCMAudio(audio_stream.url, **FFMPEG_OPTIONS)  # converts the youtube audio source into a source discord can use

    return Track(audio_source, pafy_obj.title, pafy_obj.length, yt_url)

def search(searchTerm):
    # Returns 1st URL
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + searchTerm.replace(" ", "+"))   # Note that str.replace() does NOT replace in-place, duh cause strings ain't mutable
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return "https://www.youtube.com/watch?v="+video_ids[0]
