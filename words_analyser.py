import json
LETTERS = "abcdefghijklmnopqrstuvwxyz"

with open("words.txt", "r") as f:
    words = f.readlines()
    words = set(map(lambda x: x.strip(), words))


def get_words(letters):
    letters = letters.lower()
    for word in words:
        if letters in word:
            yield word


def get_letter_pairs():
    for letter1 in LETTERS:
        for letter2 in LETTERS:
            yield letter1 + letter2


def make_syllable_json():
    num_answers: dict[str, int] = dict()
    for letters in get_letter_pairs():
        num_answers[letters] = len(list(get_words(letters)))

    num_answers = {k: v for k, v in sorted(num_answers.items(), key=lambda item: item[1], reverse=True)}

    with open("words_per_syllable.json", "w") as f:
        json.dump(num_answers, f, indent=4)


if __name__ == "__main__":
    pass
    