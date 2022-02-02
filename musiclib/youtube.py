import discord
import pafy
import re, urllib.request
import requests

class Track():
    def __init__(self, audiosource, title, duration=0, url=None, stream=None, pafy_obj=None, yt_id=None):
        self.source = audiosource
        self.title = title
        self.duration = duration
        self.url = url
        self.pafy_obj = pafy_obj
        self.stream = stream
        self.yt_id = yt_id

def url_to_pafy(yt_url):
    # Return None: URL Doesn't Exist
    if requests.get(f"https://www.youtube.com/oembed?url={yt_url}").status_code != 200:  # Status code 400 if url doesn't exist
        return None

    pafy_obj = pafy.new(yt_url)  # creates a new pafy object

    return pafy_obj

def streamURL_to_DCsource(streamURL):
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
    DC_audio_source = discord.FFmpegPCMAudio(streamURL, **FFMPEG_OPTIONS)  # converts the youtube audio source into a source discord can use
    return DC_audio_source

def pafy_to_track(pafy_obj):
    audio_stream = pafy_obj.getbestaudio()  # gets a stream object
    audio_source = streamURL_to_DCsource(audio_stream.url)

    url = f"https://youtu.be/{pafy_obj.videoid}"
    return Track(audio_source, pafy_obj.title, int(pafy_obj.length), url, audio_stream, pafy_obj, yt_id=pafy_obj.videoid)

def search(searchTerm):
    # Returns 1st URL
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + searchTerm.replace(" ", "+"))   # Note that str.replace() does NOT replace in-place, duh cause strings ain't mutable
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return "https://www.youtube.com/watch?v="+video_ids[0]

def sendMP3(yt_id):
    # Return None: URL Doesn't Exist
    if requests.get(f"https://www.youtube.com/oembed?url=https://youtu.be/{yt_id}").status_code != 200:  # Status code 400 if url doesn't exist
        return None

    # We will make use of the api at https://www.yt-download.org/api/button/{ftype: mp3/mp4/etc}/{YouTube video ID}
    # The site gives us a bunch of buttons, but we will scrape the exact link of each buttons instead
    # because pressing the buttons on the site gives ads.
