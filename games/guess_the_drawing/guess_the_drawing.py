import quickdraw
import random
import sys
import os


def getImage():
    """Return the img and the name in an array."""
    # Initialise the set of images
    qd = quickdraw.QuickDrawData(recognized=True)
    names = qd.drawing_names

    # Get a random image name
    name = names[random.randint(0, len(names))]

    # Gotta reroute the stdout to stop google's quickdraw api from spoiling the ans
    with open(os.devnull, 'w') as devnull:
        org = sys.stdout
        sys.stdout = devnull

        # Get the drawing
        img = qd.get_drawing(name)

        sys.stdout = org

    return [img, name]


def sanitise(word):
    """Remove whitespaces, hyphens, and makes everything lowercase."""
    word = word.replace(" ", "")
    word = word.replace("-", "")
    return word.lower()


def main():
    img, name = getImage()

    # Make the name consistent
    name = sanitise(name)

    # Show image
    img.image.show()

    chances = 5
    print(f"Answer: {'-' * len(name)} ({str(len(name))} letter)")

    while chances > 0:
        # Ask for input
        guess = input("\nGuess the drawing: ")

        # Make the guess consistent
        guess = guess.lower().strip()
        guess = sanitise(guess)

        if guess.lower() != name:
            chances -= 1
            print(f"Wrong! {chances} chance(s) left")
        else:
            print("Correct!")
            break

    print(f"The answer was {name}")


if __name__ == '__main__':
    while True:
        main()
