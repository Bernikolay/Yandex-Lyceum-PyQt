import sys
from PyQt6 import QtWidgets, QtGui, QtCore

class ChatApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chat App")
        self.setGeometry(100, 100, 400, 600)

        # Основной вертикальный макет
        self.layout = QtWidgets.QVBoxLayout(self)

        # Создаем QScrollArea для сообщений
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Создаем виджет для размещения сообщений
        self.messages_widget = QtWidgets.QWidget()
        self.messages_layout = QtWidgets.QVBoxLayout(self.messages_widget)

        self.scroll_area.setWidget(self.messages_widget)
        self.layout.addWidget(self.scroll_area)

        # Создаем текстовое поле для ввода пути к изображению
        self.image_path_input = QtWidgets.QLineEdit(self)
        self.image_path_input.setPlaceholderText("Введите абсолютный путь к изображению...")
        self.layout.addWidget(self.image_path_input)

        # Создаем кнопку для отправки изображения
        self.send_button = QtWidgets.QPushButton("Отправить изображение", self)
        self.send_button.clicked.connect(self.send_image)
        self.layout.addWidget(self.send_button)

    def send_image(self):
        image_path = self.image_path_input.text()
        if image_path:
            self.add_user_image(image_path)  # Отправляем изображение от пользователя
            self.add_bot_image(image_path)    # Бот отправляет то же изображение
            self.image_path_input.clear()      # Очищаем поле ввода после отправки

    def add_user_image(self, image_path):
        try:
            pixmap = QtGui.QPixmap(image_path)
            if not pixmap.isNull():
                user_image_label = QtWidgets.QLabel("Вы:")
                user_image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                self.messages_layout.addWidget(user_image_label)

                image_label = QtWidgets.QLabel()
                image_label.setPixmap(pixmap.scaled(300, 300, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
                image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                self.messages_layout.addWidget(image_label)
            else:
                self.add_message("Ошибка: Невозможно загрузить изображение.")
        except Exception as e:
            self.add_message(f"Ошибка: {str(e)}")

    def add_bot_image(self, image_path):
        try:
            pixmap = QtGui.QPixmap(image_path)
            if not pixmap.isNull():
                bot_image_label = QtWidgets.QLabel("Бот:")
                bot_image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
                self.messages_layout.addWidget(bot_image_label)

                image_label = QtWidgets.QLabel()
                image_label.setPixmap(pixmap.scaled(300, 300, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
                image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
                self.messages_layout.addWidget(image_label)
            else:
                self.add_message("Ошибка: Невозможно загрузить изображение.")
        except Exception as e:
            self.add_message(f"Ошибка: {str(e)}")

    def add_message(self, message):
        message_label = QtWidgets.QLabel(message)
        message_label.setWordWrap(True)
        self.messages_layout.addWidget(message_label)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    chat_app = ChatApp()
    chat_app.show()
    sys.exit(app.exec())
