from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class ButtonPanel(QWidget):
    def __init__(self, parent=None):
        super(ButtonPanel, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create buttons
        self.open_image_button = QPushButton("打开图片")
        self.open_camera_button = QPushButton("打开摄像头")
        self.start_recognition_button = QPushButton("开始识别")
        self.clear_history_button = QPushButton("清空历史记录")
        self.exit_button = QPushButton("退出系统")

        # Add buttons to layout
        layout.addWidget(self.open_image_button)
        layout.addWidget(self.open_camera_button)
        layout.addWidget(self.start_recognition_button)
        layout.addWidget(self.clear_history_button)
        layout.addWidget(self.exit_button)

        # Set layout to the widget
        self.setLayout(layout)