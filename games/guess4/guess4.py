import csv
import random
import pixabay_getter   # Since YUHH imported this module, YUHH's path is also shared with this 'guess4' module, hence we can just drectly import pixabay_getter


def get_question(category=None):
    with open('games/guess4/guess4_wordbank.csv', 'r') as f:
        word_lists = list(csv.reader(f))

    if category:
        for word_list in word_lists:
            if word_list[0] == category:
                chosen_list = word_list
                break
        raise ValueError(f'{category} is not a category in word_list')
    else:
        chosen_list = random.choice(word_lists)

    category = chosen_list[0]
    chosen_word = chosen_list[random.randint(1, len(chosen_list) - 1)]

    pics = pixabay_getter.get_images(chosen_word, 4)

    return (chosen_word, category, pics)
