import errno
import socket
import threading
import sys
import serial #pySerial 라이브러리 추가
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtGui import QFont, QFontDatabase

class Server(QObject):
    message_received = pyqtSignal(str)

    def __init__(self, host, port, main_widget):
        super().__init__()
        # self.host = host
        self.port = port
        self.main_widget = main_widget
        self.serial_port = serial.Serial(str(port), 9600) #시리얼 포트 설정
        # self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client_sockets = [] #연결된 클라이언트 소켓을 추적하기 위한 리스트
        self.stop_flag = False
        self.lock = threading.Lock()

    def start_server(self):
        # 시리얼 포트가 열렸는지 확인
        if not self.serial_port.is_open:
            print("Serial port is not open.")
            return

        while not self.stop_flag:
            try:
                data = self.serial_port.readline().decode().strip()  # 데이터 수신
                if data:
                    print("Received:", data)
                    self.message_received.emit(data)  # 수신된 데이터를 PyQt 애플리케이션에 전달
            except Exception as e:
                print("Error while receiving data:", e)

    # def start_server(self):
    #     self.server_socket.bind((self.host, self.port))
    #     self.server_socket.listen()
    #
    #     # print("서버가 시작되었습니다.")
    #     # print(f"서버의 IP 주소: {self.host}")
    #     # print(f"서버의 포트 번호: {self.port}")
    #
    #     self.main_widget.show_server_info(self.host, self.port)
    #
    #     while not self.stop_flag:
    #         # print('stop flag', self.stop_flag)
    #         try:
    #             conn, addr = self.server_socket.accept()
    #             print('Connected by', addr)
    #             self.client_sockets.append(conn) #연결된 클라이언트 소켓을 리스트에 추가
    #             threading.Thread(target=self.handle_client, args=(conn,)).start()
    #         except OSError as e:
    #             if e.errno == errno.EINVAL:
    #                 #소켓이 이미 닫혔는데도 accept() 호출을 시도한 경우
    #                 break
    #             else:
    #                 raise

    # def handle_client(self, conn):
    #     with conn:
    #         while True:
    #             data = conn.recv(1024)
    #             if not data:
    #                 break
    #             message = data.decode()
    #             # print('수신된 데이터:', message)
    #             self.message_received.emit(message)

    # def send_message_to_client(self, message):
    #     if self.client_sockets:
    #         tablet_client = self.client_sockets[0]
    #         try:
    #             tablet_client.sendall(message.encode())
    #             # print("Message sent to tablet:", message)
    #         except Exception as e:
    #             print("Error while sending message to tablet:", e)

    # def send_message_to_client(self, message):
    #     with self.lock:
    #         for client_socket in self.client_sockets:
    #             try:
    #                 client_socket.sendall(message.encode())
    #             except Exception as e:
    #                 print("Error while sending message to client:", e)

    def send_message_to_client(self, message):
        # 데이터를 시리얼 포트를 통해 클라이언트에 전송
        try:
            self.serial_port.write(message.encode())
        except Exception as e:
            print("Error while sending message to client:", e)

    # def stop_server(self):
    #     self.stop_flag=True
    #     # print('stop flag', self.stop_flag)
    #     # print('client sockets', self.client_sockets)
    #
    #     # #서버 소켓을 닫기 전에 모든 클라이언트와의 연결을 먼저 종료
    #     # for client_socket in self.client_sockets:
    #     #     client_socket.close()
    #     # self.client_sockets = [] #모든 클라이언트 소켓 비우기
    #
    #     with self.lock:
    #         # 서버 소켓을 닫기 전에 모든 클라이언트와의 연결을 먼저 종료
    #         for client_socket in self.client_sockets:
    #             client_socket.close()
    #         self.client_sockets = []  # 모든 클라이언트 소켓 비우기
    #
    #     self.server_socket.close()

    def stop_server(self):
        self.stop_flag = True
        if self.serial_port.is_open:
            self.serial_port.close()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.server = None

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
        modified_text = original_text[:3]+original_text[4:8]+original_text[9:]

        #클립보드에 수신된 데이터 저장
        clipboard = QApplication.clipboard()
        clipboard.setText(modified_text.replace('\n', '\r\n'))

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

    #통상적으로 사용되는 포트 번호 범위: 1024-49151
    # random_port = random.randint(1024, 49151)
    random_port = 65432

    server = Server(socket.gethostbyname(socket.gethostname()), random_port, ex)
    ex.server = server
    server.message_received.connect(ex.show_received_message)
    server_thread = threading.Thread(target=server.start_server)
    server_thread.start()

    sys.exit(app.exec_())
