import discord
import guess_the_drawing as gtd
import io, re, random, html
import text_generator as textgen
import trivia_game as trivia
import time, os
import score_handler
from dotenv import load_dotenv
import comic_generator as comicgen

client = discord.Client()

#global variables
Guessing_Game = {"Ongoing" : False, "Answer" : None, "Chances" : 5, "Channel" : None}
Trivia_Game = {"Ongoing" : False, "Answer_Index" : 0, "Answers" : [], "Channel" : None}
Conversation = {"Ongoing" : False, "Channel" : None}
locked = False


@client.event
async def on_ready():
    for guild in client.guilds:
        await guild.system_channel.send("Yuhhh dudes im here")

#for reference, https://discordpy.readthedocs.io/en/latest/migrating.html#sending-messages
@client.event
async def on_message(message):
    if message.author == client.user or locked:
        return

    #remove spaces and lowercase it to make it consistent with commands
    unsanitised_message = message
    message.content = gtd.sanitise(message.content)
    
    if message.content == "testing":
        channel = message.channel
        reply = 'what a nerd, ' + str(message.author.name)
        await channel.send(reply)

        return

    #INSULT
    if message.content == "insultme":
        await insult(message)
        
    #JOKE
    if message.content == "tellmeajoke":
        await joke(message)

    #INSPIRATIONAL QUOTE
    if message.content == "inspireme":
        await inspire(message)

    #PRINT SCORES
    if message.content == "showmescores":
        await show_scores(message)
    
    #COMPLIMENT
    if message.content == "complimentme" or message.content == "praiseme":
        await compliment(message)
    
    #PICKUP LINE
    if message.content == "pickmeup":
        await message.channel.send(textgen.generate_pickup_line())
        return

    #COMIC GENERATOR
    if message.content == "showmeacomic":
        await show_comic(message)
    
    
    #TRIVIA GAME 
    if Trivia_Game["Ongoing"]:
        await trivia_game(message)

    
    if message.content == "trivia":
        await trivia_game_start(message)


    #GUESSING GAME  
    if Guessing_Game["Ongoing"]:
        await guessing_game(message)

        
    if message.content == "guess":
        await guessing_game_start(message)
        
def lock(func):
    #stops another command from being run if a command is currently being executed
    async def inner(message):
        global locked
        locked = True
        await func(message)
        locked = False
    return inner

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
    await message.channel.send("'{}' -{}".format(quote[0], quote[1]))

@lock
async def show_scores(message):
    channel = message.channel
    filepath = os.path.join(os.getcwd(), "scores")
    score_files = os.listdir(filepath)

    await channel.send(score_handler.print_scores())
    return

@lock
async def compliment(message):
    channel = message.channel
    compliment = textgen.generate_compliment()

    await channel.send(compliment)

    def checkfunc(m):
        if m.channel != channel:
            return False
        pattern = "thanks|thankyou|ty|thx|thnks"
        if re.match(pattern, gtd.sanitise(m.content)):
            return True

    msg = await client.wait_for('message', timeout = 2, author = message.author ,check=checkfunc)
    await channel.send('Youre welcome! (nerd)')
    return

@lock
async def show_comic(message):
    channel = message.channel
    comic = comicgen.Comic()
    img = comic.get_image()
    #send the comic title
    await channel.send(comic.get_title())
    with io.BytesIO() as binary:
        img.save(binary, 'PNG')
        binary.seek(0)
        await message.channel.send(file=discord.File(fp=binary, filename="image.png"))

    await channel.send(comic.get_alt_text())

@lock
async def trivia_game(message):
    #If the message was not sent in the trivia game channel, continue
    channel = message.channel
    if channel != Trivia_Game["Channel"]:
        return

    answer = message.content

    #check if answer is from 1-4
    if re.match("[1-4]",answer) == None or len(answer) > 1:
        await channel.send("Send only the number, ya nerd. (1,2,3,4)")
        return
    
    correct_ans = Trivia_Game["Answers"][Trivia_Game["Answer_Index"]]
    print(answer, Trivia_Game["Answer_Index"])
    if int(answer) - 1 != Trivia_Game["Answer_Index"]:
        await channel.send("Wrong! The answer was {} ({})".format(Trivia_Game["Answer_Index"] + 1, correct_ans))
    else:
        await channel.send("Correct! The answer is {} ({})".format(Trivia_Game["Answer_Index"] + 1, correct_ans))

        #add score
        score_handler.add_score("Trivia_Game", message.author.name)
        

    Trivia_Game["Ongoing"] = False

@lock
async def trivia_game_start(message):
    check = checkOngoingGame()
    if check[0]:
        await message.channel.send(check[1] + " ongoing")
        return

    
    channel = message.channel
    Trivia_Game["Channel"] = channel
    await channel.send("Starting Game")

    #get the trivia qns
    results = trivia.generateQuestion()
    question = html.unescape(results['question'])
    
    #shuffle correct ans into incorrect ones
    answers = results['incorrect_answers']
    answers.append(results['correct_answer'])
    answers = [html.unescape(x) for x in answers]
    
    random.shuffle(answers)
    print(answers, results['correct_answer'])
    
    await channel.send("Q:\t" + question)
    await channel.send("1.\t{}\n2.\t{}\n3.\t{}\n4.\t{}".format(answers[0], answers[1], answers[2], answers[3]))

    Trivia_Game["Ongoing"] = True
    Trivia_Game["Answers"] = answers
    Trivia_Game["Answer_Index"] = answers.index(results['correct_answer'])
    return

@lock
async def guessing_game(message):
    #If the message was not sent in the guessing game channel, continue
    channel = message.channel
    if channel != Guessing_Game["Channel"]:
        return
    answer = gtd.sanitise(message.content)
    if answer != Guessing_Game["Answer"]:
        Guessing_Game["Chances"] = Guessing_Game["Chances"] - 1
        await channel.send("Wrong! " + str(Guessing_Game["Chances"]) + " Chance(s) left")
        if Guessing_Game["Chances"] <= 0:
            await channel.send("The answer was " + Guessing_Game["Answer"])
            Guessing_Game["Ongoing"] = False
    else:
        await channel.send("Correct! The answer is " + Guessing_Game["Answer"])
        #add score
        score_handler.add_score("Guessing_Game", message.author.name)
        Guessing_Game["Ongoing"] = False

@lock
async def guessing_game_start(message):
    check = checkOngoingGame()
    if check[0]:
        await message.channel.send(check[1] + " ongoing")
        return

    
    channel = message.channel
    Guessing_Game["Channel"] = channel
    await channel.send("Starting Game")

    #do stuff with img and answer
    img, name = gtd.getImage()
    img = img.image
    Guessing_Game["Answer"] = gtd.sanitise(name)
    
    with io.BytesIO() as binary:
        img.save(binary, 'PNG')
        binary.seek(0)
        await channel.send(file=discord.File(fp=binary, filename="image.png"))

    await channel.send("What is this image? ({} {} letters)".format(re.sub("[a-z]", "-", name.strip()), str(len(Guessing_Game["Answer"]))))

    Guessing_Game["Ongoing"] = True
    Guessing_Game["Chances"] = 5
    return



def checkOngoingGame():
    #returns True if a game is currently being played, and a string of which game.
    if Guessing_Game["Ongoing"]:
        return [True, "Guessing Game"]
    if Trivia_Game["Ongoing"]:
        return [True, "Trivia Game"]
    return [False, None]

load_dotenv()
client.run(os.getenv('TOKEN'))
