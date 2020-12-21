import quickdraw
import random
import sys, os
import cv2

def getImage():
    #returns the img and the name in an array
    #Initialise the set of images
    qd = quickdraw.QuickDrawData(recognized = True)
    names = qd.drawing_names

    #get a random image name
    name = names[random.randint(0, len(names))]
    
    #gotta reroute the stdout to stop google's quickdraw api from spoiling the ans
    with open(os.devnull, "w") as devnull:
        org = sys.stdout
        sys.stdout = devnull

        #get the drawing
        img = qd.get_drawing(name)

        sys.stdout = org

    return [img, name]

def sanitise(word):
    #very securely removes whitespaces, hyphens, and makes everything lowercase
    word = word.replace(" ", "")
    word = word.replace("-", "")
    return word.lower()

    
def main():
    img, name = getImage()

    #make the name consistent
    name = sanitise(name)

    #show image
    img.image.show()
    
    chances = 5
    print("Answer: " + "-" * len(name), "(" +str(len(name))," letters" + ")")
    
    while chances > 0:
        #Ask for input
        guess = input("\nGuess the drawing: ")

        #make the guess consistent
        guess = guess.lower().strip()
        guess = sanitise(guess)
        
        if guess.lower() != name:
            chances -= 1
            print("Wrong!", chances, "Chance(s) left")
        else:
            print("Correct!")
            break
        
    print("The answer was", name)
    

        
if __name__ == "__main__":
    while True:
        main()


    
