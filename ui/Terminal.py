from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QDialog

from ui.generated.Terminal import Ui_TerminalDialog
from utils.QPyConsole import QPyConsole


class Terminal(QDialog, Ui_TerminalDialog):

    def __init__(self, *args, **kwargs):
        super(Terminal, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.terminalThread = QThread(parent=self)
        self.terminalThread.start()
        self.terminal = QPyConsole(parent=self.terminalThread)
        self.terminal.moveToThread(self.terminalThread)
