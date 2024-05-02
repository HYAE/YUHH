# YUHH

The one and only repository for the YUHH Discord Bot.
  - Great bot!
  - Full of useless features!
  - Full of fun games!
  - Plays music!!
  - Made by a bunch of so very experienced programmers!
  - AWESOME

## Features
### - Music Player
Works generally well but lacks a few more polishing features.
#### Play Youtube Audio
**Invoke with: play [Youtube Title/URL]**  
**Sibling cmds: pause, resume**
- Can only play Youtube audio (might add more platforms in the future)
- Tracks will be added to queue if one is currently playing

#### Queue System
**Show Queue**  
**Invoke with: queue**
- Shows the currently playing track, and upcoming track
- Looping tracks coming soon!!

**Skip Current Track**  
**Invoke with: skip**
- Currently only skips the current track, will add an option to skip specific tracks (remove from queue) in the near future!

### - Guess the drawing
**Invoke with: guess**  
Uses Google QuickDraw drawings drawn by other humans that Google's QuickDraw AI was able to guess.

### - Trivia
**Invoke with: trivia**  
A quick multiple-choice trivia games to test your knowledge of random things with your friends.
Currently only support random topics, categories and more features will be added soon!

### - Insult
**Invoke with: insult me**  
You know that feeling when you really want someone to just insult you in your face? Yeap, we've got you covered!\
Insults are not that creative yet, but too bad that's all you get. If you want better insults feel free to DM me!

### - Joke
**Invoke with: tell me a joke**  
That's you!

### - Inspire
**Invoke with: inspire me**  
You get stuff said by people way smarter than you.

### - Testing
**Invoke with: testing**  
Try it, nerd.

### - Scoring
**Invoke with: show me scores**  
Displays the scoreboard for all the games, which includes
- Guess the drawing
- Trivia
- Guess 4

Currently doesn't have a reset feature and just cumulates, but hey, that's nice too.

### - Compliment
**Invoke with: compliment me / praise me**  
You are beautiful just the way you are. But if you need even more of an ego boost, you can always get YUHH to compliment you.

### - Pick up lines
**Invoke with: pick me up**  
For those lonely singles our there! It's ok, YUHH loves you unconditionally!\
For those who just can't seem to pick anyone up, please learn from YUHH.\
YUHH is rated 10 out of 10 best lover on very www.totallylegitdatingsite.com!

### - Comic
**Invoke with: show me a comic**  
Ok you're not alone, I think the comics are pretty lame too. (Thank @Junjayel for his choice of API)

### - Picture
**Invoke with: "show me a picture of " (*Invocation needs to match all letters and spaces*)**  
YUHH will search through high quality nice photographs taken by photographers better than you.
- Images are copyright-free, from Pixabay. How awesome!
- Just don't try to be funny and ask for obscure images thanks.

### - Guess 4
**Invoke with: guess 4**  
A similar game to Guess The Drawing
- 4 pictures are shown on set intervals, followed by a hint\
- First to guess the word linking all 4 pictures together wins!

### - Cheer Up
**Invoke with: i'm sad**  
Cmon don't be sadd :D

### Mini Invocations
**Invoke with: are you there?**  
Just a quick way to check if YUHH is there for you :>

### Backend
Invoke `testing` to view debugging info, mostly printed in the backend terminal.

## Updates
- Replaced Outdated APIs (Jokes & Pickup Lines)
- Fixed Music Player

## Dependencies
### Endpoint APIs
| Feature | API |
| ------ | ------ |
| Trivia | [OpenTDB](https://opentdb.com/) |
| Insult | [MattBas](https://insult.mattbas.org/api/) |
| Joke | [JokeAPI](https://v2.jokeapi.dev/) |
| Inspire | [Type.fit](https://type.fit/api/quotes) |
| Compliment | [Complimentr](https://complimentr.com/) |
| Pick Me Up | [VinuXD](https://vinuxd.vercel.app/#pickup-line-api) |
| Pictures | [PixaBay](https://pixabay.com/api/docs/) |
| Gifs | [Tenor](https://tenor.com/gifapi/documentation) |

### External Python Libraries
| Feature | Library |
| ------ | ------ |
| Hide Bot Key | [python-dotenv](https://pypi.org/project/python-dotenv/) |
| Guess The Drawing | [quickdraw 0.1.0](https://pypi.org/project/quickdraw/) |
| Youtube Support | [youtube-dl](https://pypi.org/project/youtube_dl/) |
| FFmpeg for Discord.py | [FFmpeg](https://www.ffmpeg.org/) |

### Env
There should be a `.env` file in the root directory to store API tokens used, the format is
```txt
TOKEN={Discord Bot Token}
PIXABAY_KEY={Pixabay Key}
```

## About us
> " 'Go for it now. The future is promised to no one.' -Wayne Dyer " - Qiao Hui

### Development
Want to contribute? Great!  
GIVE US MONEY, THANKS!  
Jk there's no donation link here.

### Todos
 - Feature: Remove specific tracks in Music Player
 - Feature: [WIP] Get a direct download link for music currently playing

### Known Bugs
 - When Guess 4 is invoked right after a completed Guess 4 game, the game glitches.
    - This is due to the function only checking after 1 seconds of `asyncio.sleep` . Will fix this soon..
 - Commands get ignored if something else is going on
    - This is due to a lock system we have, we should change it to a queue system to that commands will run after the current process is done
- Guess4 crashes if there are not enough images (IMPORTANT!! WILL FIX SOON!)

## License
We are chill people, apart from the licenses of all the dependencies we use, you can freely use our code in any way you want :D  
Remember to get your own API keys for things that requires it:
- Discord
- Pixabay
