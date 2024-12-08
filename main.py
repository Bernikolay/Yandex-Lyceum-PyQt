#Import libaries
import sqlite3
import os
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QDialog,
                             QVBoxLayout,
                             QComboBox,
                             QInputDialog,
                             QMessageBox,
                             QPushButton,
                             QLabel,
                             QWidget,
                             QSpacerItem,
                             QSizePolicy)

#Import ui
from main_ui import Ui_MainWindow
from cmd_ui import Ui_Form
from cmd_start_ui import Ui_Form as Ui_Form_start

#Button you choose
current_button = 1

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

    #You can change type
    def on_checkbox_changed(self):
        self.image = not self.image
        if self.image:
            self.img_msg()
        else:
            self.lineEdit_2.setText("")
    #Image send
    def img_msg(self):
        self.lineEdit_2.setText("Укажите путь к картинке! (Два слэша в начале)")

#Command_EDIT
class AnotherWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.image = False
        self.ok_button.clicked.connect(self.get_text)
        self.checkBox_output_image.stateChanged.connect(self.on_checkbox_changed)
        #Get some data
        self.pullup()

    def pullup(self):
        global current_button

        #Connection
        self.connection = sqlite3.connect('Data_base2.db')
        self.cursor = self.connection.cursor()

        #Try to pullup
        try:
            print("current button:", current_button)
            query = "SELECT value FROM Input_cmd WHERE id = ?"
            self.cursor.execute(query, ((current_button),))
            result = self.cursor.fetchone()
            print(result[0], "Успех input pullup")
            self.lineEditInput.setText(str(result[0]))
        except Exception as e:
            #Error
            print("Ошибка input pullup")
        # Try to pullup
        try:
            print("current button:", current_button)
            query = "SELECT value FROM Output_cmd WHERE id = ?"
            self.cursor.execute(query, ((current_button),))
            result = self.cursor.fetchone()
            print(result[0], "Успех output pullup")
            self.lineEditOutput.setText(str(result[0]))
        #Error
        except Exception as e:
            print("Ошибка output pullup")

    #Input data
    def get_text(self):
        #lineEdit
        global current_button
        text_input = self.lineEditInput.text()
        text_output = self.lineEditOutput.text()
        print(text_input)
        print(text_output)
        #print(current_button)
        add_input_to_database(current_button, text_input)
        is_img_ = 0
        if self.image is True:
            is_img_ = 1
        else:
            is_img_ = 0
        add_output_to_database(current_button, text_output)
    #Change state
    def on_checkbox_changed(self):
        self.image = not self.image
        if self.image:
            self.img_msg()
        else:
            self.lineEditOutput.setText("")
    #Image
    def img_msg(self):
        #Path
        self.lineEditOutput.setText("Укажите путь к картинке! (Два слэша в начале)")

    def pullup_next_data(self):
        global current_button

        # Connection
        self.connection = sqlite3.connect('Data_base2.db')
        self.cursor = self.connection.cursor()

        # Pull up input data
        try:
            print("Current button:", current_button)
            query = "SELECT value FROM Input_cmd WHERE id = ?"
            self.cursor.execute(query, (current_button,))
            result = self.cursor.fetchone()
            print(result[0], "Success input pullup")
            self.lineEditInput.setText(str(result[0]))
        except Exception as e:
            print("Error input pullup")

        # Pull up output data
        try:
            print("Current button:", current_button)
            query = "SELECT value FROM Output_cmd WHERE id = ?"
            self.cursor.execute(query, (current_button,))
            result = self.cursor.fetchone()
            print(result[0], "Success output pullup")
            self.lineEditOutput.setText(str(result[0]))
        except Exception as e:
            print("Error output pullup")

