from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QTextFormat,QPixmap, QTextBlockFormat
from PyQt5.QtCore import Qt, QSize, QTimer, QPoint
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
        
print("Done")



class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()
        self.old_chat_messages = ""  # Initialize global message tracker
        self.toggled = False  # Initialize toggle state
        
        # Layout setup
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 40, 40, 100)  # Adjusted margins
        layout.setSpacing(10)  # Fixed negative spacing

        # Chat Text Edit
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        layout.addWidget(self.chat_text_edit)

        # Set text edit font
        font = QFont()
        font.setPointSize(13)
        self.chat_text_edit.setFont(font)

        # GIF Label
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border:none")
        movie = QMovie(GraphicsDirectoryPath("Jarvis.gif"))
        self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label)

        # Status Label
        self.label = QLabel("")
        self.label.setStyleSheet("color:white;font-size:16px;font-weight:bold; margin-right:195px; margin-top:-30px; border:none")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)

        # Timer for message updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(1000)  # Set interval (e.g., 1 second)

        self.chat_text_edit.viewport().installEventFilter(self)

        # Scrollbar Styling
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
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical{
                background: black;
                height: 10px;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{
                border: none;
                background:none;
                color:none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{
                background: none;
            }
        """)

    def loadMessages(self):
        """Loads messages from file and updates chat section."""
        try:
            with open(TempDirectoryPath("Responses.data"), "r", encoding="utf-8") as file:
                messages = file.read().strip()

                if messages and messages != self.old_chat_messages:
                    self.addMessage(message=messages, color="White")
                    self.old_chat_messages = messages
        except FileNotFoundError:
            pass

    def SpeechRecogText(self):
        """Updates status label with text from file."""
        try:
            with open(TempDirectoryPath("Status.data"), "r", encoding="utf-8") as file:
                messages = file.read().strip()
                self.label.setText(messages)
        except FileNotFoundError:
            pass

    def load_icon(self, path, width=60, height=60):
        """Loads and resizes an icon."""
        pixmap = QPixmap(path).scaled(width, height)
        self.icon_label.setPixmap(pixmap)

    def toggle_icon(self, event=None):
        """Toggles microphone button icon."""
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath("Mic_on.png"), 60, 60)
            self.MicButtonInitiated()
        else:
            self.load_icon(GraphicsDirectoryPath("Mic_off.png"), 60, 60)
            self.MicButtonClosed()
        self.toggled = not self.toggled

    def addMessage(self, message, color):
        """Adds messages to chat window with specified color."""
        cursor = self.chat_text_edit.textCursor()
        text_format = QTextCharFormat()
        text_block_format = QTextBlockFormat()
        
        text_block_format.setTopMargin(10)
        text_block_format.setLeftMargin(10)

        text_format.setForeground(QColor(color))

        cursor.setCharFormat(text_format)
        cursor.setBlockFormat(text_block_format)
        cursor.insertText(message + "\n")

        self.chat_text_edit.setTextCursor(cursor)

        
print("Chat session done")

##########################################################

class InitialScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Get screen dimensions
        screen = QApplication.primaryScreen().geometry()
        screen_width, screen_height = screen.width(), screen.height()

        # Layout setup
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Load GIF
        gif_label = QLabel()
        movie = QMovie(GraphicsDirectoryPath("Jarvis.gif"))
        max_gif_size_H = int(screen_width / 16 * 9)
        movie.setScaledSize(QSize(screen_width, max_gif_size_H))
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()

        # Load microphone icon
        self.icon_label = QLabel()
        self.load_icon(GraphicsDirectoryPath("Mic_on.png"), 60, 60)
        self.icon_label.setFixedSize(150, 150)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.mousePressEvent = self.toggle_icon

        # Speech recognition label
        self.label = QLabel("")
        self.label.setStyleSheet("color:white; font-size:16px; margin-bottom:0;")

        # Add widgets to layout
        content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 150)

        self.setLayout(content_layout)
        self.setFixedSize(screen_width, screen_height)
        self.setStyleSheet("background-color:black;")

        # Timer setup for Speech Recognition
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(1000)  # Reduced frequency to avoid excessive file reads

        # Icon toggle state
        self.toggled = True

    def SpeechRecogText(self):
        """Reads speech recognition status from a file and updates label text."""
        try:
            with open(TempDirectoryPath("Status.data"), "r", encoding="utf-8") as file:
                messages = file.read().strip()
                self.label.setText(messages)
        except FileNotFoundError:
            self.label.setText("No status data found.")
        except Exception as e:
            self.label.setText(f"Error: {str(e)}")

    def load_icon(self, path, width, height):
        """Loads and scales an icon."""
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event):
        """Toggles microphone icon and triggers corresponding function."""
        if self.toggled:
            self.load_icon(GraphicsDirectoryPath("Mic_off.png"), 60, 60)
            MicButtonClosed()
        else:
            self.load_icon(GraphicsDirectoryPath("Mic_on.png"), 60, 60)
            MicButtonInitiated()

        self.toggled = not self.toggled
        
        
print("Initial Screen Done")

##################################################
    
class MessageScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
            
        # Get screen size
        app = QApplication.instance()
        screen = app.primaryScreen()
        screen_rect = screen.availableGeometry()
        screen_width = screen_rect.width()
        screen_height = screen_rect.height()

        # Layout setup
        layout = QVBoxLayout()
        label = QLabel("")
        layout.addWidget(label)
            
        # Assuming ChatSection() is defined elsewhere
        chat_section = ChatSection()
        layout.addWidget(chat_section)

        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")
        self.setFixedSize(screen_width, screen_height) 
   

#############################################


class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        self.current_screen = None
        self.offset = QPoint()
        self.draggable = True
        self.initUI()

    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignRight)

        # Title Label
        assistant_name = str(os.getenv("AssistantName", "Assistant")).capitalize()
        title_label = QLabel(f"{assistant_name} AI")
        title_label.setStyleSheet("color:black; font-size: 18px; background-color:white;")

        # Home Button
        home_button = QPushButton("Home")
        home_button.setIcon(QIcon(GraphicsDirectoryPath("Home.png")))
        home_button.setStyleSheet("height:40px; background-color:white; color:black")

        # Chat Button
        message_button = QPushButton("Chat")
        message_button.setIcon(QIcon(GraphicsDirectoryPath("Chats.png")))
        message_button.setStyleSheet("height:40px; background-color:white; color:black")

        # Minimize Button
        minimize_button = QPushButton()
        minimize_button.setIcon(QIcon(GraphicsDirectoryPath("Minimize2.png")))
        minimize_button.setStyleSheet("background-color:white;")
        minimize_button.clicked.connect(self.minimizeWindow)

        # Maximize Button
        self.maximize_button = QPushButton()
        self.maximize_icon = QIcon(GraphicsDirectoryPath("Maximize.png"))
        self.restore_icon = QIcon(GraphicsDirectoryPath("Minimize.png"))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setStyleSheet("background-color:white;")
        self.maximize_button.clicked.connect(self.maximizeWindow)

        # Close Button
        close_button = QPushButton()
        close_button.setIcon(QIcon(GraphicsDirectoryPath("Close.png")))
        close_button.setStyleSheet("background-color:white;")
        close_button.clicked.connect(self.closeWindow)

        # Separator Line
        line_frame = QFrame()
        line_frame.setFixedHeight(1)
        line_frame.setFrameShape(QFrame.HLine)
        line_frame.setFrameShadow(QFrame.Sunken)
        line_frame.setStyleSheet("border-color: black;")

        # Button Click Events
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        # Layout Management
        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def paintEvent(self, event):
        """Paint background color."""
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)

    def minimizeWindow(self):
        """Minimize the parent window."""
        if self.parent():
            self.parent().showMinimized()

    def maximizeWindow(self):
        """Maximize or restore the parent window."""
        if self.parent():
            if self.parent().isMaximized():
                self.parent().showNormal()
                self.maximize_button.setIcon(self.maximize_icon)
            else:
                self.parent().showMaximized()
                self.maximize_button.setIcon(self.restore_icon)

    def closeWindow(self):
        """Close the parent window."""
        if self.parent():
            self.parent().close()

    def mousePressEvent(self, event):
        """Enable dragging."""
        if event.button() == Qt.LeftButton:
            self.offset = event.globalPos() - self.parent().pos()
            event.accept()

    def mouseMoveEvent(self, event):
        """Move window while dragging."""
        if event.buttons() == Qt.LeftButton and self.parent():
            self.parent().move(event.globalPos() - self.offset)
            event.accept()
            
    def showMessageScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()
        
        initial_screen = InitialScreen()
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(initial_screen)
        self.current_screen = initial_screen


print("Custom Top Bar Done")

####################################################

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()
    def initUI(self):
        # Get screen size
        app = QApplication.instance()
        screen = app.primaryScreen()
        screen_rect = screen.availableGeometry()
        screen_width = screen_rect.width()
        screen_height = screen_rect.height()

        # Create stacked widget and screens
        stacked_widget = QStackedWidget(self)
        initial_screen = InitialScreen()  # Ensure this is defined elsewhere
        message_screen = MessageScreen()  # Ensure this is defined elsewhere

        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)

        # Set window properties
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setStyleSheet("background-color: black;")

        # Add custom top bar
        top_bar = CustomTopBar(self, stacked_widget)  # Ensure this is defined elsewhere
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)

# def GraphicalUserInterface():
#     app = QApplication.instance()  
#     if not app:  
#         app = QApplication(sys.argv)

#     window = MainWindow()  # Ensure MainWindow is defined elsewhere
#     window.show()
    
    # Start the application event loop
    # sys.exit(app.exec_())
    
def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
    
if __name__ == "__main__":
   GraphicalUserInterface()