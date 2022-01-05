from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import *
import pick_word

guesses = []
num_wrong = 0
max_wrong = 6  # How many guesses do you get
correct_letters = []

class Boxes(FloatLayout):
    pass


class HangmanApp(App):
    def build(self):
        self.word = pick_word.Pick()
        self.layout = Boxes()
        return self.layout

    def Enter(self):
        print("Enter")
        self.guess_txt = self.layout.ids.guess_txt
        self.counter = self.layout.ids.counter
        self.counter.text = self.guess_txt.text


if __name__ == '__main__':
    HangmanApp().run()
