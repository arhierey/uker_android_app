from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Rectangle


class StringInstrument:
    def __init__(self):
        self.str_number = None
        self.fret_number = None
        self.tuning = None
        self.trans = {
            'C': 'C#',
            'D': 'D#',
            'E': 'F',
            'F': 'F#',
            'G': 'G#',
            'A': 'B',
            'B': 'H',
            'C#': 'D',
            'D#': 'E',
            'F#': 'G',
            'G#': 'A',
            'H': 'C'
        }

    def get_note(self, string, fret):
        note = self.tuning[string]
        for i in range(fret):
            note = self.trans[note]
        return note

    def get_strings(self, note):
        res = []
        for i in range(self.str_number):
            instr_note = self.tuning[i + 1]
            if instr_note == note:
                res.append([i + 1, 0])
            for j in range(self.fret_number):
                instr_note = self.trans[instr_note]
                if instr_note == note:
                    res.append([i+1, j+1])
        return res


class SopranoUkulele(StringInstrument):
    def __init__(self):
        super().__init__()
        self.fret_number = 13
        self.str_number = 4
        self.tuning = {1: 'A', 2: 'E', 3: 'C', 4: 'G'}

    def __str__(self):
        tuning = ''.join(self.tuning[each] for each in self.tuning)
        return 'soprano ukulele with tuning:' + tuning[::-1]


class Guitar(StringInstrument):
    def __init__(self):
        super().__init__()
        self.fret_number = 24
        self.str_number = 6
        self.tuning = {1: 'E', 2: 'H', 3: 'G', 4: 'D', 5: 'A', 6: 'E'}

    def __str__(self):
        tuning = ''.join(self.tuning[each] for each in self.tuning)
        return 'guitar with tuning:' + tuning[::-1]


class CustomButton(Button):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.background_color = (.68, .82, .86, 1)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.background_color = (.47, .37, .21, 1)
        return super().on_touch_up(touch)


class RootWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.uke = SopranoUkulele()  # TODO: ensure it's working
        self.guitar = Guitar()

        self.bind(size=self.update_background, pos=self.update_background)
        with self.canvas.before:
            self.background = Rectangle(source='uker_concept_back.png',
                                        size=self.size, pos=self.pos)

        # styles - 929

        input_layout = BoxLayout(orientation='vertical', size_hint=(1, .2), pos_hint={'top': 1})

        input_sub_box1 = BoxLayout(orientation='horizontal', size_hint=(1, .5))
        input_sub_box2 = BoxLayout(orientation='horizontal', size_hint=(1, .5))

        self.label_string = Label(text='STRING NUMBER', font_size=20, color=(.47, .37, .21, 1))
        self.label_fret = Label(text='FRET NUMBER', font_size=20, color=(.47, .37, .21, 1))

        self.input_string = TextInput(background_normal='', background_color=(0, 0, 0, 0),
                                      padding=[self.width/2, 0, self.width/2, 0], font_size=20,
                                      foreground_color=(.47, .37, .21, 1))
        self.input_fret = TextInput(background_normal='', background_color=(0, 0, 0, 0),
                                    padding=[self.width/2, 0, self.width/2, 0], font_size=20,
                                    foreground_color=(.47, .37, .21, 1))

        input_sub_box1.add_widget(self.label_string)
        input_sub_box1.add_widget(self.label_fret)

        input_sub_box2.add_widget(self.input_string)
        input_sub_box2.add_widget(self.input_fret)

        input_layout.add_widget(input_sub_box1)
        input_layout.add_widget(input_sub_box2)

        self.add_widget(input_layout)

        self.convert_button = CustomButton(text='CONVERT', size_hint=(1, .1), pos_hint={'bottom': 1},
                                           background_normal='', background_color=(.47, .37, .21, 1),
                                           on_press=self.convert_data, font_size=20)

        self.add_widget(self.convert_button)

        self.output = Label(text='', size_hint=(1, .8), pos_hint={'top': .9}, font_size=20, color=(.47, .37, .21, 1))
        self.add_widget(self.output)

    def update_background(self, instance, value):
        self.background.size = self.size
        self.background.pos = self.pos

    def convert_data(self, instance):
        input1 = self.input_string.text
        input2 = self.input_fret.text

        self.input_fret.text, self.input_string.text = '', ''
        try:
            guitar_note = self.guitar.get_note(int(input1), int(input2))
            uke_str = self.uke.get_strings(guitar_note)
            output = 'Note is ' + guitar_note + '\n' + '\n'.join(
                {1: 'first', 2: 'second', 3: 'third', 4: 'fourth'}[each[0]] + ' string ' + str(each[1]) + ' fret'
                for each in uke_str)
        except ValueError:
            output = ''
        except KeyError:
            output = ''

        self.output.text = output


class MyApp(App):
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    app = MyApp()
    app.run()
