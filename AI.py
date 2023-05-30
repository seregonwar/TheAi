from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel, QMenu, QMenuBar, QAction, QFileDialog, QSplitter
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from hugchat import hugchat
from googlesearch import search
from google.auth import impersonated_credentials
from google.auth.transport.requests import Request
import json
import pyttsx3
import datetime

chatbot = hugchat.ChatBot(cookie_path="cookies.json")  # or cookies=[...]

engine = pyttsx3.init()

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ChatBot")
        self.setGeometry(100, 100, 800, 500)

        self.central_widget = QSplitter(self)
        self.setCentralWidget(self.central_widget)

        self.chat_widget = QWidget(self.central_widget)
        self.history_widget = QWidget(self.central_widget)

        self.central_widget.addWidget(self.chat_widget)
        self.central_widget.addWidget(self.history_widget)
        self.central_widget.setSizes([600, 200])

        self.chat_layout = QVBoxLayout()
        self.chat_widget.setLayout(self.chat_layout)

        self.history_layout = QVBoxLayout()
        self.history_widget.setLayout(self.history_layout)

        self.chat_text = QTextEdit()
        self.chat_text.setReadOnly(True)
        self.chat_text.setFont(QFont("Arial", 12))
        self.chat_layout.addWidget(self.chat_text)

        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Arial", 12))
        self.chat_layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send")
        self.send_button.setFont(QFont("Arial", 12))
        self.send_button.clicked.connect(self.handle_user_input)
        self.chat_layout.addWidget(self.send_button)

        self.file_button = QPushButton("Upload File")
        self.file_button.setFont(QFont("Arial", 12))
        self.file_button.clicked.connect(self.upload_file)
        self.chat_layout.addWidget(self.file_button)

        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        self.history_text.setFont(QFont("Arial", 12))
        self.history_layout.addWidget(self.history_text)

        # Storico delle chat
        self.chat_history = []

    def handle_user_input(self):
        user_input = self.input_field.text().strip()
        self.input_field.clear()

        if user_input:
            # Aggiungi la richiesta dell'utente alla chat
            self.add_user_message(user_input)

            response = chatbot.chat(user_input)

            # Check if user wants to search online
            if response.startswith("[SEARCH]"):
                query = response.replace("[SEARCH]", "").strip()
                search_results = self.search_online(query)
                self.add_bot_message(f"You asked me to search for '{query}'. Here are some results:")

                for i, result in enumerate(search_results):
                    self.add_bot_message(f"{i+1}. {result}")

                # Text-to-speech synthesis
                engine.say("Here are some search results:")
                engine.runAndWait()

                for i, result in enumerate(search_results):
                    engine.say(f"Result {i+1}: {result}")
                    engine.runAndWait()

            # Check if user wants search suggestions
            elif response == "[SUGGESTIONS]":
                self.add_bot_message("Could you please provide some search suggestions?")

                # Placeholder suggestions
                suggestions = ["suggestion 1", "suggestion 2", "suggestion 3"]
                self.add_bot_message("Here are some search suggestions:")

                for suggestion in suggestions:
                    self.add_bot_message(f"- {suggestion}")

            # Check if user wants to access local files
            elif response == "[ACCESS_LOCAL_FILES]":
                self.add_bot_message("Sure, I can access local files. Please provide the file path.")

            # Display the response from the chatbot
            self.add_bot_message(response)

    def search_online(self, query):
        # Perform the Google search
        search_results = list(search(query, num_results=5))
        return search_results

    def add_user_message(self, message):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.chat_text.append(f"[User | {current_time}]: {message}")
        self.chat_history.append(f"[User | {current_time}]: {message}")

    def add_bot_message(self, message):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.chat_text.append(f"[AI | {current_time}]: {message}")
        self.chat_history.append(f"[AI | {current_time}]: {message}")

    def upload_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_path, _ = QFileDialog.getOpenFileName(self, "Upload File", "", "All Files (*);;Text Files (*.txt)", options=options)

        if file_path:
            # Visualizza il file nella chat come messaggio inviato dall'utente
            self.add_user_message(f"Uploaded file: {file_path}")
            self.add_bot_message(f"Processing file: {file_path}")
            # Add your file processing and analysis logic here

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ChatBot")
        self.setGeometry(100, 100, 800, 500)

        self.central_widget = QSplitter(self)
        self.setCentralWidget(self.central_widget)

        self.chat_widget = QWidget(self.central_widget)
        self.history_widget = QWidget(self.central_widget)

        self.central_widget.addWidget(self.chat_widget)
        self.central_widget.addWidget(self.history_widget)
        self.central_widget.setSizes([600, 200])

        self.chat_layout = QVBoxLayout()
        self.chat_widget.setLayout(self.chat_layout)

        self.history_layout = QVBoxLayout()
        self.history_widget.setLayout(self.history_layout)

        self.chat_text = QTextEdit()
        self.chat_text.setReadOnly(True)
        self.chat_text.setFont(QFont("Arial", 12))
        self.chat_layout.addWidget(self.chat_text)

        self.input_field = QLineEdit()
        self.input_field.setFont(QFont("Arial", 12))
        self.chat_layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send")
        self.send_button.setFont(QFont("Arial", 12))
        self.send_button.clicked.connect(self.handle_user_input)
        self.chat_layout.addWidget(self.send_button)

        self.file_button = QPushButton("Upload File")
        self.file_button.setFont(QFont("Arial", 12))
        self.file_button.clicked.connect(self.upload_file)
        self.chat_layout.addWidget(self.file_button)

        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        self.history_text.setFont(QFont("Arial", 12))
        self.history_layout.addWidget(self.history_text)

        # Storico delle chat
        self.chat_history = []

    def handle_user_input(self):
        user_input = self.input_field.text().strip()
        self.input_field.clear()

        if user_input:
            # Aggiungi la richiesta dell'utente alla chat
            self.add_user_message(user_input)

            response = chatbot.chat(user_input)

            # Check if user wants to search online
            if response.startswith("[SEARCH]"):
                query = response.replace("[SEARCH]", "").strip()
                search_results = self.search_online(query)
                self.add_bot_message(f"You asked me to search for '{query}'. Here are some results:")

                for i, result in enumerate(search_results):
                    self.add_bot_message(f"{i+1}. {result}")

                # Text-to-speech synthesis
                engine.say("Here are some search results:")
                engine.runAndWait()

                for i, result in enumerate(search_results):
                    engine.say(f"Result {i+1}: {result}")
                    engine.runAndWait()

            # Check if user wants search suggestions
            elif response == "[SUGGESTIONS]":
                self.add_bot_message("Could you please provide some search suggestions?")

                # Placeholder suggestions
                suggestions = ["suggestion 1", "suggestion 2", "suggestion 3"]
                self.add_bot_message("Here are some search suggestions:")

                for suggestion in suggestions:
                    self.add_bot_message(f"- {suggestion}")

            # Check if user wants to access local files
            elif response == "[ACCESS_LOCAL_FILES]":
                self.add_bot_message("Sure, I can access local files. Please provide the file path.")

            # Display the response from the chatbot
            self.add_bot_message(response)

    def search_online(self, query):
        # Perform the Google search
        search_results = list(search(query, num_results=5))
        return search_results

    def add_user_message(self, message):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.chat_text.append(f"[User | {current_time}]: {message}")
        self.chat_history.append(f"[User | {current_time}]: {message}")

    def add_bot_message(self, message):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.chat_text.append(f"[AI | {current_time}]: {message}")
        self.chat_history.append(f"[AI | {current_time}]: {message}")

    def upload_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_path, _ = QFileDialog.getOpenFileName(self, "Upload File", "", "All Files (*);;Text Files (*.txt)", options=options)

        if file_path:
            # Visualizza il file nella chat come messaggio inviato dall'utente
            self.add_user_message(f"Uploaded file: {file_path}")
            self.add_bot_message(f"Processing file: {file_path}")
            # Add your file processing and analysis logic here

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 300, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.settings_label = QLabel("Application Settings")
        self.settings_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.layout.addWidget(self.settings_label)

        self.settings_text = QTextEdit()
        self.settings_text.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.settings_text)

# Creazione dell'applicazione principale
if __name__ == "__main__":
    app = QApplication([])

    # Personalizzazione del tema dell'app
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(220, 220, 220))
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    app.setPalette(palette)

    # Creazione della finestra dell'applicazione
    app_window = AppWindow()
    app_window.show()

    # Aggiunta di un menu a tendina per gestire le impostazioni dell'applicazione
    menu_bar = QMenuBar(app_window)
    settings_menu = QMenu("Settings", app_window)
    menu_bar.addMenu(settings_menu)
    settings_action = QAction("Application Settings", app_window)
    settings_action.triggered.connect(lambda: show_settings_window(app_window))
    settings_menu.addAction(settings_action)
    app_window.setMenuBar(menu_bar)

    # Creazione della finestra delle impostazioni
    settings_window = SettingsWindow()
    settings_window.hide()

    def show_settings_window(parent):
        settings_window.show()

    app.exec_()
