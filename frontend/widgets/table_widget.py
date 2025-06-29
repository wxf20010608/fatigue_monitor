from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class ResultTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "类别", "识别位置 (x-center, y-center, w, h)", "置信度", "截取的图片"])
        
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def add_result(self, result_id, category, position, confidence, image_path):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(str(result_id)))
        self.table.setItem(row_position, 1, QTableWidgetItem(category))
        self.table.setItem(row_position, 2, QTableWidgetItem(position))
        self.table.setItem(row_position, 3, QTableWidgetItem(str(confidence)))
        self.table.setItem(row_position, 4, QTableWidgetItem(image_path))

    def clear_results(self):
        self.table.setRowCount(0)