import errno
import socket
import threading
import sys
import random
import subprocess
import platform
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtGui import QFont, QFontDatabase

import usb.core
import usb.util

dev = usb.core.find(True)
if dev is None:
    print("No device")
else:
    print("device : ", dev)

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.server = None
        # self.add_firewall_rule()
        # self.find_usb_device()

    def initUI(self):
        self.setWindowTitle('PC KEYPAD')
        self.setGeometry(400, 400, 400, 400)

        # 폰트 설정
        # font_id = QFontDatabase.addApplicationFont("AppleSDGothicNeoEB.ttf")
        # print('font id:', font_id)
        # font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        # print('font family:', QFontDatabase.applicationFontFamilies(font_id))
        # font_path = "./AppleSDGothicNeoEB.ttf"
        # font = QFont(font_path)
        # font.setPointSize(25)

        font = QFont()
        font.setPointSize(25)

        # IP 주소와 포트 번호를 표시하는 라벨
        self.ip_label = QLabel("IP 주소 : 000.000.0.0")
        self.ip_label.setFont(font)
        self.ip_label.setAlignment(Qt.AlignCenter)  # 가운데 정렬 설정
        self.port_label = QLabel("포트 번호 : -----")
        self.port_label.setFont(font)
        self.port_label.setAlignment(Qt.AlignCenter)  # 가운데 정렬 설정

        self.received_message_label = QLabel("")
        self.received_message_label.setFont(font)
        self.received_message_label.setAlignment(Qt.AlignCenter)

        button_font = font
        button_font.setPointSize(15)

        self.btn_copy = QPushButton('복사', self)
        self.btn_copy.setVisible(False)
        self.btn_copy.setFixedSize(100,50)
        self.btn_copy.setFont(button_font)

        self.btn_receive = QPushButton('번호 지우기', self)
        self.btn_receive.setVisible(False)
        self.btn_receive.setFixedSize(300, 50)
        self.btn_receive.setFont(button_font)

        #라벨과 버튼을 포함하는 수평 레이아웃 생성
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.received_message_label)
        h_layout.addWidget(self.btn_copy)

        # 수직 레이아웃 생성하여 라벨 및 버튼 추가
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.ip_label)
        v_layout.addWidget(self.port_label)
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.btn_receive)

        # 포트 라벨과 버튼 사이의 간격을 조정
        v_layout.setSpacing(5)  # 5 픽셀 간격으로 설정

        # 수직 레이아웃을 중앙에 배치
        central_widget = QWidget(self)
        central_widget.setLayout(v_layout)
        central_layout = QVBoxLayout(self)
        central_layout.addWidget(central_widget)
        central_layout.setAlignment(Qt.AlignCenter)

        self.setLayout(central_layout)

        self.btn_receive.clicked.connect(self.sendSignalToClients)
        self.btn_copy.clicked.connect(self.btnClicked)

    def find_usb_device(self):
        #usb 장치 찾기
        self.device = usb.core.find()
        if self.device is None:
            print('USB 장치를 찾을 수 없습니다.')
            return
        try:
            #USB 장치 정보 출력
            print("Manufacturer:", usb.util.get_string(self.device, self.device.iManufacturer))
            print("Product:", usb.util.get_string(self.device, self.device.iProduct))
            print("Serial:", usb.util.get_string(self.device, self.device.iSerialNumber))

        except Exception as e:
            print("USB 장치 접근 중 오류 발생", e)
            return

    def show_server_info(self, host, port):
        self.ip_label.setText(f"IP 주소: {host}")
        self.port_label.setText(f"포트 번호: {port}")
        print('server: ', self.server)

    def show_received_message(self, message):
        self.ip_label.hide()
        self.port_label.hide()

        self.received_message_label.setText(message)

        #수신된 데이터가 표시될 때만 버튼을 보이도록 설정
        self.btn_copy.setVisible(True)
        self.btn_receive.setVisible(True)

    def btnClicked(self):
        #클립보드에 저장할 텍스트
        original_text = self.received_message_label.text()
        #하이픈 제거
        # modified_text = original_text[:3]+original_text[4:8]+original_text[9:]

        #클립보드에 수신된 데이터 저장
        clipboard = QApplication.clipboard()
        # clipboard.setText(modified_text.replace('\n', '\r\n'))
        clipboard.setText(original_text.replace('\n', '\r\n'))

    def sendSignalToClients(self):
        # print("send signal to Clients")
        message = "Erase"
        if self.server:
            self.server.send_message_to_client(message)
    def closeEvent(self, event):
        #애플리케이션이 종료될 때 서버를 정상적으로 종료하고 스레드 정리
        if self.server:
            self.server.stop_server()
        event.accept()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())