import sys
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QThread

class UdpListener(QThread):
    """Background thread to listen for UDP packets and emit signals with the received data."""
    data_received = pyqtSignal(int)

    def __init__(self, host='172.31.253.194', port=12345):
        super().__init__()
        self.host = host
        self.port = port
        self.running = True

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.host, self.port))
        sock.settimeout(1.0)

        while self.running:
            try:
                data, addr = sock.recvfrom(1024)
                val_str = data.decode('utf-8').strip()
                val = int(float(val_str))
                val = max(0, min(255, val))
                self.data_received.emit(val)
                print(f"Received data: {data} from {addr}")
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error receiving data: {e}")
        sock.close()

    def stop(self):
        self.running = False
        self.wait()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Plot Receiver")
        self.setGeometry(100, 100, 800, 600)

        self.widgetContainer = QWidget()
        self.setCentralWidget(self.widgetContainer)
        mainLayout = QVBoxLayout(self.widgetContainer)

        self.label = QLabel("Waiting for Telemetry...", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: red; padding: 10px;")
        mainLayout.addWidget(self.label)

    def update_display(self, val):
        self.label.setText(f"Received Red Intensity: {val}")
        self.label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: rgb({val}, 0, 0); padding: 10px;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    window.raise_()
    window.activateWindow()

    # Instantiate and start the background UDP listener thread
    listener = UdpListener()
    listener.data_received.connect(window.update_display)
    listener.start()

    exit_code = app.exec_()
    listener.stop()
    sys.exit(exit_code)