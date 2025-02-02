from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QTextFormat,QPixmap, QTextBlockFormat
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
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"


def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why","which", "whose", "whom", "can you", "what's", "who's", "where's", "who's", "how's", "who's", ]
    
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    
    return new_query.capitalize()


def SetMicrophoneStatus(Command):
    with open(rf'{TempDirPath}\Mic.data','w',encoding='utf-8') as file:
        file.write(Command)
def GetMicrophoneStatus():
    with open(rf'{TempDirPath}\Mic.data','r',encoding='utf-8') as file:
        Status = file.read()
        return Status
def SetAssistantStatus(Command):
    with open(rf'{TempDirPath}\Status.data','w',encoding='utf-8') as file:
        file.write(Command)

def GetAssistantStatus():
    with open(rf'{TempDirPath}\Status.data','r',encoding='utf-8') as file:
        Status = file.read()
        return Status

def MicButtonInitiated():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")
    
def GraphicsDirectoryPath(Filename):
    Path = rf"{GraphicsDirPath}\{Filename}"
    return Path

def TempDirectoryPath(Filename):
    Path = rf"{TempDirPath}\{Filename}"
    return Path

def ShowTextToScreen(Text):
    with open(rf"{TempDirPath}\Responses.data","w", encoding="utf-8") as file:
        file.write(Text)

class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10,40,40,100)
        layout.setSpacing(-100)
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)
        self.setStyleSheet("background-color: black")
        layout.setSizeConstraint(QVBoxLayout.setDefaultConstraint)
        layout.setStretch(1,1)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        text_color = QColor(Qt.blue)
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border:none")
        movie = QMovie(GraphicsDirectoryPath("Jarvis.gif"))
        max_gif_size_w = 480
        max_gif_size_h = 270
        movie.setScaledSize(QMovie(max_gif_size_w, max_gif_size_h))
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label)
        self.label = QLabel("")
        self.label.setStyleSheet("color:white;font-size:16px;font-weight:bold margin-right:195px; margin-top:-30px; border:none")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)
        layout.setSpacing(-10)
        layout.addWidget(self.gif_label)
        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start()
        self.chat_text_edit.viewport().installEventFilter(self)
        self.setStyleSheet("""
                           QScrollBar:vertical{
                               border: none;
                               background: black;
                               height: 10px;
                               margin: 0 0 0 0;
                           }
                           QScrollBar:handle:vertical{
                               background: white;
                               min-height: 20px;
                           }
                           QScrollBar::add-line:vertical{
                               background: black;
                               subcontrol-position: bottom;
                               subcontrol-origin: bottom;
                               height: 10px;
                           }
                           QScrollBar::sub-line:vertical{
                               background: black;
                               subcontrol-position: top;
                               subcontrol-origin: margin;
                               height: 10px;
                           }
                           QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{
                               border: none;
                               background:none:
                               color:none;
                           }
                           QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{
                               background: none;
                           }
                            """)
        def load_messages(self):
            global old_chat_messages
            with open(TempDirectoryPath("Responces.data"), "r", encoding="utf-8") as file:
                messages = file.read()
                
                if None == messages:
                    pass
                if len(messages)<=1:
                    pass
                if str(old_chat_messages) == str(messages):
                    pass
                else:
                    self.addMessage(message = messages, color = "White")
                    old_chat_messages = messages
                    
        def SpeechRecogText(self):
            with open(TempDirectoryPath("Status.data"), "r", encoding="utf-8") as file:
                messages = file.read()
                self.label.setText(messages)
               
                    
            
        def load_icon(self,path, width = 60, height = 60):
            pixmap = QPixmap(path)
            new_pixmap = pixmap.scaled(width, height)
            self.icon_label.setPixmap(new_pixmap)
        
        def toggle_icon(self,event=None):
            if self.toggled:
                self.load_icon(GraphicsDirectoryPath("voice.png",60, 60))
                MicButtonInitiated()
            else:
                self.load_icon(GraphicsDirectoryPath("mic.png",60, 60))
                MicButtonClosed()
            self.toggled = not self.toggled
            
        
        def addMessage(self, message, color):
            cursor = self.chat_text_edit().textCursor()
            format = QTextCharFormat()
            formatm = QTextBlockFormat()
            formatm.setTopMargin(10)
            formatm.setLeftMargin(10)
            format.setForeground(QColor(color))
            cursor.setCharFormat(format)
            cursor.setBlockFormat(formatm)
            cursor.insertText(message + "\n")
            self.chat_text_edit().setTextCursor(cursor)

class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height() 
