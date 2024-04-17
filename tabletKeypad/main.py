import socket
import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import mainthread

import threading

class InputScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 전체 화면을 가운데에 정렬하기 위한 FloatLayout
        self.layout = FloatLayout()

        # 서버 IP 주소 입력창과 라벨을 오른쪽 정렬하는 BoxLayout
        ip_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(None, None), size=(350, 40))
        ip_label = Label(text='서버 IP 주소(숫자만 입력하세요):', font_name='AppleSDGothicNeoEB', font_size=20, color=(0,0,0,1),
                         halign='right', size_hint=(None, None), size=(150, 40))
        self.ip_input = IPInput(multiline=False, size_hint=(None, None), size=(200, 40))
        # self.ip_input.foreground_color=(0,0,0,1)
        ip_layout.add_widget(ip_label)
        ip_layout.add_widget(self.ip_input)
        ip_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.7}  # 중앙에 배치

        # 포트 번호 입력창과 라벨을 오른쪽 정렬하는 BoxLayout
        port_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(None, None), size=(350, 40))
        port_label = Label(text='포트 번호:', font_name='AppleSDGothicNeoEB', font_size=20, color=(0,0,0,1),
                           halign='right', size_hint=(None, None), size=(150, 40))
        self.port_input = TextInput(multiline=False, size_hint=(None, None), size=(100, 40))
        port_layout.add_widget(port_label)
        port_layout.add_widget(self.port_input)
        port_layout.pos_hint = {'center_x': 0.5, 'center_y': 0.6}  # 중앙에 배치

        # 연결 버튼
        self.connect_button = Button(text='연결', on_press=self.connect, font_name='AppleSDGothicNeoEB',
                                     size_hint=(None, None), size=(100, 40))
        self.connect_button.pos_hint = {'center_x': 0.5, 'center_y': 0.3}  # 중앙에 배치

        # 오류 메시지 텍스트
        self.error_label = Label(text='', font_name='AppleSDGothicNeoEB', font_size=15, color=(1, 0, 0, 1),
                                 size_hint=(None, None), size=(350, 30), pos_hint={'center_x': 0.5, 'center_y': 0.2})

        # 레이아웃에 위젯 추가
        self.layout.add_widget(ip_layout)
        self.layout.add_widget(port_layout)
        self.layout.add_widget(self.connect_button)
        self.layout.add_widget(self.error_label)

        self.add_widget(self.layout)

    # def connect(self, instance):
    #     ip_address = self.ip_input.text
    #     port_number = int(self.port_input.text)
    #
    #     app = App.get_running_app()
    #
    #     HOST = ip_address
    #     PORT = port_number
    #     try:
    #         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #             s.connect((HOST, PORT))
    #             print("서버에 연결되었습니다.")
    #             app.change_to_number_pad_screen(HOST, PORT)
    #             # app.change_to_image_screen(HOST, PORT)
    #     except Exception as e:
    #         # print("서버 연결에 실패했습니다:", e)
    #         self.error_label.text = "서버 연결에 실패했습니다: {}".format(e)

    def connect(self, instance):
        ip_address = self.ip_input.text
        port_number = int(self.port_input.text)

        app = App.get_running_app()

        HOST = ip_address
        PORT = port_number

        app.set_connection_info(HOST, PORT)

class IPInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_chars = 12  # 최대 12자까지 입력
    def insert_text(self, substring, from_undo=False):
        if len(self.text) in [3, 7, 9] and substring.isdigit():
            # 특정 위치에 '.' 추가
            substring = '.' + substring
        super(IPInput, self).insert_text(substring, from_undo=from_undo)

    def do_backspace(self, from_undo=False, mode='bkspc'):
        # 부모 클래스의 do_backspace 메서드 호출
        super(IPInput, self).do_backspace(from_undo=from_undo, mode=mode)

        # 텍스트가 빈 경우에는 추가적인 처리를 하지 않음
        if not self.text:
            return

        # 텍스트가 빈 경우가 아니면 맨 뒤에 있는 문자를 확인하여 처리
        last_char = self.text[-1]

        if last_char == '.':
            # 맨 뒤에 있는 문자가 '.'인 경우에는 마지막 '.'을 삭제
            self.text = self.text[:-1]
        elif last_char.isdigit() and len(self.text) in [4, 8, 10]:
            # 맨 뒤에 있는 문자가 숫자이고 특정 위치에 '.'이 있는 경우에는 해당 숫자를 삭제
            self.text = self.text[:-1]

# class ImageScreen(Screen):
#     def __init__(self, image_path, **kwargs):
#         super().__init__(**kwargs)
#         self.image_path = image_path
#         self.layout = FloatLayout()
#         self.image = Image(source=self.image_path, allow_stretch=True, keep_ratio=False)
#         self.layout.add_widget(self.image)
#         self.add_widget(self.layout)
#
#     def on_pre_enter(self, *args):
#         #이미지가 화면에 꽉 차도록 크기를 조정합니다.
#         self.image.size = Window.size

