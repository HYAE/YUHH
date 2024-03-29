import discord
import io
import re
import random
import html
import text_generator as textgen
import time
import os
import score_handler
from dotenv import load_dotenv
import comic_generator as comicgen
import asyncio
import pixabay_getter
import games.guess_the_drawing.guess_the_drawing as gtd
import games.guess4.guess4 as guess4
import games.trivia_game.trivia_game as trivia
import tenor_getter
import musiclib

intents = discord.Intents.default()
intents.message_content = True
# Make sure to go https://discord.com/developers/applications/
# and enable Message Content Intent (Privileged Gateway Intents)
client = discord.Client(intents=intents)

# Global variables
Guessing_Game = {"Ongoing": False,
                 "Answer": None,
                 "Chances": 5,
                 "Channel": None}

Trivia_Game = {"Ongoing": False,
               "Answer_Index": 0,
               "Answers": [],
               "Channel": None}

Conversation = {"Ongoing": False,
                "Channel": None}
# Each picture revealed is 1 try, category reveal is also 1 try
Guess4 = {"Ongoing": False,
          "Answer": None,
          "Try": 0,
          "Channel": None}

locked = False
error_replies = ["what?", "huh?", "come again?", "something's wrong!!",
                 "pardon?", "ugh?", "i just don't get it"]
music_dl_path = "./.musicdownloads"


@client.event
async def on_ready():
    print("Bot Ready.")


# For reference,
# https://discordpy.readthedocs.io/en/latest/migrating.html#sending-messages
@client.event
async def on_message(message):
    if message.author == client.user or locked:
        return

    # Remove spaces and lowercase it to make it consistent with commands
    unsanitised_message_content = message.content
    message.content = sanitise(message.content)

    if message.content == "ping":
        await message.channel.send(
            f"pong! ye chuan sucks {round(client.latency * 1000)} ms")
        return

    if message.content[:11] == "areyouthere":
        await message.channel.send("Yeah?")
        return

    if message.content == "testing":
        print_debug_info(message)
        await message.channel.send(f"What a nerd, {message.author.name}\n"
                                   f"Check your terminal.")
        return

    # LOG OUT
    if message.content == "gettheyuhhouttahere":
        await log_out(message)

    # INSULT
    if message.content == "insultme":
        await insult(message)

    # JOKE
    if message.content == "tellmeajoke":
        await joke(message)

    # INSPIRATIONAL QUOTE
    if message.content == "inspireme":
        await inspire(message)

    # PRINT SCORES
    if message.content == "showmescores":
        await show_scores(message)

    # COMPLIMENT
    if message.content == "complimentme" or message.content == "praiseme":
        await compliment(message)

    # PICKUP LINE
    if message.content == "pickmeup":
        await message.channel.send(textgen.generate_pickup_line())
        return

    # COMIC GENERATOR
    if message.content == "showmeacomic":
        await show_comic(message)
        return

    # CHEER UP
    if (message.content == "sad" or
       "imsad" in sanitise(message.content, (" ", "-", "\'", "‘", "’"))):
        await cheer_up(message)
        return

    # SHOW A RANDOM PICTURE FROM PIXABAY
    if unsanitised_message_content[:21].lower() == ("show me a picture of "):
        await show_pic(message, unsanitised_message_content[21:])
        return

    # TRIVIA GAME
    if Trivia_Game["Ongoing"]:
        await trivia_game(message)
    if message.content == "trivia":
        await trivia_game_start(message)

    # GUESSING GAME
    if Guessing_Game["Ongoing"]:
        await guessing_game(message)
    if message.content == "guess":
        await guessing_game_start(message)

    # GUESS4 GAME
    if Guess4["Ongoing"]:
        await guess_four_check(message)
    if message.content == "guess4" or message.content == "guessfour":
        await guess_four(message)

    # PLAY MUSIC
    if message.content[:4] == "play":
        if await voice_check_n_warn(message):
            search_term = unsanitised_message_content[4:].strip()
            await music_play(message, search_term)
    # PAUSE MUSIC
    if message.content == "pause":
        if await voice_check_n_warn(message):
            await music_pause(message)
    # SKIP TRACK
    if message.content == "skip":
        if await voice_check_n_warn(message):
            await music_skip(message)
    # RESUME MUSIC
    if message.content in ["resume", "continue", "unpause"]:
        if await voice_check_n_warn(message):
            await music_resume(message)
    # STOP MUSIC PLAYER
    if message.content == "stop":
        if await voice_check_n_warn(message):
            await music_stop(message)
    # CHECK QUEUE
    if message.content == "queue":
        if await voice_check_n_warn(message):
            await music_queue(message)
    # LOOP SONG
    if message.content == "loop":
        if await voice_check_n_warn(message):
            await music_loop(message)
    # GET TRACK (DOWNLOAD)
    if message.content == "gimmethissong":
        if await voice_check_n_warn(message):
            client.loop.create_task(music_download(message))