#This is main window
class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.bot_name = ""
        super().__init__()
        self.setupUi(self)
        self.pixmap = QPixmap('Assets/pc1.png')
        self.label.setPixmap(self.pixmap)

        #Buttons
        self.pushButton_5.clicked.connect(self.add_name)
        self.plus_button.clicked.connect(self.add_action)
        #self.plus_button_2.clicked.connect(self.add_action)
        self.pause_button.clicked.connect(self.pause)
        self.run_bot_button.clicked.connect(self.run_bot)
        #self.welcome_message_button.clicked.connect(self.edit_cmd_start)
        #self.undo_button.clicked.connect(self.clear_all())

    def restore(self):
        self.connection = sqlite3.connect('Data_base2.db')
        self.cursor = self.connection.cursor()
        query = "SELECT MAX(id) AS max_id FROM Input_cmd"
        self.cursor.execute(query)
        result = self.cursor.fetchone()

        #SELECT MAX(id) AS max_id FROM Input_cmd;
        n = result[0]
        for i in range(int(n)):
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

            # Connect
            new_button.clicked.connect(self.edit_cmd)

            # Pos
            mid_index = self.button_layout.count() - 1

            # Insert
            self.button_layout.insertWidget(mid_index, new_button)

    def clear_all(self):
        clear_all_tables()
    def add_name(self):
        self.bot_name, ok_pressed = QInputDialog.getText(self, "Название", "Название:........")
        if ok_pressed:
            print(self.bot_name)
            with open('Bot_description.txt', 'w') as f:
                f.write(self.bot_name)

    def add_action(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Выбор действия")

        #Style
        dialog.setStyleSheet("QInputDialog{background-color: rgb(61, 65, 89);}")

        action, ok_pressed = QInputDialog.getItem(
            dialog, "Ввод", "",
            ("Стандартная команда", "Сообщение",), 0, False)

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

                #Connect
                new_button.clicked.connect(self.edit_cmd)

                #Pos
                mid_index = self.button_layout.count() - 1

                #Insert
                self.button_layout.insertWidget(mid_index, new_button)

    def print_one(self):
        print(1)

    def edit_cmd(self):
        global current_button
        sending_button = self.sender()
        print(sending_button.text(), "Текст кнопки")
        current_button = int(sending_button.text()[-1])
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
        self.window1 = ChatApp()
        if self.window1.isVisible():
            self.window1.hide()
        else:
            self.window1.hide()

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

        #Main box
        self.layout = QtWidgets.QVBoxLayout(self)

        #QScrollAre
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        #Widget
        self.messages_widget = QtWidgets.QWidget()
        self.messages_layout = QtWidgets.QVBoxLayout(self.messages_widget)

        self.scroll_area.setWidget(self.messages_widget)
        self.layout.addWidget(self.scroll_area)

        #New input
        self.input_field = QtWidgets.QLineEdit(self)
        self.input_field.setPlaceholderText("Введите ваше сообщение...")
        self.input_field.setStyleSheet("QLineEdit{"
                                       "background-color: white;"
                                       "border: 2px solid blue;"
                                       "border-radius: 10px;"
                                       "padding: 5px;"
                                       "}"
                                       "QPushButton:hover {"
                                       "background-color: lightblue;"
                                       "}")
        self.layout.addWidget(self.input_field)

        #New button
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

        #Connect
        self.connection = sqlite3.connect('Data_base2.db')
        self.cursor = self.connection.cursor()

    def send_message(self):
        message_text = self.input_field.text().strip()
        if message_text:
            #Add msg
            self.add_message("Вы: " + message_text)

            #Bot
            bot_response = self.get_bot_response(message_text)
            if bot_response:
                if bot_response.startswith('\\'):
                    # Если ответ начинается с \, загружаем изображение по указанному пути
                    image_path = bot_response[2:].strip()  # Убираем символ \
                    self.add_image(image_path)
                else:
                    self.add_message("Бот: " + bot_response)
            else:
                self.add_message("Бот: Извините, я не понимаю.")

            #Clear
            self.input_field.clear()

            #Scroll
            self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    def get_bot_response(self, user_input):
        #Search
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

    def add_image(self, image_path):
        #Check
        if os.path.isfile(image_path):
            pixmap = QPixmap(image_path)  # Загружаем изображение из файла

            image_label = QtWidgets.QLabel()
            image_label.setPixmap(pixmap)
            image_label.setScaledContents(True)  # Масштабирование содержимого
            image_label.setFixedSize(300, 300)   # Установка фиксированного размера для изображения
            self.messages_layout.addWidget(image_label)
        else:
            self.add_message("Бот: Не удалось найти изображение по указанному пути.")
            print(image_path)

    def closeEvent(self, event):
        #Close
        self.connection.close()
        event.accept()


#input
def add_input_to_database(id, variable):
    connection = sqlite3.connect('Data_base2.db')
    cursor = connection.cursor()

    #Check id
    cursor.execute('SELECT * FROM Input_cmd WHERE id = ?', (id,))
    row = cursor.fetchone()

    if row:
        #Update
        cursor.execute('UPDATE Input_cmd SET value = ? WHERE id = ?', (variable, id))
        print(f"Запись с id {id} обновлена.")
    else:
        #New table
        cursor.execute('INSERT INTO Input_cmd (id, value) VALUES (?, ?)', (id, variable))
        print(f"Запись с id {id} добавлена.")

    connection.commit()
    connection.close()

def add_new_input_to_database(id, variable):
    # Connecting to the database
    connection = sqlite3.connect('Data_base2.db')
    cursor = connection.cursor()

    #Check
    cursor.execute('SELECT COUNT(*) FROM Input_cmd WHERE id = ?', (id,))
    count_result = cursor.fetchone()[0]
    if count_result > 0:
        # Logic to update the record
        cursor.execute('UPDATE Input_cmd SET value = ? WHERE id = ?', (variable, id))
        print(f"Record with id {id} updated.")
    else:
        # Logic to insert a new record
        cursor.execute('INSERT INTO Input_cmd (id, value) VALUES (?, ?)', (id, variable))
        print(f"Record with id {id} added.")

    # Another check for the presence of the record (after making changes)
    cursor.execute('SELECT * FROM Input_cmd WHERE id = ?', (id,))
    row = cursor.fetchone()
    if row:
        print(f"After updating/inserting, the record with id {id} looks like this: {row}")

    # Closing the connection
    connection.commit()
    connection.close()

#output
def create_output_table():
    connection = sqlite3.connect('Data_base2.db')
    cursor = connection.cursor()

    #Output_cmd
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Output_cmd (
            id INTEGER PRIMARY KEY,
            value TEXT
        )
    ''')

    connection.commit()
    connection.close()

#new table
def create_my_table():
    connection = sqlite3.connect('Data_base2.db')
    cursor = connection.cursor()

    #Output_cmd
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Data (
            id INTEGER PRIMARY KEY,
            value TEXT
        )
    ''')

    connection.commit()
    connection.close()

