from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel, QMenu, QMenuBar, QAction, QFileDialog, QSplitter
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
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

        self.setWindowTitle("TheAi")
        self.setGeometry(100, 100, 800, 500)

        self.central_widget = QSplitter(self)
        self.setCentralWidget(self.central_widget)

        # Barra di ricerca
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.handle_search)

        search_layout = QVBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        search_widget = QWidget()
        search_widget.setLayout(search_layout)

        self.central_widget.addWidget(search_widget)

        self.chat_layout = QVBoxLayout()
        self.central_widget.setLayout(self.chat_layout)

        self.chat_widget = QWidget(self.central_widget)
        self.history_widget = QWidget(self.central_widget)

        self.central_widget.addWidget(self.chat_widget)
        self.central_widget.addWidget(self.history_widget)
        self.central_widget.setCollapsible(0, False)
        self.central_widget.setCollapsible(1, True)
        self.central_widget.setSizes([200, 600])

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

        self.new_chat_button = QPushButton("New Chat")
        self.new_chat_button.setFont(QFont("Arial", 12))
        self.new_chat_button.clicked.connect(self.create_new_chat)

        # Aggiungi il pulsante "New Chat" al layout del widget centrale
        self.central_widget.layout().addWidget(self.new_chat_button)

        # Pulsante per decidere se lasciare o meno la dizione
        self.diction_button = QPushButton("Toggle Diction")
        self.diction_button.setFont(QFont("Arial", 12))
        self.diction_button.setCheckable(True)
        self.diction_button.setChecked(True)  # Default: diction enabled
        self.diction_button.clicked.connect(self.toggle_diction)
        self.chat_layout.addWidget(self.diction_button)

        # Menu a tendina per cambiare il tema dell'applicazione
        self.theme_menu = QMenu("Change Theme")
        self.theme_menu.setFont(QFont("Arial", 12))
        self.theme_menu.triggered.connect(self.change_theme)

        self.theme_action_light = QAction("Light Theme")
        self.theme_action_light.setFont(QFont("Arial", 12))
        self.theme_action_light.setCheckable(True)
        self.theme_action_light.setChecked(True)  # Default: light theme
        self.theme_menu.addAction(self.theme_action_light)

        self.theme_action_dark = QAction("Dark Theme")
        self.theme_action_dark.setFont(QFont("Arial", 12))
        self.theme_action_dark.setCheckable(True)
        self.theme_menu.addAction(self.theme_action_dark)

        self.theme_menu_button = QMenuBar()
        self.theme_menu_button.addMenu(self.theme_menu)
        self.chat_layout.addWidget(self.theme_menu_button)

        # Web browser basato su Chromium
        self.web_view = QWebEngineView()
        self.history_layout.addWidget(self.web_view)

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

                # Text-to-speech synthesis
                engine.say("Could you please provide some search suggestions?")
                engine.runAndWait()

                engine.say("Here are some search suggestions:")
                engine.runAndWait()

                for suggestion in suggestions:
                    engine.say(suggestion)
                    engine.runAndWait()

            else:
                self.add_bot_message(response)

                # Text-to-speech synthesis
                engine.say(response)
                engine.runAndWait()

    def add_user_message(self, message):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.chat_text.setTextColor(QColor("blue"))
        self.chat_text.append(f"[USER] {current_time}: {message}")
        self.chat_text.setTextColor(QColor("black"))

        # Aggiungi la richiesta dell'utente allo storico delle chat
        self.chat_history.append({"timestamp": current_time, "sender": "USER", "message": message})

    def add_bot_message(self, message):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.chat_text.setTextColor(QColor("green"))
        self.chat_text.append(f"[BOT] {current_time}: {message}")
        self.chat_text.setTextColor(QColor("black"))

        # Aggiungi la risposta del bot allo storico delle chat
        self.chat_history.append({"timestamp": current_time, "sender": "BOT", "message": message})

    def upload_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Upload File")
        if file_path:
            self.add_user_message(f"Uploaded file: {file_path}")

    def create_new_chat(self):
        # Pulisci la finestra di chat
        self.chat_text.clear()

        # Resetta la cronologia delle chat
        self.chat_history = []

    def toggle_diction(self):
        if self.diction_button.isChecked():
            self.diction_button.setText("Toggle Diction: ON")
            engine.setProperty("volume", 1.0)
        else:
            self.diction_button.setText("Toggle Diction: OFF")
            engine.setProperty("volume", 0.0)

    def change_theme(self, action):
        if action == self.theme_action_light:
            self.theme_action_light.setChecked(True)
            self.theme_action_dark.setChecked(False)
            self.set_theme("light")
        elif action == self.theme_action_dark:
            self.theme_action_light.setChecked(False)
            self.theme_action_dark.setChecked(True)
            self.set_theme("dark")

    def set_theme(self, theme):
        if theme == "light":
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(255, 255, 255))
            palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
            palette.setColor(QPalette.Base, QColor(240, 240, 240))
            palette.setColor(QPalette.AlternateBase, QColor(220, 220, 220))
            palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
            palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
            palette.setColor(QPalette.Text, QColor(0, 0, 0))
            palette.setColor(QPalette.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
            palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.Link, QColor(0, 0, 255))
            palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
            palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
            QApplication.setPalette(palette)
        elif theme == "dark":
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
            palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
            palette.setColor(QPalette.Text, QColor(255, 255, 255))
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
            palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
            QApplication.setPalette(palette)

    def handle_search(self):
        query = self.search_input.text().strip()
        if query:
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

        self.search_input.clear()

    def search_online(self, query):
        search_results = []
        for result in search(query, num_results=5):
            search_results.append(result)
        return search_results


if __name__ == "__main__":
    app = QApplication([])
    window = ChatWindow()
    window.show()
    app.exec()
