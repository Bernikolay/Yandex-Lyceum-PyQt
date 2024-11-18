#pyuic6 Designer.ui -o main_ui.py
#pyuic6 CMDedit.ui -o cmd_ui.py
#pyuic6 CMD_start_edit.ui -o cmd_start_ui.py
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
from cmd_start_ui import Ui_Form as Ui_Form_start

class CMDStartEdit(QWidget, Ui_Form_start):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.image = False
        self.ok_button_start.clicked.connect(self.get_text)
        self.checkBox_2.stateChanged.connect(self.on_checkbox_changed)

    def get_text(self):
        #lineEdit
        text = self.lineEdit_2.text()
        print(text)

    def on_checkbox_changed(self):
        self.image = not self.image
        if self.image:
            self.img_msg()
        else:
            self.lineEdit_2.setText("")

    def img_msg(self):
        self.lineEdit_2.setText("Укажите путь к картинке!")


class AnotherWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.image = False
        self.ok_button.clicked.connect(self.get_text)
        self.checkBox_output_image.stateChanged.connect(self.on_checkbox_changed)

    def get_text(self):
        # lineEdit
        text = self.lineEditInput.text()
        text_output = self.lineEditOutput.text()
        print(text)
        print(text_output)

    def on_checkbox_changed(self):
        self.image = not self.image
        if self.image:
            self.img_msg()
        else:
            self.lineEditOutput.setText("")

    def img_msg(self):
        self.lineEditOutput.setText("Укажите путь к картинке!")

class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.bot_name = ""
        super().__init__()
        self.setupUi(self)
        #Buttons
        self.pushButton_5.clicked.connect(self.add_name)
        self.plus_button.clicked.connect(self.add_action)
        #self.plus_button_2.clicked.connect(self.add_action)
        self.plus_button_3.clicked.connect(self.add_action)
        self.pause_button.clicked.connect(self.pause)
        self.run_bot_button.clicked.connect(self.run_bot)
        self.welcome_message_button.clicked.connect(self.edit_cmd_start)

    def add_name(self):
        self.bot_name, ok_pressed = QInputDialog.getText(self, "Название", "Название:........")
        if ok_pressed:
            print(self.bot_name)

    def add_action(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Выбор действия")

        # Устанавливаем стиль для диалогового окна
        dialog.setStyleSheet("QInputDialog{background-color: rgb(61, 65, 89);}")

        action, ok_pressed = QInputDialog.getItem(
            dialog, "Ввод", "",
            ("Стандартная команда", "2",), 0, False)

        if ok_pressed:
            print(action)
            if action == "Стандартная команда":
                self.button_layout = self.scrollAreaWidgetContents_4.layout()
                new_button = QPushButton(f"/команда {self.button_layout.count() - 1}", self)
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

    def edit_cmd_start(self):
        self.window1 = CMDStartEdit()
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
