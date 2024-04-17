import errno
import socket
import threading
import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QThread
from PyQt5.QtGui import QFont, QFontDatabase

class Server(QObject):
    message_received = pyqtSignal(str)

    def __init__(self, host, port, main_widget):
        super().__init__()
        self.host = host
        self.port = port
        self.main_widget = main_widget
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sockets = [] #연결된 클라이언트 소켓을 추적하기 위한 리스트
        self.stop_flag = False

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        print("서버가 시작되었습니다.")
        print(f"서버의 IP 주소: {self.host}")
        print(f"서버의 포트 번호: {self.port}")

        self.main_widget.show_server_info(self.host, self.port)

        # while True:
        #     conn, addr = self.server_socket.accept()
        #     print('Connected by', addr)
        #     threading.Thread(target=self.handle_client, args=(conn,)).start()
        #

        while not self.stop_flag:
            print('stop flag', self.stop_flag)
            try:
                conn, addr = self.server_socket.accept()
                print('Connected by', addr)
                self.client_sockets.append(conn) #연결된 클라이언트 소켓을 리스트에 추가
                threading.Thread(target=self.handle_client, args=(conn,)).start()
            except OSError as e:
                if e.errno == errno.EINVAL:
                    #소켓이 이미 닫혔는데도 accept() 호출을 시도한 경우
                    break
                else:
                    raise

    def handle_client(self, conn):
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()
                print('수신된 데이터:', message)
                self.message_received.emit(message)

    def send_message_to_client(self, message):
        print('send message to client 함수 호출')
        if self.client_sockets:
            print('self.client_sockets는 되나 ')
            tablet_client = self.client_sockets[0]
            print('tablet client:', tablet_client)
            try:
                print('try문에 걸리나')
                tablet_client.sendall(message.encode())
                print("Message sent to tablet:", message)
            except Exception as e:
                print("Error while sending message to tablet:", e)

    def stop_server(self):
        # self.running = False
        self.stop_flag=True
        print('stop server 함수가 호출된다')
        # print('stop flag', self.stop_flag)
        # print('client sockets', self.client_sockets)
        #서버 소켓을 닫기 전에 모든 클라이언트와의 연결을 먼저 종료
        for client_socket in self.client_sockets:
            client_socket.close()
        self.client_sockets = [] #모든 클라이언트 소켓 비우기

        self.server_socket.close()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.server = None

    def initUI(self):
        self.setWindowTitle('My PyQt App')
        self.setGeometry(400, 400, 400, 400)

        # 폰트 설정
        font_id = QFontDatabase.addApplicationFont("AppleSDGothicNeoEB.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family)
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

        self.btn_copy = QPushButton('복사', self)
        self.btn_copy.setVisible(False)

        self.btn_receive = QPushButton('입력 받기', self)
        self.btn_receive.setVisible(True)

        # 수직 레이아웃 생성하여 라벨 및 버튼 추가
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.ip_label)
        v_layout.addWidget(self.port_label)
        v_layout.addWidget(self.received_message_label)
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
        # print('show received message 함수')
        #
        self.ip_label.hide()
        self.port_label.hide()

        self.received_message_label.setText(message)
        # self.received_message_label.setAlignment(Qt.AlignCenter)

        #수신된 데이터가 표시될 때만 버튼을 보이도록 설정
        # self.btn.setVisible(True)
        self.btn_copy.setVisible(True)

    def btnClicked(self):
        # print('버튼이 클릭되었습니다!')
        #클립보드에 수신된 데이터 저장
        clipboard = QApplication.clipboard()
        # clipboard.setText(self.received_message_label.text().replace('\n', '\r\n'))
        clipboard.setText(self.received_message_label.text().replace('\n', '\r\n'))
        # print('수신된 데이터가 클립보드에 저장되었습니다!')

    def sendSignalToClients(self):
        print("send signal to Clients")
        message = "change_to_number_pad_screen" #변경할 화면을 나타냄
        # server.send_message_to_client(message)
        if self.server:
            self.server.send_message_to_client(message)
    def closeEvent(self, event):
        # server.stop_server()
        # event.accept()
        # print('closeEvent 함수가 호출된다')
        #애플리케이션이 종료될 때 서버를 정상적으로 종료하고 스레드 정리
        if self.server:
            self.server.stop_server()
            server_thread.join()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()

    #통상적으로 사용되는 포트 번호 범위: 1024-49151
    random_port = random.randint(1024, 49151)

    # server = Server(socket.gethostbyname(socket.gethostname()), random_port, ex)
    # server.message_received.connect(ex.show_received_message)
    # threading.Thread(target=server.start_server).start()

    server = Server(socket.gethostbyname(socket.gethostname()), random_port, ex)
    ex.server = server
    server.message_received.connect(ex.show_received_message)
    # server.message_received.connect(lambda message: print("Received:", message))
    server_thread = threading.Thread(target=server.start_server)
    server_thread.start()

    # def close_application():
    #     server.stop_server()
    #     server_thread.join()
    #     app.quit()

    # app.aboutToQuit.connect(close_application)

    sys.exit(app.exec_())
