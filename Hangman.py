from kivy.app import App
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
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


kv = Builder.load_file("Hangman.kv")


class HangmanApp(App):
    def build(self, phrase = True, hard_mode = False):
        self.word, self.phrase = pick_word.Pick(phrase, hard_mode)
        self.layout = kv
        self.guesses = []
        self.censored_word = ""
        self.num_wrong = 0
        self.max_wrong = 5  # How many guesses do you get
        self.correct_letters = []
        self.canvas = self.layout.get_screen("game").ids.mistake_counter.canvas
        self.mistake_counter = self.layout.get_screen("game").ids.mistake_counter
        self.layout.get_screen("game").ids.word.text = pick_word.censor_word(self.correct_letters, self.word)
        return self.layout

    def Enter(self):
        self.guess_txt = self.layout.get_screen("game").ids.guess_txt.text
        self.num_wrong, self.correct_letters, self.guesses = pick_word.check_guess(self.num_wrong, self.correct_letters,
                                                                                   self.guesses, self.word,
                                                                                   self.guess_txt)
        self.layout.get_screen("game").ids.mistake_counter.text = str(self.num_wrong)
        self.layout.get_screen("game").ids.word.text = pick_word.censor_word(self.correct_letters, self.word)
        self.layout.get_screen("game").ids.guess_txt.text = ""
        self.draw_rect()

    def get_hint(self):
        if self.phrase[0]:
            self.layout.get_screen("hint").ids.hint_text.text = self.phrase[1]
        else:
            r = requests.get(f"{dictionary_url}{self.word.strip()}")
            if not isinstance(r.json(), list):
                self.layout.get_screen("hint").ids.hint_text.text = "No Hint Available :("
            else:
                self.layout.get_screen("hint").ids.hint_text.text = r.json()[0]["meanings"][0]["definitions"][0][
                    "definition"]


    def draw_rect(self):
        self.rect_pos = [(self.mistake_counter.width * 0.2, self.mistake_counter.height * 0.1),
                         ((self.mistake_counter.width * 0.6) - 15,(self.mistake_counter.height * 0.1)+ 15),

                         ((self.mistake_counter.width * 0.6) - 15 - (self.mistake_counter.width * 0.2),
                          (self.mistake_counter.height * 0.1) + (self.mistake_counter.height * 0.7)),
                         (self.mistake_counter.width * 0.5, self.mistake_counter.height * 0.5),
                         (self.mistake_counter.width * 0.5, self.mistake_counter.height * 0.6)]
        self.rect_size = [(self.mistake_counter.width * 0.6, 15), (15, self.mistake_counter.height * 0.7), ((self.mistake_counter.width * 0.2), 15), (5, 5), (5, 5),
                          (5, 5)]
        self.canvas.clear()
        i = 0
        with self.canvas:
            while i < self.num_wrong:
                Color(1, 1, 1, 1)
                Rectangle(pos=self.rect_pos[i], size=self.rect_size[i])
                i += 1
            while i < self.max_wrong:
                Color(1, 0, 0, 1)
                Rectangle(pos=self.rect_pos[i], size=self.rect_size[i])
                i += 1


if __name__ == '__main__':
    HangmanApp().run()
