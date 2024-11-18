import sys
from random import randint
from cmd_ui import Ui_Form

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class AnotherWindow(QWidget, Ui_Form):
    """
    123
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def toggle_window1(self):
        self.window1 = AnotherWindow()
        if self.window1.isVisible():
            self.window1.hide()

        else:
            self.window1.show()


app = QApplication(sys.argv)
w = MainWindow()
w.toggle_window1()
w.show()
app.exec()