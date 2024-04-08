from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.core.audio import SoundLoader

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
        # 한글 폰트 설정
        LabelBase.register(name='AppleSDGothicNeoEB', fn_regular='./AppleSDGothicNeoEB.ttf')

        # 배경색 설정
        Window.clearcolor = (1, 1, 1, 1)  # 흰색 배경

        main_layout = GridLayout(cols=1, rows=2)

        # 상단 레이아웃: 입력된 번호를 표시하는 레이블
        top_layout = GridLayout(cols=1, rows=1, size_hint=(1, 0.2))
        self.display_label = Label(text=self.display_text, font_name='AppleSDGothicNeoEB', font_size='70sp', color=(0, 0, 0, 1)) # 검정색 텍스트
        top_layout.add_widget(self.display_label)
        main_layout.add_widget(top_layout)

        # 하단 레이아웃: 숫자 버튼 및 기능 버튼
        bottom_layout = GridLayout(cols=3, rows=4, size_hint=(1, 0.8))
        for i in range(1, 10):
            button = Button(text=str(i), on_press=self.on_button_click, font_name='AppleSDGothicNeoEB', font_size='60sp')
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

        return main_layout

    def on_button_click(self, instance):
        # 버튼을 누르면 입력된 번호를 표시하는 레이블을 업데이트
        button_text = instance.text
        if len(self.display_text) < 13:  # 최대 길이는 13자
            # '-'를 자동으로 추가
            if len(self.display_text) in [3, 8]:
                self.display_text += '-'
            self.display_text += button_text
            self.display_label.text = self.display_text
            self.play_button_sound(button_text)

    def cancel_input(self, instance):
        # 취소 버튼을 누르면 입력된 번호를 한 글자씩 삭제
        if self.display_text:
            if len(self.display_text) == 9:  # '-'를 만난 경우
                self.display_text = self.display_text[:-2]
            else:
                self.display_text = self.display_text[:-1]
            self.display_label.text = self.display_text
            self.play_button_sound('back')

    def complete_input(self, instance):
        # 입력된 번호가 13자리인 경우에만 확인 처리
        if len(self.display_text) == 13:
            print("입력된 번호:", self.display_text)
            self.play_button_sound('clear')
        else:
            print("입력된 번호는 13자리여야 확인됩니다.")

    def play_button_sound(self, sound_key):
        if sound_key in self.button_sounds:
            sound = self.button_sounds[sound_key]
            if sound:
                sound.play()

if __name__ == '__main__':
    GalaxyTabApp().run()
