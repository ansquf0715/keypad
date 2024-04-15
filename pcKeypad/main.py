import socket
import threading
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal, QObject

class Server(QObject):
    message_received = pyqtSignal(str)

    def __init__(self, host, port, main_widget):
        super().__init__()
        self.host = host
        self.port = port
        self.main_widget = main_widget
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        print("서버가 시작되었습니다.")
        print(f"서버의 IP 주소: {self.host}")
        print(f"서버의 포트 번호: {self.port}")

        self.main_widget.show_server_info(self.host, self.port)

        while True:
            conn, addr = self.server_socket.accept()
            print('Connected by', addr)
            threading.Thread(target=self.handle_client, args=(conn,)).start()

    def handle_client(self, conn):
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()
                print('수신된 데이터:', message)
                self.message_received.emit(message)

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('My PyQt App')
        self.setGeometry(400, 400, 400, 400)

        self.server_info_label = QLabel(self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.server_info_label)

        self.btn = QPushButton('클릭하세요', self)
        self.layout.addWidget(self.btn)

        self.setLayout(self.layout)

        self.btn.clicked.connect(self.btnClicked)

    def show_server_info(self, host, port):
        self.server_info_label.setText(f"서버의 IP 주소: {host}\n서버의 포트 번호: {port}")

    def show_received_message(self, message):
        self.server_info_label.setText(message)

    def btnClicked(self):
        print('버튼이 클릭되었습니다!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()

    server = Server(socket.gethostbyname(socket.gethostname()), 65432, ex)
    server.message_received.connect(ex.show_received_message)
    threading.Thread(target=server.start_server).start()

    sys.exit(app.exec_())