async def voice_check_n_warn(message):
    """Returns True only if message sender is in voice channel
    Warns via message if not.

    This is mainly used to make sure sender is in a voice
    channel for music commands"""
    if message.author.voice is None:
        await message.channel.send("You're not in a voice channel bruh.")
        return False
    return True


def lock(func):
    """Lock a function (decorator). on_message will ignore while 'locked'."""
    async def inner(*args):
        global locked
        locked = True
        await func(*args)
        locked = False
    return inner


@lock
async def log_out(message):
    await client.change_presence(status=discord.Status.offline)
    await message.channel.send("Ok.. byee ;-;")
    await client.close()
    return


@lock
async def insult(message):
    await message.channel.send(textgen.generate_insult())
    return


@lock
async def joke(message):
    joke = textgen.generate_joke()
    await message.channel.send(joke[0])
    time.sleep(3)
    await message.channel.send(joke[1])
    return


@lock
async def inspire(message):
    quote = textgen.generate_quote()
    await message.channel.send(f"'{quote[0]}' -{quote[1]}")


@lock
async def show_scores(message):
    await message.channel.send(score_handler.all_scores())
    return


@lock
async def compliment(message):
    channel = message.channel
    compliment = textgen.generate_compliment()

    await channel.send(compliment)

    def checkfunc(m):
        if m.channel != channel or m.author != message.author:
            # If the guy who said thanks isnt the guy who asked for compliment
            return False
        pattern = "thanks|thankyou|ty|thx|thnks"
        if re.match(pattern, sanitise(m.content)):
            return True
    try:
        await client.wait_for("message", timeout=5, check=checkfunc)
        await channel.send("You're welcome! _nerd_")
    except asyncio.TimeoutError:
        # If the reply wasnt received before the timeout
        await channel.send("No thanks ah? **Rude.**")
    return


@lock
async def show_comic(message):
    channel = message.channel
    comic = comicgen.Comic()
    img = comic.get_image()
    # Send the comic title
    await channel.send(comic.get_title())
    with io.BytesIO() as binary:
        img.save(binary, "PNG")
        binary.seek(0)
        await message.channel.send(
            file=discord.File(fp=binary, filename="image.png"))

    await channel.send(comic.get_alt_text())


@lock
async def cheer_up(message):
    await message.channel.send(f"Don't be sadd <@{message.author.id}>")
    gif_bin = tenor_getter.get_gif("cheer up", limit=50)
    await message.channel.send(f"<@{message.author.id}>", file=discord.File(
        io.BytesIO(gif_bin), filename='cheerup.gif'))
    return


@lock
async def trivia_game(message):
    # If the message was not sent in the trivia game channel, continue
    channel = message.channel
    if channel != Trivia_Game["Channel"]:
        return

    answer = message.content

    # Check if answer is from 1-4
    if re.match("[1-4]", answer) is None or len(answer) > 1:
        await channel.send("Send only the number, ya nerd. (1,2,3,4)")
        return

    correct_ans = Trivia_Game["Answers"][Trivia_Game["Answer_Index"]]
    print(answer, Trivia_Game["Answer_Index"])
    if int(answer) - 1 != Trivia_Game["Answer_Index"]:
        await channel.send(f"Wrong! The answer was "
                           f"**{Trivia_Game['Answer_Index']+1}. {correct_ans}**")
    else:
        await channel.send(f"Correct! The answer is "
                           f"**{Trivia_Game['Answer_Index']+1}. {correct_ans}**")

        # Add score
        score_handler.add_score("Trivia_Game", message.author.name)

    Trivia_Game["Ongoing"] = False


