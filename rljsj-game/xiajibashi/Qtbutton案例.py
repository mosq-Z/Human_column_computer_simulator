from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QPushButton 示例")
        self.setGeometry(100, 100, 300, 200)

        # 1. 创建按钮
        self.btn = QPushButton("点击我", self)
        self.btn.setGeometry(100, 80, 100, 30)  # 位置与大小

        # 2. 绑定点击事件（关键：传递函数引用，不要加 ()）
        self.btn.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        print("按钮被点击了！")

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()