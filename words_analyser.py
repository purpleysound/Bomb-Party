import json
from utils import sort_dictionary
LETTERS = "abcdefghijklmnopqrstuvwxyz"

with open("words.txt", "r") as f:
    words = f.readlines()
    words = set(map(lambda x: x.strip(), words))


def get_words(letters):
    letters = letters.lower()
    for word in words:
        if letters in word:
            yield word


def get_2_letter_pairs():
    for letter1 in LETTERS:
        for letter2 in LETTERS:
            yield letter1 + letter2


def make_2_letters_json():
    num_answers: dict[str, int] = dict()
    for letters in get_2_letter_pairs():
        num_answers[letters] = len(list(get_words(letters)))

    num_answers = sort_dictionary(num_answers, key=lambda x: x[1], reverse=True)

    with open("words_per_2_letters.json", "w") as f:
        json.dump(num_answers, f, indent=4)


def get_3_letter_pairs():
    for letter1 in LETTERS:
        for letter2 in LETTERS:
            for letter3  in LETTERS:
                yield letter1 + letter2 + letter3


def make_3_letters_json():
    num_answers: dict[str, int] = dict()
    for letters in get_3_letter_pairs():
        num_answers[letters] = len(list(get_words(letters)))

    num_answers = sort_dictionary(num_answers, key=lambda x: x[1], reverse=True)

    with open("words_per_3_letters.json", "w") as f:
        json.dump(num_answers, f, indent=4)


if __name__ == "__main__":
    make_3_letters_json()
    