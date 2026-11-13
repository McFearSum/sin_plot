import os
import sys
import socket
from PyQt5 import QtCore
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QGuiApplication


# Required for the plot to update in real-time
# os.environ["QT_QPA_PLATFORM"] = "offscreen"

class udpListener(QtCore.QThread):
    """Background thread to listen for UDP packets and emit signals with the received data."""
    def __init__(self, host='172.31.253.194', port=12345):
        super().__init__()
        self.host = host
        self.port = port
        self.running = True

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.host, self.port))
        sock.settimeout(1.0)  # Set a timeout for the socket

        while self.running:
            try:
                data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
                val_str = data.decode('utf-8').strip()
                val = int(float(val_str))  # Convert to float and then to int
                val = max(0, min(255, val))  # Clamp the value between 0 and 255
                self.data_received.emit(val)  # Emit the signal with the received value
                print(f"Received data: {data} from {addr}")

                # Here you can emit a signal with the received data if needed
            except socket.timeout:
                continue  # Continue listening for new packets
            except Exception as e:
                print(f"Error receiving data: {e}")
        sock.close()

    def stop(self):
        self.running = False
        self.wait()  # Wait for the thread to finish

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Plot Receiver")
        self.setGeometry(100, 100, 800, 600)

        # Create a plot widget
        self.widgetContainer = QWidget()
        self.setCentralWidget(self.widgetContainer)
        mainLayout = QVBoxLayout(self.widgetContainer)

        self.label = QLabel("Data Plot Receiver", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: red; padding: 10ps;")
        mainLayout.addWidget(self.label)

        circleLayout = QHBoxLayout()
        mainLayout.addLayout(circleLayout)





if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