class NumberPadScreen(Screen):
    def __init__(self, button_sounds, host=None, port=None, display_text='', **kwargs):
        super().__init__(**kwargs)

        self.HOST = host
        self.PORT = port

        self.button_sounds = button_sounds
        self.display_text = '010' # display_text 속성 초기화

        LabelBase.register(name='AppleSDGothicNeoEB', fn_regular='./AppleSDGothicNeoEB.ttf')
        Window.clearcolor = (1, 1, 1, 1)  # 흰색 배경

        main_layout = GridLayout(cols=1, rows=2)

        # 상단 레이아웃: 입력된 번호를 표시하는 레이블
        top_layout = GridLayout(cols=1, rows=1, size_hint=(1, 0.2))
        self.display_label = Label(text=self.display_text, font_name='AppleSDGothicNeoEB', font_size='70sp',
                                   color=(0, 0, 0, 1))
        top_layout.add_widget(self.display_label)
        main_layout.add_widget(top_layout)

        # 하단 레이아웃: 숫자 버튼 및 기능 버튼
        bottom_layout = GridLayout(cols=3, rows=4, size_hint=(1, 0.8))
        for i in range(1, 10):
            button = Button(text=str(i), on_press=self.on_button_click, font_name='AppleSDGothicNeoEB',
                            font_size='60sp')
            bottom_layout.add_widget(button)

        # 취소 버튼
        cancel_button = Button(text='취소', on_press=self.cancel_input, font_name='AppleSDGothicNeoEB', font_size='60sp')
        bottom_layout.add_widget(cancel_button)

        # 0 버튼
        zero_button = Button(text='0', on_press=self.on_button_click, font_name='AppleSDGothicNeoEB', font_size='60sp')
        bottom_layout.add_widget(zero_button)

        # 완료 버튼
        done_button = Button(text='완료', on_press=self.complete_input, font_name='AppleSDGothicNeoEB', font_size='60sp')
        bottom_layout.add_widget(done_button)

        main_layout.add_widget(bottom_layout)

        self.add_widget(main_layout)

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

    def complete_input(self, server_connection):
        if len(self.display_text) == 13:
            print("입력된 번호:", self.display_text)
            # self.send_to_server(self.display_text)
            app = App.get_running_app()
            app.send_message_to_server(self.display_text)
            self.display_text = '010-'
            self.play_button_sound('clear')
        else:
            print("입력된 번호는 13자리여야 확인됩니다.")

    def play_button_sound(self, sound_key):
        if sound_key in self.button_sounds:
            sound = self.button_sounds[sound_key]
            if sound:
                sound.play()
    def send_to_server(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(data.encode())
            self.display_text = '010-'
            self.display_label.text = self.display_text

class GalaxyTabApp(App):
    def __init__(self, **kwargs):
        super(GalaxyTabApp, self).__init__(**kwargs)
        self.HOST = None
        self.PORT = None
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
        self.server_socket=None

    def build(self):

        script_dir = os.path.dirname(__file__)
        font_path = os.path.join(script_dir, "AppleSDGothicNeoEB.ttf")
        image_path = os.path.join(script_dir, "기본사진.png")
        LabelBase.register("AppleSDGothicNeoEB", font_path)

        self.screen_manager = ScreenManager()

        self.input_screen = InputScreen(name='input')
        self.number_pad_screen = NumberPadScreen(name='number_pad',
                                                 button_sounds=self.button_sounds)

        # self.image_screen = ImageScreen(name='image_screen', image_path=image_path)

        self.screen_manager.add_widget(self.input_screen)
        self.screen_manager.add_widget(self.number_pad_screen)
        # self.screen_manager.add_widget(self.image_screen) #이미지 스크린을 스크린 매니저에 추가합니다.

        return self.screen_manager

    def change_to_number_pad_screen(self, host, port):
        self.number_pad_screen.HOST = host
        self.number_pad_screen.PORT = port
        self.HOST = host
        self.PORT = port
        self.screen_manager.current = 'number_pad'

    # def change_to_image_screen(self, host, port):
    #     self.HOST = host
    #     self.PORT = port
    #     self.screen_manager.current = 'image_screen'

    def set_connection_info(self, host, port):
        self.HOST = host
        self.PORT = port
        self.connect_to_server(host, port)

    def connect_to_server(self, host, port):
        self.HOST = host
        self.PORT = port
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.connect((self.HOST, self.PORT))
            print("서버에 연결되었습니다")
            self.change_to_number_pad_screen(self.HOST, self.PORT)
            # self.change_to_image_screen(self.HOST, self.PORT)

            #서버로부터 메시지를 받는 스레드 시작
            receive_thread = threading.Thread(target=self.receive_messages_from_server)
            receive_thread.daemon = True
            receive_thread.start()
        except Exception as e:
            print("서버 연결에 실패했습니다:", e)

    def send_message_to_server(self, message):
        try:
            if self.server_socket:
                self.server_socket.sendall(message.encode())
                print("메시지 전송 성공:", message)
                # self.change_to_image_screen(self.HOST, self.PORT)
            else:
                print("서버에 연결되어 있지 않습니다.")
        except Exception as e:
            print("메시지 전송 실패", e)

    @mainthread
    def process_server_message(self, message):
        print("서버로부터 온 메시지:", message)
        if message == "change_to_number_pad_screen":
            self.change_to_number_pad_screen(self.HOST, self.PORT)

    def receive_messages_from_server(self):
        while True:
            try:
                if self.server_socket:
                    data = self.server_socket.recv(1024).decode()
                    if data:
                        self.process_server_message(data)
                        # if data == "change_to_number_pad_screen":
                        #     # self.change_to_image_screen(self.HOST, self.PORT)
                        #     self.change_to_number_pad_screen(self.HOST, self.PORT)
                else:
                    print("서버에 연결되어 있지 않습니다.")
                    break
            except Exception as e:
                print("메시지 수신 중 오류 발생:", e)
                break

if __name__ == '__main__':
    GalaxyTabApp().run()