def add_output_to_database(id, variable):
    create_output_table()  #Check table

    connection = sqlite3.connect('Data_base2.db')
    cursor = connection.cursor()

    #Check id
    cursor.execute('SELECT * FROM Output_cmd WHERE id = ?', (id,))
    row = cursor.fetchone()

    if row:
        #Update
        cursor.execute('UPDATE Output_cmd SET value = ? WHERE id = ?', (variable, id))
        print(f"Запись с id {id} в таблице Output_cmd обновлена.")
    else:
        #New data
        cursor.execute('INSERT INTO Output_cmd (id, value) VALUES (?, ?)', (id, variable))
        print(f"Запись с id {id} в таблице Output_cmd добавлена.")

    connection.commit()
    connection.close()

#Clear
def clear_all_tables(database_name="Data_base2.db"):
    #Connect
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    try:
        #Get data
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Удаляем данные из каждой таблицы
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DELETE FROM {table_name}")
            print(f"Все данные из таблицы '{table_name}' были удалены.")

        #Save
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при удалении данных: {e}")
    finally:
        #Close
        cursor.close()
        conn.close()


if __name__ == '__main__':
    #Clear func:
    clear_all_tables()
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())

#pyuic6 Designer.ui -o main_ui.py
#pyuic6 CMDedit.ui -o cmd_ui.py
#pyuic6 CMD_start_edit.ui -o cmd_start_ui.py
