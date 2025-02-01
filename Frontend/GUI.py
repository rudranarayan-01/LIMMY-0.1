from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QTextFormat
from PyQt5.QtCore import Qt, QSize, QTimer
from dotenv import dotenv_values, load_dotenv
import sys
import os

load_dotenv()

env_vars = os.getenv("")
AssistantName = os.getenv("AssistantName")
current_dir = os.getcwd()
old_chat_messages = ""
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}"