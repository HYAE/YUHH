import discord
import guess_the_drawing as gtd
import io, re, random, html
import text_generator as textgen
import trivia_game as trivia
import time, os
import score_handler
from dotenv import load_dotenv

client = discord.Client()

#global variables TODO: CHANGE LISTS TO DICTS
Guessing_Game = {"Ongoing" : False, "Answer" : None, "Chances" : 5, "Channel" : None}
Trivia_Game = {"Ongoing" : False, "Answer_Index" : 0, "Answers" : [], "Channel" : None}
Conversation = {"Ongoing" : False, "Channel" : None}    # Currently useless


@client.event
async def on_ready():
    for guild in client.guilds:
        await guild.system_channel.send('Yuhhh dudes im here')

#for reference, https://discordpy.readthedocs.io/en/latest/migrating.html#sending-messages
@client.event
async def on_message(message):

    #remove spaces and lowercase it to make it consistent with commands
    unsanitised_message = message
    message.content = gtd.sanitise(message.content)
    if message.author == client.user:
        return

    if message.content == 'ping':
        await message.channel.send(f'pong! {round(client.latency * 1000)} ms')
        return

    if message.content == 'testing':
        await message.channel.send(f'What a nerd, {message.author.name}')
        return

    if message.content == 'gettheyuhhouttahere':
        await client.change_presence(status=discord.Status.offline)
        await message.channel.send('Ok.. byee ;-;')
        await client.close()
        return

    #INSULT
    if message.content == 'insultme':
        await message.channel.send(textgen.generate_insult())
        return

    #JOKE
    if message.content == 'tellmeajoke':
        joke = textgen.generate_joke()
        await message.channel.send(joke[0])
        time.sleep(3)
        await message.channel.send(joke[1])
        return

    #INSPIRATIONAL QUOTE
    if message.content == 'inspireme':
        quote = textgen.generate_quote()
        await message.channel.send("'{}' -{}".format(quote[0], quote[1]))

    #PRINT SCORES
    if message.content == 'showmescores':
        filepath = os.path.join(os.getcwd(), 'scores')
        score_files = os.listdir(filepath)

        await message.channel.send(score_handler.print_scores())
        return

    #COMPLIMENT
    if message.content == 'complimentme' or message.content == 'praiseme':

        compliment = textgen.generate_compliment()
        await message.channel.send(compliment)

        def checkfunc(m):
            if m.channel != message.channel:
                return False
            pattern = 'thanks|thankyou|ty|thx|thnks'
            if re.match(pattern, sanitise(m.content)):
                return True

        msg = await client.wait_for_message(timeout = 5, author = message.author ,check=checkfunc)
        await channel.send('Youre welcome! (nerd)')
        return

    #PICKUP LINE
    if message.content == 'pickmeup':
        await message.channel.send(textgen.generate_pickup_line())
        return


    #CONVERSATION
    if Conversation["Ongoing"]:
        channel = message.channel
        if channel != Conversation["Channel"]:
            return





    if message.content == "talkwithme":
        Conversation["Ongoing"] = True


    #TRIVIA GAME
    if Trivia_Game["Ongoing"]:
        #If the message was not sent in the trivia game channel, continue
        channel = message.channel
        if channel != Trivia_Game["Channel"]:
            return

        answer = message.content

        #check if answer is from 1-4
        if re.match('[1-4]',answer) == None or len(answer) > 1:
            await message.channel.send('Send only the number, ya nerd. (1,2,3,4)')
            return

        correct_ans = Trivia_Game["Answers"][Trivia_Game["Answer_Index"]]
        print(answer, Trivia_Game["Answer_Index"])
        if int(answer) - 1 != Trivia_Game["Answer_Index"]:
            await channel.send("Wrong! The answer was {} ({})".format(Trivia_Game["Answer_Index"] + 1, correct_ans))
        else:
            await channel.send("Correct! The answer is {} ({})".format(Trivia_Game["Answer_Index"] + 1, correct_ans))

            #add score
            score_handler.add_score('Trivia_Game', message.author.name)

        Trivia_Game["Ongoing"] = False


    if message.content == 'trivia':
        check = checkOngoingGame()
        if check:
            await message.channel.send(f'{check} Ongoing')
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


    #GUESSING GAME
    if Guessing_Game["Ongoing"]:
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


    if message.content == 'guess':

        check = checkOngoingGame()
        if check:
            await message.channel.send(f'{check} Ongoing')
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
            await channel.send(file=discord.File(fp=binary, filename='image.png'))

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
