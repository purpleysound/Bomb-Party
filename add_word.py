
if __name__ == "__main__":
    word = input("Enter Word to Add: ")
    if word:
        with open("words.txt", "a") as f:
            f.write("\n"+word)
