import socket
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
import threading

class InputScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = GridLayout(cols=2)
        self.layout.add_widget(Label(text='서버 IP 주소:'))
        self.ip_input = TextInput(multiline=False)
        self.layout.add_widget(self.ip_input)
        self.layout.add_widget(Label(text='포트 번호:'))
        self.port_input = TextInput(multiline=False)
        self.layout.add_widget(self.port_input)

        self.connect_button = Button(text='연결', on_press=self.connect)
        self.layout.add_widget(self.connect_button)

        self.add_widget(self.layout)

    def connect(self, instance):
        ip_address = self.ip_input.text
        port_number = int(self.port_input.text)
        app = App.get_running_app()
        app.connect_to_server(ip_address, port_number)
        app.change_to_number_pad_screen()

class NumberPadScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = GridLayout(cols=3)
        for i in range(1,10):
            button = Button(text=str(i), on_press=self.on_button_click)
            self.layout.add_widget(button)
        self.layout.add_widget(Button(text='취소', on_press=self.cancel_input))
        self.layout.add_widget(Button(text='0', on_press=self.on_button_click))
        self.layout.add_widget(Button(text='완료', on_press=self.complete_input))

        self.add_widget(self.layout)

        def on_button_click(self, instance):
            button_text = instance.text
            if len(self.display_text) < 13:
                if len(self.display_text) == 3 and button_text != '-':
                    self.display_text += '-'
                elif len(self.display_text) == 8 and button_text != '-':
                    self.display_text += '-'
                self.display_text += button_text
                self.display_label.text = self.display_text
                self.play_button_sound(button_text)

        def cancel_input(self, instance):
            if self.display_text:
                if len(self.display_text) == 10:
                    self.display_text = self.display_text[:-2]
                elif len(self.display_text) == 5:
                    self.display_text = self.display_text[:-2]
                else:
                    self.display_text = self.display_text[:-1]
                self.display_label.text = self.display_text
                self.play_button_sound('back')

        def complete_input(self, instance):
            if len(self.display_text) == 13:
                print("입력된 번호:", self.display_text)
                self.send_to_server(self.display_text)

                self.display_text = '010-'
                self.play_button_sound('clear')
            else:
                print("입력된 번호는 13자리여야 확인됩니다.")

class GalaxyTabApp(App):
    def __init__(self, **kwargs):
        super(GalaxyTabApp, self).__init__(**kwargs)
        self.display_text = '010'
        self.button_sounds = {
            '0': SoundLoader.load('0.mp3'),
            '1': SoundLoader.load('1.mp3'),
            '2': SoundLoader.load('2.mp3'),
            '3': SoundLoader.load('3.mp3'),
            '4': SoundLoader.load('4.mp3'),
            '5': SoundLoader.load('5.mp3'),
            '6': SoundLoader.load('6.mp3'),
            '7': SoundLoader.load('7.mp3'),
            '8': SoundLoader.load('8.mp3'),
            '9': SoundLoader.load('9.mp3'),
            'back': SoundLoader.load('back.mp3'),
            'clear': SoundLoader.load('clear.mp3'),
        }

    def build(self):
        self.screen_manager = ScreenManager()

        self.input_screen = InputScreen(name='input')
        self.number_pad_screen = NumberPadScreen(name='number_pad')

        self.screen_manager.add_widget(self.input_screen)
        self.screen_manager.add_widget(self.number_pad_screen)

        return self.screen_manager

    def connect_to_server(self):
        HOST = '192.168.0.2'
        PORT = 65432
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print("서버에 연결되었습니다.")
            #
            # while True:
            #     phone_number = input("전화번호를 입력하세요: ")
            #     s.sendall(phone_number.encode())
            # s.sendall("종료".encode())
            # while True:
            #     pass  # 계속해서 서버와 연결을 유지

    def play_button_sound(self, sound_key):
        if sound_key in self.button_sounds:
            sound = self.button_sounds[sound_key]
            if sound:
                sound.play()

    def send_to_server(self, data):
        HOST = '192.168.0.2'
        PORT = 65432
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            # print("서버에 연결되었습니다")
            s.sendall(data.encode())

    # def on_stop(self):
    #     # 앱이 종료될 때 서버로 종료 메시지를 보냄
    #     # 서버에서는 이 메시지를 받아 서버를 종료할 수 있도록 구현
    #     pass

    def change_to_number_pad_screen(self):
        self.screen_manager.current = 'number_pad'

if __name__ == '__main__':
    GalaxyTabApp().run()
