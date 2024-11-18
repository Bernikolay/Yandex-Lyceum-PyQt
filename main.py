#pyuic6 Designer.ui -o main_ui.py
#pyuic6 CMDedit.ui -o cmd_ui.py
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QDialog,
                             QVBoxLayout,
                             QComboBox,
                             QInputDialog,
                             QMessageBox,
                             QPushButton,
                             QLabel,
                             QWidget)

from main_ui import Ui_MainWindow
from cmd_ui import Ui_Form

class AnotherWindow(QWidget, Ui_Form):
    """
    123
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.api_token = ""
        super().__init__()
        self.setupUi(self)
        #Buttons
        self.pushButton_5.clicked.connect(self.add_name)
        self.plus_button.clicked.connect(self.add_action)
        #self.plus_button_2.clicked.connect(self.add_action)
        self.plus_button_3.clicked.connect(self.add_action)
        self.pause_button.clicked.connect(self.pause)
        self.run_bot_button.clicked.connect(self.run_bot)

    def add_name(self):
        self.api_token, ok_pressed = QInputDialog.getText(self, "Название", "Название:........")
        if ok_pressed:
            print(self.api_token)

    def add_action(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Выбор действия")

        # Устанавливаем стиль для диалогового окна
        dialog.setStyleSheet("QInputDialog{background-color: rgb(61, 65, 89);}")

        action, ok_pressed = QInputDialog.getItem(
            dialog, "Ввод", "",
            ("Текст-Текст", "B", "C", "D"), 0, False)

        if ok_pressed:
            print(action)
            if action == "Текст-Текст":
                self.button_layout = self.scrollAreaWidgetContents_4.layout()
                new_button = QPushButton(f"/команда {self.button_layout.count() - 2}", self)
                new_button.setSizePolicy(
                    QtWidgets.QSizePolicy.Policy.Minimum,
                    QtWidgets.QSizePolicy.Policy.Maximum
                )
                new_button.setMinimumSize(500, 60)

                new_button.setStyleSheet("QPushButton"
                                         "{"
                                         "border-radius: 20px;"
                                         "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1,"
                                         " y2:0, stop:0 rgba(96, 86, 255, 255), stop:1 "
                                         "rgba(179, 146, 221, 255));"
                                         'font: 36pt "Oceanwide QLt";'
                                         "color: rgb(255, 255, 255);"
                                         "}")

                # Подключаем сигнал clicked к слоту print_one
                new_button.clicked.connect(self.edit_cmd)

                # Определяем позицию для вставки
                mid_index = self.button_layout.count() - 1

                # Вставляем кнопку
                self.button_layout.insertWidget(mid_index, new_button)

    def print_one(self):
        print(1)

    def edit_cmd(self):
        self.window1 = AnotherWindow()
        if self.window1.isVisible():
            self.window1.hide()
        else:
            self.window1.show()


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
