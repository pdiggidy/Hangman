import re
import csv
import random


def Pick(word=True, hard_mode=False):
    game_type = "word"  # input("Would you like a word or phrase? ")
    phrase_info = {"Meaning": ""}

    if word:
        if hard_mode:  # If the player has selected hard mode pick a word from the extended list
            with open("words_dictionary_hard.txt") as words:
                words = list(words)
                word = words[random.randint(0, len(words) - 1)]
        else:
            with open("Common_words.csv", newline="") as common_words:
                reader = csv.reader(common_words)
                common_words = list(reader)
                word = common_words[random.randint(0, len(common_words) - 1)][0]

    else:  # Pick a random phrase from the list
        with open("Common_phrases.csv", newline="", encoding="utf-8-sig") as common_phrases:
            reader = csv.DictReader(common_phrases, delimiter=';')
            common_phrases = list(reader)
            phrase_info = common_phrases[random.randint(0, len(common_phrases) - 1)]  # Store the phrase info for hints
            word = phrase_info["Idiom"]  # Take just the phrase
    word = word.replace('"', "")
    return word, (not word, phrase_info["Meaning"])


def check_guess(num_wrong, correct_letters, guesses, word, guess):
    guess = re.findall("[a-zA-Z]", guess.strip().lower())  # Check if the guess is just a letter
    if len(guess) != 1:
        print("Please only guess one letter. ")
        return num_wrong, correct_letters, guesses
    else:
        guess = guess[0]  # Find all returns a list so take the first element
    if guess in guesses:
        print("You've already guessed that letter. Try again.")
        return num_wrong, correct_letters, guesses
    else:
        if guess in word:
            correct_letters.append(guess)
            guesses.append(guess)
            print("That guess is correct!")
            return num_wrong, correct_letters, guesses
        else:
            guesses.append(guess)
            num_wrong += 1
            print("That letter is wrong.")
            return num_wrong, correct_letters, guesses


def censor_word(correct_letters, word):
    censored_word_temp = ""
    for i in word.lower():
        if i == " ":
            censored_word_temp += " "
        if i in correct_letters:
            censored_word_temp += i
        if i not in correct_letters:
            censored_word_temp += "_"
    return censored_word_temp
