import random

# Hangman stages (dynamic)
Hangman = [
    """
     +---+
         |
         |
         |
        ===
    """,
    """
     +---+
     O   |
         |
         |
        ===
    """,
    """
     +---+
     O   |
     |   |
         |
        ===
    """,
    """
     +---+
     O   |
    /|   |
         |
        ===
    """,
    """
     +---+
     O   |
    /|\\  |
         |
        ===
    """,
    """
     +---+
     O   |
    /|\\  |
    /    |
        ===
    """,
    """
     +---+
     O   |
    /|\\  |
    / \\  |
        ===
    """
]



messages = ["Have Some Humanity", "ahh useless" , "Get Better Kid", "You are a disgrace to your family", "You are a failure", "You are a joke"]

words = ["Computer", "Programming", "Python"]


def hangman():
    allowed_letters = ("abcdefghijklmnopqrstuvwxyz")
    guessing_word = random.choice(words).lower()
    guessed_letters = []
    word_map= guessing(guessing_word)
    length_of_char = len(guessing_word)
    wrong_guesses = 0
    limit_guesses = len(Hangman) - 1
    while True:
        letter = input("Enter a Letter to Guessing: ")
        if len(letter) != 1 or letter not in allowed_letters:
            print("Invaid character")
        if letter in guessed_letters:
            print("You already guessed that")
            continue

        else:
            if letter in guessing_word :
                guessed_letters.append(letter)
                displaying = replacing(word_map, guessed_letters, length_of_char)
                if "_" not in displaying:
                    print("Big W!")
                    break
            else: 
                wrong_guesses += 1
                print(Hangman[wrong_guesses])
                message = random.choice(messages)
                print(message)
                if wrong_guesses == limit_guesses:
                    break

def guessing(word):
    dic = {}
    count = 0
    for char in word:
        if char not in dic:
           dic[char] = []
        dic[char].append(count)
        count+=1
    return dic

def replacing(dictionary,guessed, lenght_of_letters):
  

    displaying = ["_"] * lenght_of_letters

    for key, values in dictionary.items():
        if key in guessed:
            for pos in values:
                displaying[pos] = key
    print(displaying)
    return displaying

hangman()




















         

