@lock
async def trivia_game_start(message):
    check = check_ongoing_game()
    if check:
        await message.channel.send(check + " ongoing")
        return

    channel = message.channel
    Trivia_Game["Channel"] = channel
    await channel.send("Starting Game")

    # Get the trivia qns
    results = trivia.generateQuestion()
    question = html.unescape(results["question"])

    # Shuffle correct ans into incorrect ones
    answers = results["incorrect_answers"]
    answers.append(results["correct_answer"])
    answers = [html.unescape(x) for x in answers]

    random.shuffle(answers)
    print(answers, results["correct_answer"])

    await channel.send(f"Q:\t{question}\n"
                       f"1.\t{answers[0]}\n"
                       f"2.\t{answers[1]}\n"
                       f"3.\t{answers[2]}\n"
                       f"4.\t{answers[3]}")

    Trivia_Game["Ongoing"] = True
    Trivia_Game["Answers"] = answers
    Trivia_Game["Answer_Index"] = answers.index(results["correct_answer"])
    return


@lock
async def guessing_game(message):
    # If the message was not sent in the guessing game channel, continue
    channel = message.channel
    if channel != Guessing_Game["Channel"]:
        return
    answer = sanitise(message.content)
    if answer != Guessing_Game["Answer"]:
        Guessing_Game["Chances"] = Guessing_Game["Chances"] - 1
        await channel.send(f"Wrong! {Guessing_Game['Chances']} chance(s) left")
        if Guessing_Game["Chances"] <= 0:
            await channel.send("The answer was " + Guessing_Game["Answer"])

            Guessing_Game["Ongoing"] = False
    else:
        await message.add_reaction("✅")
        await channel.send(f"Correct, <@{message.author.id}>!"
                           f"The answer is {Guessing_Game['Answer']}")

        # Add score
        score_handler.add_score("Guessing_Game", message.author.name)
        Guessing_Game["Ongoing"] = False


@lock
async def guessing_game_start(message):
    check = check_ongoing_game()
    if check:
        await message.channel.send(check + " ongoing")
        return

    channel = message.channel
    Guessing_Game["Channel"] = channel
    await channel.send("Starting Game")

    # Do stuff with img and answer
    img, name = gtd.getImage()
    img = img.image
    Guessing_Game["Answer"] = sanitise(name)

    with io.BytesIO() as binary:
        img.save(binary, "PNG")
        binary.seek(0)
        await channel.send(file=discord.File(fp=binary, filename="image.png"))

    await channel.send("What is this image? ({} {} letters)".format(
        re.sub("[a-z]", "-", name.strip()), str(len(Guessing_Game["Answer"]))))

    Guessing_Game["Ongoing"] = True
    Guessing_Game["Chances"] = 5
    return


@lock
async def show_pic(message, query="apple"):

    # pixabay_getter returns a list of 1 image if 'qty' not specified
    ret = pixabay_getter.get_images(query)
    if ret:
        # io.BytesIO(bytes) opens a binary stream in memory, similar to
        # open('file.jpg', 'rb') which opens a binary stream on the hard disk.
        await message.channel.send(file=discord.File(io.BytesIO(ret[0]),
                                   filename="image.png"))
    else:
        await message.channel.send(f"Oopsie daisy, couldn't"
                                   f"find a nice image of {query}")


async def guess_four(message):
    check = check_ongoing_game()
    if check:
        await message.channel.send(check + " ongoing")
        return

    Guess4.update({"Ongoing":  True, "Try": 0})
    await message.channel.send("Starting Game...")
    answer, category, pics = guess4.get_question()
    Guess4["Answer"] = answer
    await message.channel.send("What's the link?")

    for pic in pics:
        if Guess4["Ongoing"]:
            await message.channel.send(file=discord.File(
                io.BytesIO(pic), filename="image.png"))
            Guess4["Try"] += 1
            await asyncio.sleep(10)
    if Guess4["Ongoing"]:
        await message.channel.send(
            f"Here's the category you noobie: {category}")
        Guess4["Try"] += 1
        await asyncio.sleep(20)
    if Guess4["Ongoing"]:
        await message.channel.send(
            f"Please Alt-F4 and uninstall, the answer is {answer}")
        Guess4["Ongoing"] = False
    return


