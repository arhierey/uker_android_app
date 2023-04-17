from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Rectangle
from kivy.uix.spinner import Spinner
from kivy.uix.spinner import SpinnerOption


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


class CustomOption(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (.79, .63, .44, 1)


class RootWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.FONT_SIZE = 40
        self.colors = {
            'blue': (.68, .82, .86, 1),
            'sand': (.96, .95, .91, 1),
            'wet-sand': (.94, .87, .63, 1),
            'brown': (.47, .37, .21, 1),
            'light-brown': (.79, .63, .44, 1),
        }
        self.spinner_labels = (
            'what string?',
            'what fret? (0-11)',
            'what fret? (12-24)'
        )

        self.uke = SopranoUkulele()
        self.guitar = Guitar()

        self.bind(size=self.update_background, pos=self.update_background)
        with self.canvas.before:
            self.background = Rectangle(source='uker_concept_back.png',
                                        size=self.size, pos=self.pos)

        input_layout = BoxLayout(orientation='horizontal', size_hint=(1, .1), pos_hint={'top': 1})

        self.spinner1 = Spinner(
            size_hint=(.5, 1),
            text=self.spinner_labels[0],
            values=('1', '2', '3', '4', '5', '6'),
            background_normal='', background_color=self.colors['light-brown'],
            option_cls=CustomOption,
        )
        self.spinner2 = Spinner(
            size_hint=(.5, 1),
            text=self.spinner_labels[1],
            values=(str(i) for i in range((self.guitar.fret_number+1)//2)),
            background_normal='', background_color=self.colors['light-brown'],
            option_cls=CustomOption,
        )
        self.spinner3 = Spinner(
            size_hint=(.5, 1),
            text=self.spinner_labels[2],
            values=(str(i) for i in range((self.guitar.fret_number+1)//2, self.guitar.fret_number+1)),
            background_normal='', background_color=self.colors['light-brown'],
            option_cls=CustomOption,
        )

        input_sub_box2 = BoxLayout(orientation='horizontal', size_hint=(.5, 1))

        input_sub_box2.add_widget(self.spinner2)
        input_sub_box2.add_widget(self.spinner3)

        input_layout.add_widget(self.spinner1)

        input_layout.add_widget(input_sub_box2)

        self.add_widget(input_layout)

        self.convert_button = Button(text='CONVERT', size_hint=(1, .1), pos_hint={'bottom': 1},
                                     background_normal='', background_color=self.colors['brown'],
                                     on_press=self.convert_data, font_size=self.FONT_SIZE)

        self.add_widget(self.convert_button)

        self.output = Label(text='', size_hint=(1, .8), pos_hint={'top': .9}, font_size=self.FONT_SIZE,
                            color=self.colors['brown'])
        self.add_widget(self.output)

    def update_background(self, instance, value):
        self.background.size = self.size
        self.background.pos = self.pos

    def convert_data(self, instance):
        input1 = self.spinner1.text
        input2 = self.spinner2.text
        input3 = self.spinner3.text

        input1_filled = input1 != self.spinner_labels[0]
        input2_filled = input2 != self.spinner_labels[1]
        input3_filled = input3 != self.spinner_labels[2]

        guitar_note = ''
        if input1_filled and (input2_filled != input3_filled):
            if input1_filled and input2_filled:
                guitar_note = self.guitar.get_note(int(input1), int(input2))
            elif input1_filled and input3_filled:
                guitar_note = self.guitar.get_note(int(input1), int(input3))
            uke_str = self.uke.get_strings(guitar_note)
            output = 'Note is ' + guitar_note + '\n' + '\n'.join(
                {1: 'first', 2: 'second', 3: 'third', 4: 'fourth'}[each[0]] + ' string ' + str(each[1]) + ' fret'
                for each in uke_str)
        else:
            output = ''

        self.spinner1.text = self.spinner_labels[0]
        self.spinner2.text = self.spinner_labels[1]
        self.spinner3.text = self.spinner_labels[2]

        self.output.text = output


class MyApp(App):
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    app = MyApp()
    app.run()
