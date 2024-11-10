import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QScrollArea, QFrame, QHBoxLayout

class ScrollAreaExample(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QScrollArea Example")
        self.resize(300, 200)

        # Создаем основной вертикальный layout
        main_layout = QVBoxLayout(self)

        # Создаем QScrollArea
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Создаем контейнер для кнопок
        self.button_container = QFrame()
        self.button_layout = QVBoxLayout(self.button_container)

        # Устанавливаем контейнер в QScrollArea
        self.scroll_area.setWidget(self.button_container)

        # Добавляем QScrollArea в основной layout
        main_layout.addWidget(self.scroll_area)

        # Кнопка для добавления новых кнопок
        add_button = QPushButton("Добавить кнопку", self)
        add_button.clicked.connect(self.add_button)
        main_layout.addWidget(add_button)

    def add_button(self):
        # Создаем новую кнопку и добавляем ее в layout контейнера
        new_button = QPushButton(f"Кнопка {self.button_layout.count() + 1}", self)
        self.button_layout.addWidget(new_button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScrollAreaExample()
    window.show()
    sys.exit(app.exec())