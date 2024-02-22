words = set()
with open('words.txt', 'r') as f:
    for word in f:
        words.add(word.strip().lower())

with open("words_alpha.txt", "r") as f:
    for word in f:
        words.add(word.strip().lower())

words = sorted(words)  # mmm 450 000 words sorted
with open("words.txt", "w") as f:
    for word in words:
        f.write(word + '\n')
