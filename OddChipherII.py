# A Small executable based on PyQt5. Plays music and encodes secrets. // UC2DIN10 Registry testing
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QStatusBar
from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QIcon, QPixmap, QGuiApplication, QFont
from PyQt5.QtCore import Qt

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # Enable high DPI scaling
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)     # Use high DPI icons

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = '4F 44 44'
        self.left = 10
        self.top = 10
        self.width = 540
        self.height = 410
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.centerWindow()
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, 'a.png')
        self.setWindowIcon(QIcon(icon_path))
        
        self.show()
        
        # Status bar
        self.statusLabel = QStatusBar()
        self.setStatusBar(self.statusLabel)
        self.statusLabel.showMessage("Encoded with the top level cryptography algorithm ROT13.")
        
        # Music player setup
        self.setupMusicPlayer()
        self.show()
        
    # Centers window on screen
    def centerWindow(self):
        centerPoint = QGuiApplication.primaryScreen().availableGeometry().center()
        fg = self.frameGeometry()
        fg.moveCenter(centerPoint)
        self.move(fg.topLeft())
       
        # Logo / Header image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, 'odd.png')
        logoPixmap = QPixmap(image_path)
        if logoPixmap.isNull():
            self.statusLabel.showMessage("Failed to load logo image.")
        else:
            self.logo = QLabel(self)
            scaledLogo = logoPixmap.scaled(self.width - 20, 148, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo.setPixmap(scaledLogo)
            self.logo.setAlignment(Qt.AlignCenter)
            self.logo.resize(scaledLogo.size())
            self.logo.move((self.width - scaledLogo.width()) // 2, 20)
            yOffset = self.logo.height() + 20  # Adjust yOffset based on the logo's new height

        # UI elements below the logo
        self.setupUIBelowLogo(yOffset)

    def setupUIBelowLogo(self, yOffset):
        boldFont = QFont()
        boldFont.setBold(True)
        # Label for input box
        KeyLabel = QLabel('State your Key:', self)
        KeyLabel.setFont(boldFont)
        KeyLabel.move(80, yOffset + 15)  # Positioned above the input box
        # Label for output box
        cipherLabel = QLabel('Get your Code:', self)
        cipherLabel.setFont(boldFont)
        cipherLabel.move(80, yOffset + 90)  # Positioned above the output box  
        yOffset += 20 # Adjust yOffset for the actual input boxes

        # Input Box and placehodlde text
        yOffset += 30
        self.inputBox = QLineEdit(self)
        self.inputBox.setPlaceholderText('Top Secret Message')
        self.inputBox.move(80, yOffset)
        self.inputBox.resize(380, 30)

        # Output Box and placeholder text
        yOffset += 70
        self.outputBox = QLineEdit(self)
        self.outputBox.setPlaceholderText(' Code comes here...')
        self.outputBox.move(80, yOffset)
        self.outputBox.resize(380, 30)
        self.outputBox.setReadOnly(True)

        # Buttons Generate and Clear
        yOffset += 40 
        self.generateButton = QPushButton('Generate', self)
        self.generateButton.move(80, yOffset)

        self.clearButton = QPushButton('Clear', self)
        self.clearButton.move(190, yOffset)  # Adjust to be slightly to the right of 'Generate'

        # Info text(s)
        yOffset += 5
        additionalTextLabel = QLabel('kthxbye :)', self)
        additionalTextLabel.move(400, yOffset)

        # Connecting button signals to slots
        self.generateButton.clicked.connect(self.on_generate)
        self.clearButton.clicked.connect(self.on_clear)

    def setupMusicPlayer(self):
        self.player = QMediaPlayer()
        music_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "b.mp3")
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(music_path)))
        self.player.setVolume(50)
        self.player.play()
        
        # Connect the mediaStatusChanged signal to the slot to check for EndOfMedia
        self.player.mediaStatusChanged.connect(self.checkMediaStatus)

    def checkMediaStatus(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.player.setPosition(0)  # Rewind to start
            self.player.play()  # Play again

    @pyqtSlot()
    def on_generate(self):
        input_text = self.inputBox.text()
        output_text = self.rot13(input_text)
        self.outputBox.setText(output_text)

    @pyqtSlot()
    def on_clear(self):
        self.inputBox.clear()
        self.outputBox.clear()

    # ROT13 function, including a highly advanced obfuscation of the NO letters.
    def rot13(self, s):
        result = ""
        for v in s:
            c = ord(v)
            if 'a' <= v <= 'z':
                result += chr((c - ord('a') + 13) % 26 + ord('a'))
            elif 'A' <= v <= 'Z':
                result += chr((c - ord('A') + 13) % 26 + ord('A'))
            elif '0' <= v <= '9':
                result += chr((c - ord('0') + 5) % 10 + ord('0'))
            elif v == 'æ':
                result += 'ø'
            elif v == 'ø':
                result += 'å'
            elif v == 'å':
                result += 'æ'
            elif v == 'Æ':
                result += 'Ø'
            elif v == 'Ø':
                result += 'Å'
            elif v == 'Å':
                result += 'Æ'
            else:
                result += v
        return result
  
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
