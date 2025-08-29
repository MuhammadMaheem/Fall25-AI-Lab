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
    # "programming" -> {'p': [0], 'r': [1, 4], 'o': [2], 'g': [3, 5], 'a': [6], 'm': [7, 8], 'i': [9], 'n': [10], 't': [11]}
    length_of_char = len(guessing_word)
    # programming -> 11
    displaying = replacing(word_map, guessed_letters, length_of_char)
     # ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_']
    wrong_guesses = 0
    limit_guesses = len(Hangman) - 1
    # limit_guesses = 7 (0-6)
    while True:
        letter = input("Enter a Letter to Guessing: ")
        if len(letter) != 1 or letter not in allowed_letters:
            print("Invaid character")
            continue
        if letter in guessed_letters:
            print("You already guessed that")
            continue

        else:
            if letter in guessing_word :
                guessed_letters.append(letter)
                displaying = replacing(word_map, guessed_letters, length_of_char)
                print(displaying)
                if "_" not in displaying:
                    print("Big W!")
                    break
            else: 
                wrong_guesses += 1
                print(Hangman[wrong_guesses])
                message = random.choice(messages)
                print(message)
                print(displaying)
                if wrong_guesses == limit_guesses:
                    break

def guessing(word):
    dic = {}
    # dic = "programming" -> {'p': [0], 'r': [1, 4], 'o': [2], 'g': [3, 5], 'a': [6], 'm': [7, 8], 'i': [9], 'n': [10], 't': [11]}

    count = 0
    for char in word:
        if char not in dic:
           dic[char] = []
        dic[char].append(count)
        count+=1
    return dic

def replacing(dictionary,guessed, lenght_of_letters):
  

    displaying = ["_"] * lenght_of_letters
    # displaying = ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_']

    for key, values in dictionary.items():
        if key in guessed:
            for pos in values:
                displaying[pos] = key
                # displaying = ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_']
                # displaying = ['p', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_']



    return displaying
    # displaying = ['p', 'r', 'o', 'g', 'r', 'a', 'm', 'm', 'i', 'n', 'g']

hangman()




















         

























