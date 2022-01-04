import json
import csv
import random
import pygame

word = ""

phrase = False
hard_mode = False
game_type = input("Would you like a word or phrase?")
if game_type.lower() == "phrase":
    phrase = True

if not phrase:
    hard_mode_choice = input("Would You like to play hard Mode? Type 'Yes' if so or anything else if not.")
    if hard_mode_choice.lower() == "yes":
        hard_mode = True

    if hard_mode:
        with open("words_dictionary_hard.txt") as words:
            words = list(words)
            word = words[random.randint(0, len(words)-1)]
            print(word)
    else:
        with open("Common_words.csv", newline="") as common_words:
            reader = csv.reader(common_words)
            common_words = list(reader)
            word = common_words[random.randint(0, len(common_words) - 1)]
            print(word)

else:
    with open("Common_phrases.csv", newline="", encoding="utf-8-sig") as common_phrases:
        reader = csv.DictReader(common_phrases, delimiter=';')
        common_phrases = list(reader)

