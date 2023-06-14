import os
import csv
from pathlib import Path

def add_score(gamename, player, score = 1):
    # Takes in gamename, player, amt of score to be added
    # Will assume that the gamename's scores are stored as [gamename].csv

    filepath = os.path.join(os.getcwd(), 'scores')
    filepath = os.path.join(filepath, gamename + '.csv')

    file = csv.reader(open(filepath, newline=''))
    lines = list(file)

    # Find if user exists in scoreboard
    player_index = [lines.index(x) for x in lines if x[0] == player]

    # If empty list, player does not exist. Create new record
    if player_index == []:
        with open(filepath, 'a') as file:
            file.write(f"{player},{score}\n")
        return

    # If player exists, update the value
    player_index = player_index[0]
    lines[player_index][1] = int(lines[player_index][1]) + score

    # Save it back
    file = csv.writer(open(filepath, 'w', newline=''))
    file.writerows(lines)
    return


def formatted_scorefile(filename):
    """Return one long string with newlines.

    takes in ONLY the filename ('testgame', not 'testgame.csv'), not the full filepath.
    """
    filepath = os.path.join(os.getcwd(), 'scores')
    filepath = os.path.join(filepath, filename)

    gamename = Path(filename).stem # Stem removes the file extension
    output = f"Scoreboard for {gamename}\n"
    output += "-"*40 + "\n"

    r = csv.reader(open(filepath, newline=""))
    lines = list(r)
    lines.sort(key=lambda x: int(x[1]), reverse=True)

    for line in lines:
        output += f"{line[0]}: {line[1]}\n"
    output += "-"*40 + "\n"
    return output


def all_scores():
    """Print all the files in the scores folder."""
    filepath = os.path.join(os.getcwd(), 'scores')
    score_files = os.listdir(filepath)

    output = ""
    for file in score_files:
        output += formatted_scorefile(file)
        output += "\n"

    return output
