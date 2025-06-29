from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
import cv2

class CameraThread(QThread):
    frame_signal = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = False

    def run(self):
        cap = cv2.VideoCapture(0)
        self.running = True
        while self.running:
            ret, frame = cap.read()
            if ret:
                self.frame_signal.emit(frame)
        cap.release()

    def stop(self):
        self.running = False
        self.wait()

class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.camera_thread = None

    def initUI(self):
        self.layout = QVBoxLayout()
        self.camera_label = QLabel(self)
        self.layout.addWidget(self.camera_label)
        self.setLayout(self.layout)

    def start_camera(self):
        if self.camera_thread is not None:
            self.camera_thread.stop()
        self.camera_thread = CameraThread()
        self.camera_thread.frame_signal.connect(self.update_frame)
        self.camera_thread.start()

    def update_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.camera_label.setPixmap(QPixmap.fromImage(q_img).scaled(
            self.camera_label.size(), aspectRatioMode=1))

    def stop_camera(self):
        if self.camera_thread is not None:
            self.camera_thread.stop()
            self.camera_thread = None
        self.camera_label.clear()