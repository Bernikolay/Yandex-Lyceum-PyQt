#pyuic6 Designer.ui -o window2.py
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow,
                             QInputDialog, QMessageBox, QPushButton)

from window2 import Ui_MainWindow

class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.api_token = ""
        super().__init__()
        self.setupUi(self)
        #Buttons
        self.pushButton_5.clicked.connect(self.add_api_token)
        self.plus_button.clicked.connect(self.add_action)
        #self.plus_button_2.clicked.connect(self.add_action)
        self.plus_button_3.clicked.connect(self.add_action)
        self.pause_button.clicked.connect(self.pause)
        self.run_bot_button.clicked.connect(self.run_bot)

    def add_api_token(self):
        self.api_token, ok_pressed = QInputDialog.getText(self, "Token", "Ваш токен:........")
        if ok_pressed:
            print(self.api_token)

    def add_action(self):
        action, ok_pressed = QInputDialog.getItem(
            self, "Ввод", "Выбор действия:",
            ("Текст-Текст", "B", "C", "D"), 0, False)
        if ok_pressed:
            print(action)
        if action == "Текст-Текст":
            self.button_layout = self.scrollAreaWidgetContents_4.layout()
            new_button = QPushButton(f"Button {self.button_layout.count() + 1}", self)
            new_button.setStyleSheet("QPushButton"
                                    "{"
	                                    "border-radius: 70px;"
	                                    "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1,"
                                        " y2:0, stop:0 rgba(96, 86, 255, 255), stop:1 "
                                        "rgba(179, 146, 221, 255));"
	                                    'font: 63 56pt "Oceanwide QLt";'
	                                    "color: rgb(255, 255, 255);"
                                     "}")
            self.button_layout.addWidget(new_button)


    def pause(self):
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Пауза")
        self.msg.setText("Бот остановлен.")
        self.msg.exec()

    def run_bot(self):
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Запуск")
        self.msg.setText("Бот работает.")
        self.msg.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
