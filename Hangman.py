from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.switch import Switch
from kivy.graphics import Canvas, Rectangle, Color
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
import pick_word
import requests

dictionary_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"

LabelBase.register(name="PlayFair", fn_regular="PlayFairDisplay-Regular.ttf")


class Hint(Screen):
    pass


class Setting(Screen):
    pass


class GameScreen(Screen):
    pass


class Manager(ScreenManager):
    pass


class Boxes(FloatLayout):
    pass


kv = Builder.load_file("Hangman.kv")


class HangmanApp(App):
    def build(self):
        self.word, self.phrase = pick_word.Pick()
        self.layout = kv
        self.guesses = []
        self.censored_word = ""
        self.num_wrong = 0
        self.max_wrong = 6  # How many guesses do you get
        self.correct_letters = []
        self.layout.get_screen("game").ids.word.text = pick_word.censor_word(self.correct_letters, self.word)
        return self.layout

    def Enter(self):
        print("Enter")
        self.guess_txt = self.layout.get_screen("game").ids.guess_txt.text
        self.num_wrong, self.correct_letters, self.guesses = pick_word.check_guess(self.num_wrong, self.correct_letters,
                                                                                   self.guesses, self.word,
                                                                                   self.guess_txt)
        self.layout.get_screen("game").ids.mistake_counter.text = str(self.num_wrong)
        self.layout.get_screen("game").ids.word.text = pick_word.censor_word(self.correct_letters, self.word)
        self.layout.get_screen("game").ids.guess_txt.text = ""

    def get_hint(self):
        if self.phrase[0]:
            self.layout.get_screen("hint").ids.hint_text.text = self.phrase[1]
        else:
            r = requests.get(f"{dictionary_url}{self.word.strip()}")
            if not isinstance(r.json(), list):
                self.layout.get_screen("hint").ids.hint_text.text = "No Hint Available :("
            else:
                self.layout.get_screen("hint").ids.hint_text.text = r.json()[0]["meanings"][0]["definitions"][0]["definition"]


if __name__ == '__main__':
    HangmanApp().run()
