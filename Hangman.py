from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Canvas, Rectangle, Color
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
import pick_word

LabelBase.register(name="PlayFair", fn_regular="PlayFairDisplay-Regular.ttf")


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
        self.word = pick_word.Pick()
        self.layout = kv
        self.guesses = []
        self.censored_word = ""
        self.num_wrong = 0
        self.max_wrong = 6  # How many guesses do you get
        self.correct_letters = []
        self.layout.get_screen("game").ids.word.text= pick_word.censor_word(self.correct_letters, self.word)
        return self.layout

    def Enter(self):
        print("Enter")
        self.guess_txt = self.layout.ids.guess_txt.text
        self.num_wrong, self.correct_letters, self.guesses = pick_word.check_guess(self.num_wrong, self.correct_letters,
                                                                                   self.guesses, self.word,
                                                                                   self.guess_txt)
        self.layout.ids.mistake_counter.text = str(self.num_wrong)
        self.layout.ids.word.text = pick_word.censor_word(self.correct_letters, self.word)
        self.layout.ids.guess_txt.text = ""


if __name__ == '__main__':
    HangmanApp().run()
