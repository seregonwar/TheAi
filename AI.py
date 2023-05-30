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

        self.chat_layout = QVBoxLayout()
        self.central_widget.setLayout(self.chat_layout)

        self.chat_widget = QWidget(self.central_widget)
        self.history_widget = QWidget(self.central_widget)

        self.central_widget.addWidget(self.chat_widget)
        self.central_widget.addWidget(self.history_widget)
        self.central_widget.setCollapsible(0, False)
        self.central_widget.setCollapsible(1, True)
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

        # Aggiungi il menu delle chat a destra
        self.central_widget.setCollapsible(0, False)
        self.central_widget.setCollapsible(1, True)
        self.central_widget.setSizes([600, 200])

        # Aggiungi pulsante "New Chat"
        self.new_chat_button = QPushButton("New Chat")
        self.new_chat_button.setFont(QFont("Arial", 12))
        self.new_chat_button.clicked.connect(self.create_new_chat)
        self.central_widget.layout().addWidget(self.new_chat_button)

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

        # Aggiungi la risposta del chatbot allo storico delle chat
        self.chat_history.append({"timestamp": current_time, "sender": "BOT", "message": message})

    def upload_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Upload File",
            "",
            "All Files (*);;Text Files (*.txt)",
            options=options
        )

        if file_path:
            # Upload file
            self.add_user_message(f"[FILE] {file_path}")

    def search_online(self, query):
        credentials = None

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                credentials = credentials.from_service_account_file(
                    "service_account.json",
                    target_principal="your_target_service_account@example.com"
                )

        with impersonated_credentials.Credentials(
            credentials=credentials,
            target_principal="your_target_service_account@example.com",
            target_scopes=["https://www.googleapis.com/auth/cloud-platform"],
            lifetime=3600,
        ) as impersonated_creds:
            search_results = list(search(query, num_results=5, credentials=impersonated_creds))

        return search_results

    def toggle_diction(self):
        if self.diction_button.isChecked():
            engine.setProperty("rate", 150)  # Default speed
        else:
            engine.setProperty("rate", 100)  # Reduced speed

    def change_theme(self, action):
        theme = action.text()

        if theme == "Light Theme":
            self.set_theme("light")
        elif theme == "Dark Theme":
            self.set_theme("dark")

    def set_theme(self, theme):
        palette = self.palette()

        if theme == "light":
            palette.setColor(QPalette.Base, Qt.white)
            palette.setColor(QPalette.Text, Qt.black)
        elif theme == "dark":
            palette.setColor(QPalette.Base, Qt.black)
            palette.setColor(QPalette.Text, Qt.white)

        self.setPalette(palette)

    def create_new_chat(self):
        self.chat_text.clear()
        self.history_text.clear()
        self.chat_history = []

app = QApplication([])
window = ChatWindow()
window.show()
app.exec_()
