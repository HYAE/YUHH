# YUHH

The one and only repository for the YUHH Discord Bot.
  - Great bot!
  - Full of useless features!
  - Full of fun games!
  - Made by a bunch of so very experienced programmers!
  - AWESOME

## Features
### - Guess the drawing
**Invoke with: guess**\
Uses Google QuickDraw drawings drawn by other humans that Google's QuickDraw AI was able to guess.

### - Trivia
**Invoke with: trivia**\
A quick multiple-choice trivia games to test your knowledge of random things with your friends.\
Currently only support random topics, categories and more features will be added soon!

### - Insult
**Invoke with: insult me**\
You know that feeling when you really want someone to just insult you in your face? Yeap, we've got you covered!\
Insults are not that creative yet, but too bad that's all you get. If you want better insults feel free to DM me!

### - Joke
**Invoke with: tell me a joke**\
That's you!

### - Inspire
**Invoke with: inspire me**\
You get stuff said by people way smarter than you.

### - Testing
**Invoke with: testing**\
Try it, nerd.

### - Scoring
**Invoke with: show me scores**\
Displays the scoreboard for all the games, which includes
- Guess the drawing
- Trivia
- Guess 4

Currently doesn't have a reset feature and just cumulates, but hey, that's nice too.

### - Compliment
**Invoke with: compliment me / praise me**\
You are beautiful just the way you are. But if you need even more of an ego boost, you can always get YUHH to compliment you.

### - Pick up lines
**Invoke with: pick me up**\
For those lonely singles our there! It's ok, YUHH loves you unconditionally!\
For those who just can't seem to pick anyone up, please learn from YUHH.\
YUHH is rated 10 out of 10 best lover on very www.totallylegitdatingsite.com!

### - Comic
**Invoke with: show me a comic**\
Ok you're not alone, I think the comics are pretty lame too. (Thank @Junjayel for his choice of API)

### - Picture
**Invoke with: "show me a picture of " (*Invokation needs to match all letters and spaces*)**\
YUHH will search through high quality nice photographs taken by photographers better than you.\
- Images are copyright-free, from Pixabay. How awesome!\
- Just don't try to be funny and ask for obscure images thanks.

### - Guess 4
**Invoke with: guess 4**\
A similar game to Guess The Drawing\
- 4 pictures are shown on set intervals, followed by a hint\
- First to guess the word linking all 4 pictures together wins!

## New Features!
### - Cheer Up
**Invoke with: i'm sad**\
Cmon don't be sadd :D

## Dependencies
### Endpoint APIs
| Feature | API |
| ------ | ------ |
| Trivia | [OpenTDB](https://opentdb.com/) |
| Insult | [MattBas](https://insult.mattbas.org/api/) |
| Joke | [us-central1-dadsofunny](https://us-central1-dadsofunny.cloudfunctions.net/DadJokes/random/jokes) |
| Inspire | [Type.fit](https://type.fit/api/quotes) |
| Compliment | [Complimentr](https://complimentr.com/) |
| Pick Me Up | [BPLaaS](http://bplaas.herokuapp.com/) |
| Pictures | [PixaBay](https://pixabay.com/api/docs/) |
| Gifs | [Tenor](https://tenor.com/gifapi/documentation) |

### External Python Libraries
| Feature | Library |
| ------ | ------ |
| Guess The Drawing | [quickdraw 0.1.0](https://pypi.org/project/quickdraw/) |

## About us
> " 'Go for it now. The future is promised to no one.' -Wayne Dyer " - Qiao Hui

### Development
Want to contribute? Great!\
GIVE US MONEY THANKS!

### Todos
 - Be more awesome

### Known Bugs
 - When Guess 4 is invoked right after a completed Guess 4 game, the game glitches.
   - This is due to the function only checking after 1 seconds of asyncio.sleep . Will fix this soon.

## License
We are chill people, apart from the licenses of all the depedencies we use, you can freely use our code in any way you want :D\
Remember to get your own API keys for things that requires it:
- Pixabay

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

Examples:
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
