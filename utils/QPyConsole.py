import sys
from code import InteractiveConsole

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


# inspired and modified from https://gist.github.com/daegontaven/a986a2241e15e95be7489f443e79fb7f by daegontaven
class QPyConsole(QObject, InteractiveConsole):
    push_command = pyqtSignal(str)
    multi_line = pyqtSignal()
    output = pyqtSignal(str)
    error = pyqtSignal(str)

    class EmitStream(object):

        def __init__(self, signal):
            self.signal = signal

        def write(self, data):
            self.signal.emit(data)

    def __init__(self, parent=None, locals=None, filename="<console>"):
        super(QPyConsole, self).__init__(parent)
        InteractiveConsole.__init__(self, locals, filename)
        self.stdout = self.EmitStream(self.output)
        self.stderr = self.EmitStream(self.error)
        self.push_command.connect(self.push_line)

    def runcode(self, code):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        sys.excepthook = sys.__excepthook__
        result = InteractiveConsole.runcode(self, code)
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        return result

    @pyqtSlot(str)
    def push_line(self, cmd):
        if self.push(cmd):
            self.multi_line.emit()

    def write(self, data):
        self.error.emit(data)

