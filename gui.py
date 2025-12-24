import sys
import os

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QRadioButton, QLineEdit, QCheckBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from src import FernetEncrypter
from src import logger


class QtEncryptor(QThread):
    signal = pyqtSignal(dict)

    def __init__(self, path:str, encode:bool, code_lvl:bool) -> None:
        super().__init__()
        self.path = path
        self.encode = encode    
        self.code_lvl = code_lvl
    
    def run(self) -> None:
        enc = FernetEncrypter('key.k')
        self.status = enc.folder_cryptor(self.path, encode=self.encode, code_lvl=self.code_lvl)
        self.signal.emit(self.status)


class MyWindow(QWidget):

    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle('Encryptor')
        # self.setGeometry(700, 300, 500, 250)
        self.setFixedSize(500, 250)

        self.logger = logger(log_name='pyQTWindow')
        self.path = ''
        self.encode = True
        self.code_lvl = False
        self.status = 'Not Set'

        self.init_ui()

    def init_ui(self):
        self.add_text('Recursively encrypts and decrypts the given path', QFont("Times", 10, QFont.Bold), 10, 35, Qt.AlignCenter)
        self.add_path_textbox()
        self.add_radio_button()
        self.add_checkbox()
        self.add_button()
        self.log_text = self.add_text('--------Check logs--------', QFont("Times", 10, QFont.Bold), 275, 200, Qt.AlignCenter, hidden=True)

    def add_text(self, text, qfont, left, top, qalign, hidden=False):
        label1 = QLabel(text, self)
        label1.setFont(qfont)
        label1.move(left, top)  # left, top
        label1.setAlignment(qalign)
        label1.setHidden(hidden)
        return label1

    def add_path_textbox(self):
        self.add_text('Encrption Path', QFont("Times", 8, QFont.System), 35, 105, Qt.AlignRight)
        self.t1 = QLineEdit(self)
        self.t1.setToolTip('Sets the path for recurive encryption')
        self.t1.move(150, 100)

        self.t1.setEnabled(True)

    def add_radio_button(self):
        # add tooltip
        self.r1 = QRadioButton('Encryption', self)
        self.r2 = QRadioButton('Decryption', self)
        self.r1.setChecked(True)
        self.r1.move(70, 150)
        self.r2.move(170, 150)

        self.r1.toggled.connect(lambda: self.button_state(self.r1))
        self.r2.toggled.connect(lambda: self.button_state(self.r2))

    def add_checkbox(self):
        self.c1 = QCheckBox('Rename Only', self)
        self.c1.setToolTip('If checked, only the file name gets encrypted;\nIf unchecked, the whole file is encrypted, making it unreadable')
        self.c1.setChecked(True)
        self.c1.move(300, 150)
        self.c1.toggled.connect(lambda: self.button_state(self.c1)) 

    def add_button(self):
        # buttons 
        self.button = QPushButton('Start Cryption', self)
        self.button.move(150, 200)
        self.button.clicked.connect(lambda: self.on_click())
    
    # ---------- GUI states handler ----------
    def button_state(self, b):
        # for debugging
        # if b.isChecked():
        #     print(b.text() + " is selected")
        # else:
        #     print(b.text() + " is deselected")

        # make a provision to delete the content of widgets
        if b.text() == 'Encryption':
            self.encode = True
        
        if b.text() == 'Decryption':
            self.encode = False

        if b.text() == 'Rename Only' and b.isChecked():
            self.code_lvl = False
        
        if b.text() == 'Rename Only' and not b.isChecked():
            self.code_lvl = True

        self.logger.info(f'Button state change: {b.text()} to {b.isChecked()}')

    def on_click(self):

        if self.button.text() == 'Start Cryption':
            
            self.logger.info(f'Cryption Started-> encryption:{self.encode}, rename:{not self.code_lvl}, path:{self.t1.text()}')
            self.path = r'{}'.format(self.t1.text())
            
            if os.path.exists(self.path):
                self.t1.setEnabled(False)
                self.r1.setEnabled(False)
                self.r2.setEnabled(False)
                self.c1.setEnabled(False)
                self.encrypt_thread = QtEncryptor(self.path, self.encode, self.code_lvl)
                self.encrypt_thread.signal.connect(self.get_encrypt_process)
                self.encrypt_thread.start()
                self.button.setText("Kill Task")
                self.log_text.setText('Running - Check logs')
            else:
                self.log_text.setText('Incorrect path, Try Again!')
                self.logger.warning('Incorrect path, Try Again!')

        elif self.button.text() == 'Done':
            self.button.setEnabled(False)
            self.log_text.setText(f"Succ:{self.status['success']},Fail:{self.status['fail']}")
            self.logger.info('Cryption Successful')
        else:
            self.encrypt_thread.terminate()
            self.button.setText("Restart App")
            self.button.setEnabled(False)
            self.log_text.setText('! Terminated Check logs !')
            self.logger.warning('Cryption Terminated in between')

        self.log_text.setHidden(False)

    def get_encrypt_process(self, status):
        # binded to pyqtSignal to get success status

        self.status = status
        self.logger.info(f'Encryption successfull, Status:{self.status}')
        self.button.setText("Done")
        self.on_click()
        

# Run the main function if this script is executed
if __name__ == '__main__':
    app = QApplication(sys.argv)  # Create an application instance
    window = MyWindow()           # Create an instance of the window
    window.show()                 # Show the window
    sys.exit(app.exec_())         # Start the application's event loop
