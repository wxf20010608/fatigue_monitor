from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QFileDialog, QSizePolicy, QHeaderView, QCalendarWidget, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QPixmap, QImage, QPainter
import cv2
import requests
import json
import numpy as np
import subprocess
import os
import sys
import socket

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("疲劳监测系统")
        self.resize(1000, 700)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5; /* Light gray background for the main window */
            }
            QPushButton {
                background-color: #4CAF50; /* Green */
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
            QTableWidget {
                border: 1px solid #ddd; /* Light border for table */
                border-radius: 5px;
                gridline-color: #eee;
                background-color: rgba(255, 255, 255, 0.8); /* Slightly transparent background for table */
                selection-background-color: #a8d7ff;
            }
            QTableWidget QHeaderView::section {
                background-color: #e0e0e0;
                padding: 5px;
                border: 1px solid #ccc;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
            /* General font for the whole app */
            * {
                font-family: "Segoe UI", sans-serif; /* A common, clean font */
            }
        """);

        # 左侧按钮区
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignTop)

        self.btn_open_img = QPushButton("打开图片")
        self.btn_open_cam = QPushButton("打开摄像头")
        self.btn_start = QPushButton("开始识别")
        self.btn_save_results = QPushButton("保存当前结果")
        self.btn_clear = QPushButton("清空历史记录")
        self.btn_exit = QPushButton("退出系统")
        self.btn_face_recognition = QPushButton("切换至人脸识别系统")

        for btn in [self.btn_open_img, self.btn_open_cam, self.btn_start, self.btn_save_results, self.btn_clear, self.btn_exit, self.btn_face_recognition]:
            btn.setMinimumHeight(40)
            left_layout.addWidget(btn)
            left_layout.addSpacing(10)
        left_layout.addStretch()

        # Add calendar widget above the clock
        self.calendar_widget = QCalendarWidget(self)
        self.calendar_widget.setStyleSheet("""
            QCalendarWidget {
                background-color: rgba(255, 255, 255, 0.1); /* Semi-transparent white */
                border: 1px solid #555;
                border-radius: 5px;
                color: white;
                font-size: 14px;
            }
            QCalendarWidget QAbstractItemView {
                selection-background-color: #007bff; /* Highlight color */
                selection-color: white;
            }
            QCalendarWidget QToolButton {
                color: white;
                background-color: transparent;
                font-size: 16px;
            }
            QCalendarWidget QMenu {
                background-color: #333;
                color: white;
            }
            QCalendarWidget QSpinBox {
                color: white;
                background-color: transparent;
            }
        """)
        left_layout.addWidget(self.calendar_widget)

        # Clock container widget
        self.clock_container_widget = QWidget(self)
        self.clock_container_layout = QHBoxLayout(self.clock_container_widget)
        self.clock_container_layout.setContentsMargins(0, 0, 0, 0) # Remove contents margins
        self.clock_container_widget.setStyleSheet("""
            QWidget {
                background-color: transparent; /* Make background transparent */
                border-radius: 8px; /* Match button border-radius */
            }
            QLabel {
                color: white; /* Changed to white for better visibility */
                font-size: 30px; /* Increased font size for clock */
                font-weight: bold;
            }
        """);

        self.alarm_icon_label = QLabel(self.clock_container_widget)
        alarm_pixmap = QPixmap("D:/AI_Learning/python/01_Learning/Target_Detection/fatigue_monitor_update/frontend/resources/时钟.png") # Updated path to alarm clock icon
        if not alarm_pixmap.isNull():
            self.alarm_icon_label.setPixmap(alarm_pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)) # Scale for visibility
        self.alarm_icon_label.setFixedSize(30, 30) 
        self.clock_container_layout.addWidget(self.alarm_icon_label)
        self.clock_container_layout.addSpacing(5) # Add a small space between icon and time

        self.clock_label = QLabel(self.clock_container_widget)
        self.clock_container_layout.addWidget(self.clock_label)
        self.clock_container_layout.addStretch() # Make the clock container fit its content width

        left_layout.addWidget(self.clock_container_widget) # Add clock container below calendar

        # Timer for updating the clock
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)
        self.update_clock()

        main_layout.addWidget(left_widget, 1)

        # 右侧区域（摄像头+表格）
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        self.camera_label = QLabel("摄像头区域")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("background-color: rgba(50, 50, 50, 0.7); color: #333; border: 2px solid #ccc; border-radius: 5px;")
        self.camera_label.setFixedSize(640, 360)
        right_layout.addWidget(self.camera_label, 4) # Vertical stretch for camera (4 parts)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["ID", "类别", "识别位置 (x, y, w, h)", "置信度", "截取的图片", "时间"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        right_layout.addWidget(self.table, 1) # Vertical stretch for table (1 part)

        right_widget.setFixedWidth(self.camera_label.width() + right_layout.contentsMargins().left() + right_layout.contentsMargins().right())

        main_layout.addWidget(right_widget, 0) 
        # 绑定按钮事件
        self.btn_open_img.clicked.connect(self.open_image)
        self.btn_open_cam.clicked.connect(self.open_camera)
        self.btn_start.clicked.connect(self.start_detection_mode)
        self.btn_save_results.clicked.connect(self.manual_save_results)
        self.btn_clear.clicked.connect(self.clear_history)
        self.btn_exit.clicked.connect(self.close)
        self.btn_face_recognition.clicked.connect(self.switch_to_face_recognition_system)

        # 摄像头相关
        self.cap = None
        self.display_timer = QTimer()
        self.display_timer.timeout.connect(self.update_camera_display)
        self.detection_timer = QTimer()
        self.detection_timer.timeout.connect(self.perform_detection_on_frame)
        self.current_frame = None
        self.image_path = None
        self.detection_results = []
        # 存储实时检测过程中的所有结果，只在关闭摄像头时保存
        self.temp_detection_results = []

        self.background_pixmap = QPixmap("D:/AI_Learning/python/01_Learning/Target_Detection/fatigue_monitor_update/frontend/resources/image.png")

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.background_pixmap.isNull():
            scaled_pixmap = self.background_pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(self.rect().topLeft(), scaled_pixmap)
        super().paintEvent(event)

    def update_clock(self):
        current_time = QDateTime.currentDateTime().toString("hh:mm:ss")
        self.clock_label.setText(current_time)

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image_path = file_path
            image = cv2.imread(file_path)
            self.current_frame = image
            self.display_image(image)
            # 不再自动进行检测，改为手动点击"开始识别"
            # self.start_detection()

    def open_camera(self):
        if self.cap is not None and self.cap.isOpened():
            # 已开启，关闭摄像头和所有定时器
            self.display_timer.stop()
            self.detection_timer.stop()
            self.cap.release()
            self.cap = None
            self.btn_open_cam.setText("打开摄像头")
            self.detection_results = []
            
            # 不再自动保存结果，由"开始识别"按钮控制检测和结果的保存
            # if self.temp_detection_results:
            #     self.save_current_detection_results()
            #     self.temp_detection_results = []  # 清空临时结果
            
            self.update_camera_display()
            self.camera_label.setStyleSheet("background-color: rgba(50, 50, 50, 0.7); color: #333; border: 2px solid #ccc; border-radius: 5px;")
        else:
            # 未开启，打开摄像头
            self.camera_label.setText("正在尝试打开摄像头...")
            print("Attempting to open camera...") 
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.camera_label.setText("无法打开摄像头！请检查摄像头连接或权限。") # More informative message
                print("Error: Could not open camera.") # Debug print
                self.camera_label.setStyleSheet("background-color: rgba(50, 50, 50, 0.7); color: #333; border: 2px solid #ccc; border-radius: 5px;")
                return
            print("Camera opened successfully. Starting display timer.") # Debug print
            self.display_timer.start(30)
            self.btn_open_cam.setText("关闭摄像头")
            # 清空临时检测结果，检测由"开始识别"按钮控制
            self.temp_detection_results = []
            # Set camera label to grey semi-transparent when active
            self.camera_label.setStyleSheet("background-color: rgba(128, 128, 128, 0.5); color: white; border: 2px solid #ccc; border-radius: 5px;")

    def update_camera_display(self):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Style already set in open_camera when active, no need to repeat here
                self.current_frame = frame.copy()
                display_frame = frame.copy()
                for item in self.detection_results:
                    x, y, w, h = map(int, item.get("bbox", [0,0,0,0]))
                    label = item.get("label", "")
                    conf = item.get("confidence", 0)
                    cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0,255,0), 2)
                    cv2.putText(display_frame, f"{label} {conf:.2f}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                self.display_image(display_frame)
            else:
                # If frame not read, release cap and stop display timer, set to white semi-transparent
                print("Warning: Could not read frame from camera. Releasing camera.") # Debug print
                self.display_timer.stop()
                self.cap.release()
                self.cap = None
                self.camera_label.setText("摄像头已断开")
                self.btn_open_cam.setText("打开摄像头")
                self.camera_label.setStyleSheet("background-color: rgba(50, 50, 50, 0.7); color: #333; border: 2px solid #ccc; border-radius: 5px;") # Set to dark grey semi-transparent on disconnect
        else:
            self.camera_label.clear()
            self.camera_label.setText("摄像头区域")
            # Apply inactive style for camera_label when initially empty or disconnected
            self.camera_label.setStyleSheet("background-color: rgba(50, 50, 50, 0.7); color: #333; border: 2px solid #ccc; border-radius: 5px;")

    def start_detection_mode(self):
        if self.btn_start.text() == "开始识别":
            # Start detection
            if self.cap is not None and self.cap.isOpened():
                self.detection_timer.start(150)
                self.camera_label.setText("正在实时识别...")
                self.btn_start.setText("停止识别")
            elif self.current_frame is not None: # Image is loaded
                self.detection_timer.stop() # Ensure timer is stopped for one-time detection
                print("Starting detection on uploaded image...")
                self.start_detection() # Perform one-time detection and save
                # self.camera_label.setText("图片识别完成！") # Removed: Avoids clearing image
                # For image, we don't change button text to stop, as it's a one-time operation
            else:
                self.camera_label.setText("请先打开图片或摄像头")
        else: # Button text is "停止识别"
            # Stop detection
            if self.cap is not None and self.cap.isOpened():
                self.detection_timer.stop()
                self.camera_label.setText("摄像头已暂停识别。")
                self.btn_start.setText("开始识别")
            # If it's an image, the button text won't be "停止识别", so this else is for camera only

    def perform_detection_on_frame(self):
        if self.current_frame is not None:
            _, img_encoded = cv2.imencode('.jpg', self.current_frame)
            files = {'file': ('image.jpg', img_encoded.tobytes(), 'image/jpeg')}
            try:
                resp = requests.post("http://127.0.0.1:8000/detect", files=files, timeout=5)
                if resp.status_code == 200:
                    new_results = resp.json().get("results", [])
                    # 更新当前检测结果用于显示边框
                    self.detection_results = new_results
                    # 保存到临时变量，等待手动保存
                    self.temp_detection_results = new_results.copy() if new_results else []
                    # 直接将结果添加到表格
                    # if new_results:
                    #     self.show_results(new_results)
                else:
                    print(f"Detection API error: {resp.status_code}")
                    self.detection_results = []
            except requests.exceptions.Timeout:
                print("Detection API call timed out.")
                self.detection_results = []
            except Exception as e:
                print(f"Error during detection API call: {e}")
                self.detection_results = []

    def display_image(self, img):
        try:
            print(f"Displaying image with shape: {img.shape}")  # Debug print
            rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_img = QImage(rgb_image.data.tobytes(), w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_img)
            # 获取QLabel当前大小，自适应缩放
            label_size = self.camera_label.size()
            scaled_pixmap = pixmap.scaled(label_size, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.camera_label.setPixmap(scaled_pixmap)
            print(f"Image displayed successfully, label size: {label_size}")  # Debug print
        except Exception as e:
            print(f"Error displaying image: {e}")  # Debug print
            self.camera_label.setText(f"图片显示错误: {e}")

    def resizeEvent(self, event):
        # 窗口大小变化时，刷新摄像头画面
        if self.current_frame is not None and self.cap is not None and self.cap.isOpened():
             self.display_image(self.current_frame)
        elif self.current_frame is not None: 
            self.display_image(self.current_frame) 
        super().resizeEvent(event)

    def check_backend_connection(self):
        """检查后端连接状态"""
        try:
            resp = requests.get("http://127.0.0.1:8000/", timeout=3)
            return resp.status_code == 200
        except:
            return False

    def start_detection(self):
        if self.current_frame is None:
            self.camera_label.setText("请先打开图片或摄像头")
            return

        # 检查后端连接
        if not self.check_backend_connection():
            print("Backend not available")  # Debug print
            self.camera_label.setText("后端服务未启动，请先启动后端服务")
            return

        print(f"Starting detection on image with shape: {self.current_frame.shape}")  # Debug print

        # 将当前帧转为jpg并发送到后端
        _, img_encoded = cv2.imencode('.jpg', self.current_frame)
        files = {'file': ('image.jpg', img_encoded.tobytes(), 'image/jpeg')}
        try:
            resp = requests.post("http://127.0.0.1:8000/detect", files=files, timeout=5)
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                print(f"Detection results: {results}")  # Debug print
                
                # 在图片上画框
                frame_with_boxes = self.current_frame.copy()
                for item in results:
                    x, y, w, h = map(int, item.get("bbox", [0,0,0,0]))
                    label = item.get("label", "")
                    conf = item.get("confidence", 0)
                    cv2.rectangle(frame_with_boxes, (x, y), (x+w, y+h), (0,255,0), 2)
                    cv2.putText(frame_with_boxes, f"{label} {conf:.2f}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                
                # 更新当前帧为带框的图片，并显示
                self.current_frame = frame_with_boxes
                print("Displaying image with detection boxes...")  # Debug print
                self.display_image(frame_with_boxes)
                # 直接将结果保存到表格
                # if results:
                #     self.show_results(results)
                # 保存到临时变量，等待手动保存
                self.temp_detection_results = results.copy() if results else []
            else:
                print(f"Detection API error: {resp.status_code}")  # Debug print
                self.camera_label.setText(f"识别失败，后端返回错误: {resp.status_code}")
        except requests.exceptions.Timeout:
            print("Detection API timeout")  # Debug print
            self.camera_label.setText("识别失败: 后端请求超时")
        except Exception as e:
            print(f"Detection error: {e}")  # Debug print
            self.camera_label.setText(f"识别失败: {e}")

    def show_results(self, results):
        # 获取当前时间作为时间戳
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        
        # 获取当前表格行数作为起始索引
        start_row = self.table.rowCount()
        
        for idx, item in enumerate(results):
            # 为每个检测结果添加时间戳
            item["timestamp"] = current_time
            
            # 在表格末尾添加新行
            row_idx = start_row + idx
            self.table.insertRow(row_idx)
            
            # 设置ID（使用全局递增的ID）
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_idx + 1)))
            
            # 设置类别
            self.table.setItem(row_idx, 1, QTableWidgetItem(item.get("label", "")))
            
            # 设置识别位置
            bbox = item.get("bbox", [0, 0, 0, 0])
            self.table.setItem(row_idx, 2, QTableWidgetItem(f"{bbox[0]:.2f}, {bbox[1]:.2f}, {bbox[2]:.2f}, {bbox[3]:.2f}"))
            
            # 设置置信度
            self.table.setItem(row_idx, 3, QTableWidgetItem(f"{item.get('confidence', 0):.2f}"))
            
            # 截取图片
            if self.current_frame is not None:
                x, y, w, h = map(int, bbox)
                crop = self.current_frame[y:y+h, x:x+w]
                if crop.size > 0:
                    rgb_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
                    h2, w2, ch2 = rgb_crop.shape
                    qt_crop = QImage(rgb_crop.data.tobytes(), w2, h2, ch2 * w2, QImage.Format_RGB888)
                    pixmap_crop = QPixmap.fromImage(qt_crop).scaled(60, 40, Qt.AspectRatioMode.KeepAspectRatio)
                    label = QLabel()
                    label.setPixmap(pixmap_crop)
                    self.table.setCellWidget(row_idx, 4, label)
            
            # 设置时间戳
            self.table.setItem(row_idx, 5, QTableWidgetItem(current_time))

    def clear_history(self):
        self.table.setRowCount(0)
        # 不清空摄像头画面和 current_frame

    def closeEvent(self, event):
        # 关闭摄像头时保存所有临时检测结果
        if self.temp_detection_results:
            self.save_current_detection_results()
            self.temp_detection_results = []  # Clear temporary results
            
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        event.accept()

    def switch_to_face_recognition_system(self):
        QMessageBox.information(self, "系统切换", "正在尝试切换至人脸识别系统...")
        
        # 1. 停止当前疲劳监测系统的摄像头和定时器
        if self.cap is not None and self.cap.isOpened():
            self.display_timer.stop()
            self.detection_timer.stop()
            self.cap.release()
            self.cap = None

        # 2. 关闭当前窗口
        self.close()

        # Helper function to check if a port is in use
        def is_port_in_use(port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                return s.connect_ex(("127.0.0.1", port)) == 0

        # 计算项目根目录路径 - 移到条件块外面
        current_file_dir = os.path.dirname(os.path.abspath(__file__))  # fatigue_monitor_update/frontend/ui
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_dir)))  # Target_Detection
        
        print(f"当前文件目录: {current_file_dir}")
        print(f"项目根目录: {project_root}")

        # 3. 启动人脸识别系统的后端服务 (face_recoginition_myself/main.py)
        face_backend_port = 8002
        if not is_port_in_use(face_backend_port):
            face_backend_path = os.path.join(project_root, "face_recoginition_myself", "main.py")
            
            print(f"人脸识别后端路径: {face_backend_path}")
            
            # 检查文件是否存在
            if not os.path.exists(face_backend_path):
                print(f"错误：找不到人脸识别后端文件: {face_backend_path}")
                return
            
            # Define log file paths for the backend
            face_output_log = os.path.join(project_root, "face_backend_output.log")
            face_error_log = os.path.join(project_root, "face_backend_error.log")

            try:
                print(f"正在启动人脸识别后端: {face_backend_path}")
                with open(face_output_log, "w") as fout, open(face_error_log, "w") as ferr:
                    subprocess.Popen([sys.executable, face_backend_path], 
                                     creationflags=subprocess.DETACHED_PROCESS,
                                     stdout=fout, # Redirect stdout to file
                                     stderr=ferr  # Redirect stderr to file
                                     )
                print(f"人脸识别后端启动命令已执行，输出到 {face_output_log} 和 {face_error_log}")
            except Exception as e:
                print(f"启动人脸识别后端失败: {e}")
        else:
            print(f"人脸识别后端 (端口 {face_backend_port}) 已经在运行，跳过启动。")

        # 4. 启动人脸识别系统的前端应用程序 (face_recoginition_myself/app.py)
        face_frontend_path = os.path.join(project_root, "face_recoginition_myself", "app.py")
        print(f"人脸识别前端路径: {face_frontend_path}")
        
        # 检查文件是否存在
        if not os.path.exists(face_frontend_path):
            print(f"错误：找不到人脸识别前端文件: {face_frontend_path}")
            return
            
        try:
            print(f"正在启动人脸识别前端: {face_frontend_path}")
            subprocess.Popen([sys.executable, face_frontend_path]) # Removed DETACHED_PROCESS and DEVNULL for debugging
            print(f"人脸识别前端已启动: {face_frontend_path}")
        except Exception as e:
            print(f"启动人脸识别前端失败: {e}")

    def manual_save_results(self):
        """手动保存当前检测结果到表格"""
        if not self.temp_detection_results:
            QMessageBox.information(self, "提示", "当前没有检测结果可保存")
            return
            
        # 保存当前检测结果
        result_count = len(self.temp_detection_results)
        # Use show_results to add to the table
        self.show_results(self.temp_detection_results)
        self.temp_detection_results = []  # Clear temporary results after saving
        QMessageBox.information(self, "成功", f"已保存 {result_count} 个检测结果到表格")

    # Re-added the save_current_detection_results functionality for clarity, though manual_save_results will now call show_results directly
    def save_current_detection_results(self):
        """保存当前检测结果到表格（累积保存）"""
        if not self.temp_detection_results:
            return
            
        # 获取当前时间作为时间戳（每次关闭摄像头的时间）
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        
        # 获取当前表格行数作为起始索引
        start_row = self.table.rowCount()
        
        for idx, item in enumerate(self.temp_detection_results):
            # 为每个检测结果添加时间戳（使用关闭摄像头的时间）
            item["timestamp"] = current_time
            
            # 在表格末尾添加新行（累积保存）
            row_idx = start_row + idx
            self.table.insertRow(row_idx)
            
            # 设置ID（使用全局递增的ID）
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_idx + 1)))
            
            # 设置类别
            self.table.setItem(row_idx, 1, QTableWidgetItem(item.get("label", "")))
            
            # 设置识别位置
            bbox = item.get("bbox", [0, 0, 0, 0])
            self.table.setItem(row_idx, 2, QTableWidgetItem(f"{bbox[0]:.2f}, {bbox[1]:.2f}, {bbox[2]:.2f}, {bbox[3]:.2f}"))
            
            # 设置置信度
            self.table.setItem(row_idx, 3, QTableWidgetItem(f"{item.get('confidence', 0):.2f}"))
            
            # 截取图片（这里使用最后一次的current_frame）
            if self.current_frame is not None:
                x, y, w, h = map(int, bbox)
                crop = self.current_frame[y:y+h, x:x+w]
                if crop.size > 0:
                    rgb_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
                    h2, w2, ch2 = rgb_crop.shape
                    qt_crop = QImage(rgb_crop.data.tobytes(), w2, h2, ch2 * w2, QImage.Format_RGB888)
                    pixmap_crop = QPixmap.fromImage(qt_crop).scaled(60, 40, Qt.AspectRatioMode.KeepAspectRatio)
                    label = QLabel()
                    label.setPixmap(pixmap_crop)
                    self.table.setCellWidget(row_idx, 4, label)
            
            # 设置时间戳（显示关闭摄像头的时间）
            self.table.setItem(row_idx, 5, QTableWidgetItem(current_time))