@lock
async def guess_four_check(message):
    if sanitise(message.content) == sanitise(Guess4["Answer"]):
        await message.add_reaction("✅")
        if Guess4["Try"] == 1:
            await message.channel.send(
                f"WOWZERS <@{message.author.id}>! YOU SMARTIEPANTS!")
        elif Guess4["Try"] == 2 or Guess4["Try"] == 3:
            await message.channel.send(
                f"YOU GOT IT, <@{message.author.id}>! "
                f"NOT BAD JUST {Guess4['Try']} PICTURES.")
        elif Guess4["Try"] == 4:
            await message.channel.send(
                f"THAT\'S IT, <@{message.author.id}>! 4 pictures tho...")
        else:
            await message.channel.send(
                f"Well <@{message.author.id}> got it right, "
                "but they shouldn\'t even be proud.")
        score_handler.add_score("Guess4", message.author.name)
        Guess4["Ongoing"] = False
    return


@lock
async def music_play(message, search_term):
    if search_term == "":   # A bare "play" will resume the song if paused
        await music_resume(message)
        return

    voice_channel = message.author.voice.channel
    # Attempt to get the voice_client in author's voice channel if it exists
    voice_client = discord.utils.get(
        client.voice_clients, channel=voice_channel)
    if voice_client is None:
        # Connects the author's voice channel and creates a
        # VoiceClient to establish your connection to the voice server.
        voice_client = await voice_channel.connect()

    # Check user entered a URL or search term,
    # and get an audioSource accordingly
    yt_url = search_term
    if (search_term.startswith("https://www.youtube.com/watch?v=") or
       search_term.startswith("https://youtu.be/")):
        await message.channel.send("Fetching...")
    else:
        await message.channel.send(f"Searching for: {search_term}")
        yt_url = musiclib.youtube.search(search_term)
        await message.channel.send(f"Fetching: {yt_url}")

    ytdl_info = musiclib.youtube.url_to_ytdl(yt_url)
    track = musiclib.youtube.ytdl_to_track(ytdl_info)
    if track is None:   # Error code for wrong URL
        await message.channel.send("No such thing you dumb dumb!")
        return

    ID = voice_client.channel.id
    musiclib.qmgr.enqueue(ID, track)

    if voice_client.is_playing() or voice_client.is_paused():
        await message.channel.send("Added to queue.")
        print(f"Added to queue: {yt_url}; Voice Client: {voice_client}; "
              f"Voice Channel ID: <{voice_channel.id}>\n")
    else:   # Start playing from a non-playing state
        voice_client.play(track.source,
                          after=lambda error: music_after(error, voice_client))
        print(f"Playing: {yt_url}; Voice Client: {voice_client}; "
              f"Guild: {message.guild}; Voice Channel: <{voice_channel}>\n")


@lock
async def music_pause(message):
    voice_client = discord.utils.get(client.voice_clients,
                                     channel=message.author.voice.channel)
    # voice_client is None if no voice client
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        await message.channel.send("Pausing...")
    else:
        await message.channel.send(random.choice(error_replies))


@lock
async def music_resume(message):
    voice_client = discord.utils.get(client.voice_clients,
                                     channel=message.author.voice.channel)
    # voice_client is None if no voice client
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        await message.channel.send("Resuming...")
    else:
        await message.channel.send(random.choice(error_replies))


@lock
async def music_skip(message):
    voice_client = discord.utils.get(client.voice_clients,
                                     channel=message.author.voice.channel)
    if voice_client is not None and voice_client.is_playing():
        # Check if loop is on
        queueID = voice_client.channel.id
        pl = musiclib.qmgr.get_queue(queueID)
        pl.stop_looping()
        voice_client.stop()
        await message.channel.send("Skipped")
    else:
        await message.channel.send(random.choice(error_replies))


@lock
async def music_stop(message):
    # Stops the music player entirely (clears queue)
    voice_client = discord.utils.get(client.voice_clients,
                                     channel=message.author.voice.channel)
    if voice_client is not None and voice_client.is_playing():
        # Clear and delete this channel's music queue
        musiclib.qmgr.remove_queue(voice_client.channel.id)
        voice_client.stop()
        await message.channel.send("Stopped")
    else:
        await message.channel.send(random.choice(error_replies))


def music_play_next(voice_client):
    queueID = voice_client.channel.id

    # Check if loop is on
    queue = musiclib.qmgr.get_queue(queueID)

    if queue and queue.looping:
        source = musiclib.youtube.streamURL_to_DCsource(
            queue.get_tracks()[0].streamURL)
        voice_client.play(source,
                          after=lambda error: music_after(error, voice_client))
        return

    # When not looping, we dequeue the current track and move on
    # If queue is now empty, dequeue() will destroy the
    # queue for us and return None
    musiclib.qmgr.dequeue(queueID)

    if musiclib.qmgr.get_queue(queueID):
        # If queue still exist AKA if there are still tracks left to play
        track = queue.get_tracks()[0]
        voice_client.play(track.source,
                          after=lambda error: music_after(error, voice_client))
        print(f"Playing Next In Queue: {track.url}\n")
    else:
        voice_client.stop()
        print("Music Queue Ended\n")


