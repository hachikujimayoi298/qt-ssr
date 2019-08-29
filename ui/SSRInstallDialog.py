import traceback

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot, QThreadPool, QSettings
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QDialog, QDialogButtonBox

from ui.generated.SSRInstallDialog import Ui_SSRInstallDialog
from utils import init_ssr_at


class SSRInstallSignals(QObject):
    done = pyqtSignal()
    stderr = pyqtSignal(str)
    stdout = pyqtSignal(str)


class SSRInstallThread(QRunnable):

    def __init__(self, path, *args, **kwargs):
        super(SSRInstallThread, self).__init__()
        self.path = path
        self.args = args
        self.kwargs = kwargs
        self.signals = SSRInstallSignals()

    # noinspection PyBroadException
    @pyqtSlot()
    def run(self):
        try:
            init_ssr_at(self.path, self.signals)
        except Exception as e:
            self.signals.stderr.emit(str(e))
            self.signals.stderr.emit(traceback.format_exc())

        self.signals.done.emit()


class SSRInstallDialog(QDialog, Ui_SSRInstallDialog):

    def __init__(self, *args, path, **kwargs):
        super(QDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
        self.threadPool = QThreadPool()
        self.path = path
        self.installThread = SSRInstallThread(self.path)
        self.installThread.signals.stderr.connect(self.display_stderr)
        self.installThread.signals.stdout.connect(self.display_stdout)
        self.installThread.signals.done.connect(self.finalize)
        self.threadPool.start(self.installThread)

    def display_stderr(self, text):
        self.textEdit.moveCursor(QTextCursor.End)
        cursor = self.textEdit.textCursor()
        fmt = cursor.charFormat()
        fmt.setForeground(QtCore.Qt.red)
        cursor.setCharFormat(fmt)
        cursor.insertText(text)

    def display_stdout(self, text):
        self.textEdit.moveCursor(QTextCursor.End)
        cursor = self.textEdit.textCursor()
        fmt = cursor.charFormat()
        fmt.setForeground(QtCore.Qt.black)
        cursor.setCharFormat(fmt)
        cursor.insertText(text)

    def finalize(self):
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
