#pyuic6 Designer.ui -o main_ui.py
#pyuic6 CMDedit.ui -o cmd_ui.py
#pyuic6 CMD_start_edit.ui -o cmd_start_ui.py
import sqlite3
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

current_button = 0

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

#CMD_EDIT
class AnotherWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.image = False
        self.ok_button.clicked.connect(self.get_text)
        self.checkBox_output_image.stateChanged.connect(self.on_checkbox_changed)

    def get_text(self):
        #lineEdit
        global current_button
        text_input = self.lineEditInput.text()
        text_output = self.lineEditOutput.text()
        print(text_input)
        print(text_output)
        print(current_button)
        add_input_to_database(current_button, text_input)
        is_img_ = 0
        if self.image is True:
            is_img_ = 1
        else:
            is_img_ = 0
        add_output_to_database(current_button, text_output)

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
            with open('Bot_description.txt', 'w') as f:
                f.write(self.bot_name)

    def add_action(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Выбор действия")

        # Устанавливаем стиль для диалогового окна
        dialog.setStyleSheet("QInputDialog{background-color: rgb(61, 65, 89);}")

        action, ok_pressed = QInputDialog.getItem(
            dialog, "Ввод", "",
            ("Стандартная команда", "Start message",), 0, False)

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

                # Подключаем сигнал clicked к слоту
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
            global current_button
            sending_button = self.sender()
            print(sending_button.text())
            current_button = int(sending_button.text()[-1])
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
        self.window1 = ChatApp()
        if self.window1.isVisible():
            self.window1.hide()
        else:
            self.window1.show()

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

# Записываем input
def add_input_to_database(id, variable):
    connection = sqlite3.connect('Data_base2.db')
    cursor = connection.cursor()

    # Проверяем, существует ли запись с данным id
    cursor.execute('SELECT * FROM Input_cmd WHERE id = ?', (id,))
    row = cursor.fetchone()

    if row:
        # Если запись существует, обновляем её
        cursor.execute('UPDATE Input_cmd SET value = ? WHERE id = ?', (variable, id))
        print(f"Запись с id {id} обновлена.")
    else:
        # Если записи нет, вставляем новую
        cursor.execute('INSERT INTO Input_cmd (id, value) VALUES (?, ?)', (id, variable))
        print(f"Запись с id {id} добавлена.")

    connection.commit()
    connection.close()


# Записываем output
def create_output_table():
    connection = sqlite3.connect('Data_base2.db')
    cursor = connection.cursor()

    # Создаем таблицу Output_cmd, если она не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Output_cmd (
            id INTEGER PRIMARY KEY,
            value TEXT
        )
    ''')

    connection.commit()
    connection.close()


def add_output_to_database(id, variable):
    create_output_table()  # Убедимся, что таблица существует

    connection = sqlite3.connect('Data_base2.db')
    cursor = connection.cursor()

    # Проверяем, существует ли запись с данным id
    cursor.execute('SELECT * FROM Output_cmd WHERE id = ?', (id,))
    row = cursor.fetchone()

    if row:
        # Если запись существует, обновляем её
        cursor.execute('UPDATE Output_cmd SET value = ? WHERE id = ?', (variable, id))
        print(f"Запись с id {id} в таблице Output_cmd обновлена.")
    else:
        # Если записи нет, вставляем новую
        cursor.execute('INSERT INTO Output_cmd (id, value) VALUES (?, ?)', (id, variable))
        print(f"Запись с id {id} в таблице Output_cmd добавлена.")

    connection.commit()
    connection.close()

# Очистка
def clear_all_tables(database_name="Data_base2.db"):
    # Подключаемся к базе данных
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    try:
        # Получаем список всех таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Удаляем данные из каждой таблицы
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DELETE FROM {table_name}")
            print(f"Все данные из таблицы '{table_name}' были удалены.")

        # Сохраняем изменения
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при удалении данных: {e}")
    finally:
        # Закрываем соединение
        cursor.close()
        conn.close()


if __name__ == '__main__':
    #clear_all_tables()
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
