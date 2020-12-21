import os
import csv
from pathlib import Path

def add_score(gamename, player, score = 1):
    #Takes in gamename, player, amt of score to be added
    #will assume that the gamename's scores are stored as [gamename].csv

    filepath = os.path.join(os.getcwd(), "scores")
    filepath = os.path.join(filepath, gamename + ".csv")
    
    file=csv.reader(open(filepath, newline=''))
    lines = list(file)

    #find if user exists in scoreboard
    player_index = [lines.index(x) for x in lines if x[0] == player]
    
    #if empty list, player does not exist. Create new record
    if player_index == []:
        with open(filepath, 'a') as file:
            file.write( "{},{}\n".format(player, score))

        return

    #if player exists, update the value
    player_index = player_index[0]
    lines[player_index][1] = int(lines[player_index][1]) + score
    
    #save it back
    file = csv.writer(open(filepath, 'w', newline=''))
    file.writerows(lines)
    return

def print_scores():
    #prints all the files in the scores folder
    filepath = os.path.join(os.getcwd(), "scores")
    score_files = os.listdir(filepath)

    output = ""
    for file in score_files:
        output += "\n" + print_score(file) + "\n"

    return output
    
def print_score(filename):
    #returns one long string with '\n's
    #takes in ONLY the filename ("testgame", not "testgame.csv"), not the full filepath.

    filepath = os.path.join(os.getcwd(), "scores")
    filepath = os.path.join(filepath, filename)

    #stem removes the file extension
    output = "{}\n{}".format('Scoreboard for ' + Path(filename).stem, '-' * 40)

    r = csv.reader(open(filepath, newline=''))
    lines = list(r)

    lines.sort(key=lambda x: x[1], reverse=True)

    for line in lines:
        output += '\n{}\t\t\t:\t\t\t{}'.format(line[0], line[1])

    output += '\n' + '-' * 40
    return output