def music_after(error, voice_client):
    # Here we sorta just keep playing the next thing in queue until empty
    music_play_next(voice_client)


@lock
async def music_queue(message):
    voice_client = discord.utils.get(client.voice_clients,
                                     channel=message.author.voice.channel)
    if voice_client is None:
        await message.channel.send("I'm not playing shit m8!")
        return

    queueID = voice_client.channel.id

    await message.channel.send(embed=musiclib.qmgr.get_embed(queueID))


@lock
async def music_loop(message):
    voice_client = discord.utils.get(client.voice_clients,
                                     channel=message.author.voice.channel)
    if voice_client is None:
        await message.channel.send("I'm not even in voice m8!")
        return

    # Get queue (Playlist object); Return -1: Queue does not exist
    queueID = voice_client.channel.id
    queue = musiclib.qmgr.get_queue(queueID)
    if queue == -1:
        await message.channel.send("I'm not playing shit m8!")
        print(f"Error: Queue <{queueID}> doesn't exist")
        return

    # Toggle looping
    queue.toggle_looping()

    if queue.looping:
        await message.channel.send("Looping :)")
    else:
        await message.channel.send("No Looping :(")


async def music_download(message):
    # TODO: NOT THE SAFEST WAY TO GO ABOUT DOING THIS,
    # CURRENTLY NO LIMIT ON DOWNLOAD SIZE, AND DISCORD.PY
    # DIRECTLY ACCESSES OUR FILES BY PATH TO SEND THE FILE, NO GOOD!!

    voice_client = discord.utils.get(client.voice_clients,
                                     channel=message.author.voice.channel)
    if voice_client is None:
        await message.channel.send("I'm not playing shit m8!")
        return

    # Get playlist; Return -1: Queue does not exist
    queueID = voice_client.channel.id
    queue = musiclib.qmgr.get_queue(queueID)
    if queue == -1:
        await message.channel.send("I'm not playing shit m8!")
        print(f"Error: Queue <{queueID}> doesn't exist")
        return

    track = queue.get_tracks()[0]
    download_embed = discord.Embed(
        title="Sure Thing! Try the following:",
        description=f"[{track.title}]"
                    "(https://www.yt-download.org/api/button/mp3/"
                    f"{track.yt_id})")
    await message.channel.send(embed=download_embed)


def check_ongoing_game():
    """Return True if a game is currently playing, and a str of which game."""
    if Guessing_Game["Ongoing"]:
        return "Guessing Game"
    if Trivia_Game["Ongoing"]:
        return "Trivia Game"
    if Guess4["Ongoing"]:
        return "Guess Four"
    return None


def sanitise(word, chars_to_remove=[" ", "-"], case_sensitive=False):
    """Clean a word, default to removing " " & "-", and lowercasing all."""
    if not case_sensitive:
        word = word.lower()
    for char in chars_to_remove:
        word = word.replace(char, "")
    return word


def print_debug_info(message):
    print("DEBUG INFO\n--------------")
    print("Testing From")
    print(f"  Guild: {message.guild} <{message.guild.id}>")
    print(f"  Channel: {message.channel}<{message.channel.id}>")
    print(f"  Author: {message.author}")
    print(f"    ID: <{message.author.id}>")
    print(f"    Name: {message.author.name}")
    print(f"    In Voice Channel: {message.author.voice.channel} "
          f"<{message.author.voice.channel.id}>")

    print("Voice Clients")
    if client.voice_clients == []:
        print("  None")
    for voice_client in client.voice_clients:
        print(f"  {voice_client}")
        print(f"    Guild: {voice_client.guild} <{voice_client.guild.id}>")
        print(f"    Channel: {voice_client.channel} "
              f"<{voice_client.channel.id}>")
        print(f"    Flags: Connected = {voice_client.is_connected()}; "
              f"Playing = {voice_client.is_playing()}; "
              f"Paused = {voice_client.is_paused()}")
        print(f"    Queue: {musiclib.qmgr.get_queue(voice_client.channel.id)}")
    print()


load_dotenv()
client.run(os.getenv("TOKEN"))
