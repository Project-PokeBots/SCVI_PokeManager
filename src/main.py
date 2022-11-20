import sys, socket, random, string, binascii, re
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QComboBox, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot
from px8parse import PX8


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "SCVI_PokéManager"
        self.width = 300
        self.height = 50
        self.font = "Arial"
        self.font_size = 12
        self.SwitchIP = None
        self.slot = 1
        self.offset = "0x42FD510 0xA90 0x9B0 0x0"
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setMinimumSize(self.width, self.height)
        self.setFont(QFont(self.font, self.font_size))

        # Create buttons for dump, inject, and IP submit
        self.dump = QPushButton("Dump", self)
        self.dump.clicked.connect(self.dump_clicked)
        self.dump.resize(100, 50)
        self.dump.move(0, 0)

        self.inject = QPushButton("Inject", self)
        self.inject.clicked.connect(self.inject_clicked)
        self.inject.resize(100, 50)
        self.inject.move(100, 0)

        self.submit = QPushButton("Connect", self)
        self.submit.clicked.connect(self.on_ip)
        self.submit.resize(100, 60)
        self.submit.move(200, 50)

        # Create dropdown to select slot location
        self.combo = QComboBox(self)
        self.combo.addItems([str(e) for e in range(1, 31)])
        self.combo.currentTextChanged.connect(self.combo_clicked)
        self.combo.resize(100, 50)
        self.combo.move(200, 0)

        # Create label
        self.label = QLabel(self)
        self.label.setText("Switch IP:")
        self.label.resize(100, 50)
        self.label.move(0, 50)

        # Create text input boxes for IP
        self.inp = QLineEdit(self)
        self.inp.resize(100, 60)
        self.inp.move(100, 50)

        self.show()

    @pyqtSlot()
    def dump_clicked(self):
        alert = QMessageBox()
            #address = 0x42FD510 0xA90 0x9B0 0x0 + ((1- 1) * 30 * 344) + ((self.slot - 1) * 344)
        self.switch.sendall(f"pointerPeek 344 {self.offset}\r\n".encode())
        pokemon = (self.switch.recv(689))[0:-1]
        name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        with open(f"{name}.ek9", "wb+") as writer:
            writer.write(binascii.unhexlify(pokemon))
        alert.setWindowTitle(f"Successfully dumped to {name}.ek9")
        with open(f"{name}.ek9", "rb") as reader:
            alert.setText(str(PX8(buf = reader.read())))

        alert.exec()

    def inject_clicked(self):
        alert = QMessageBox()
        try:
            with open("inject.ek9", "rb") as f:
                pk = f.read().hex()
        except:
            alert.setWindowTitle("[!] No file")
            alert.setText('No file named "inject.ek9" found!')
            return alert.exec()
        self.switch.sendall(f"pointerPoke 0x{pk} {self.offset}\r\n".encode())
        alert.setWindowTitle("Successfully injected")
        alert.setText(f"Pokémon injected into slot {self.slot} {self.SwitchIP}!")

        alert.exec()

    def combo_clicked(self, text):
        global slot
        slot = int(text)

    def on_ip(self):
        text = self.inp.text()
        if not re.match(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", text):
            alert = QMessageBox()
            alert.setWindowTitle("[!] Error")
            alert.setText(f"Invalid IP set!")
            alert.exec()
        else:
            self.SwitchIP = str(text)
            alert = QMessageBox()
            alert.setWindowTitle("Switch IP")
            alert.setText(f"Switch IP set to {self.SwitchIP}!")
            self.switch = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.switch.connect((self.SwitchIP, 6000))
            alert.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
