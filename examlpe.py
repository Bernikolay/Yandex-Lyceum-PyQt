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
        self.messages_widget.setStyleSheet("QWidget{"
                                           "background-color: white;"
                                           "}")
        self.messages_layout = QtWidgets.QVBoxLayout(self.messages_widget)

        self.scroll_area.setWidget(self.messages_widget)
        self.layout.addWidget(self.scroll_area)

        # Создаем поле ввода текста
        self.input_field = QtWidgets.QLineEdit(self)
        self.input_field.setStyleSheet("QLineEdit{"
                                            "background-color: white;"
                                            "border: 2px solid blue;"
                                            "border-radius: 10px;"
                                            "padding: 5px;"
                                            "}"
                                            "QPushButton:hover {"
                                            "background-color: lightblue;"
                                            "}")
        self.input_field.setPlaceholderText("Введите ваше сообщение...")
        self.layout.addWidget(self.input_field)

        # Создаем кнопку отправки
        self.send_button = QtWidgets.QPushButton("Отправить", self)
        self.send_button.setStyleSheet(("QPushButton{"
                                            "background-color: white;"
                                            "border: 2px solid blue;"
                                            "border-radius: 10px;"
                                            "padding: 5px;"
                                            "}"
                                            "QPushButton:hover {"
                                            "background-color: lightblue;"
                                            "}"))
        self.send_button.clicked.connect(self.send_message)
        self.layout.addWidget(self.send_button)

        # Подключение к базе данных
        self.connection = sqlite3.connect('Data_base2.db')
        self.cursor = self.connection.cursor()

    def send_message(self):
        message_text = self.input_field.text().strip()
        if message_text:
            # Добавляем сообщение пользователя
            self.add_message("Вы: " + message_text)

            # Получаем ответ от бота
            bot_response = self.get_bot_response(message_text)
            if bot_response:
                self.add_message("Бот: " + bot_response)
            else:
                self.add_message("Бот: Извините, я не понимаю.")

            # Очищаем поле ввода
            self.input_field.clear()

            # Прокручиваем вниз к последнему сообщению
            self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    def get_bot_response(self, user_input):
        # Поиск ответа в базе данных
        try:
            query = "SELECT value FROM Output_cmd WHERE id IN (SELECT id FROM Input_cmd WHERE value = ?)"
            self.cursor.execute(query, (user_input,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Ошибка при получении ответа: {e}")
            return None

    def add_message(self, message):
        message_label = QtWidgets.QLabel(message)
        message_label.setWordWrap(True)
        self.messages_layout.addWidget(message_label)

    def closeEvent(self, event):
        # Закрытие соединения с базой данных при выходе
        self.connection.close()
        event.accept()
