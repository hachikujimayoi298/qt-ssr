from typing import Union

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QTextCursor, QKeySequence, QKeyEvent
from PyQt5.QtWidgets import QPlainTextEdit


class REPLTextEdit(QPlainTextEdit):

    push_command = pyqtSignal(str)

    def __init__(self, multi_line_mode=False, multi_line_return=QKeySequence.InsertLineSeparator, *args, **kwargs):
        super(REPLTextEdit, self).__init__(*args, **kwargs)
        self.prompted: bool = False
        self.cursor_after_prompt: Union[QTextCursor, None] = None
        self.prompt: Union[str, None] = None
        self.multi_line_mode: bool = multi_line_mode
        self.multi_line_return: QKeySequence.StandardKey = multi_line_return
        self.multi_line: bool = False
        self.history: [(str, bool)] = []

        self.cursorPositionChanged.connect(self.checkEditable)

    @pyqtSlot(str, bool)
    def prompt(self, prompt: str, multi_line: bool):
        self.prompted = True
        self.prompt = prompt
        self.multi_line = multi_line
        self.appendPlainText(prompt)
        self.moveCursor(QTextCursor.End)
        self.cursor_after_prompt = self.textCursor()
        self.checkEditable()

    def getCommand(self):
        cursor = QTextCursor(self.cursor_after_prompt)
        cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
        return cursor.selectedText()

    @pyqtSlot()
    def checkEditable(self):
        """
        Check if the REPL accepts input set it to be editable if so
        :return: whether the REPL accepts input
        """
        editable = self.prompted \
            and self.textCursor().position() >= self.cursor_after_prompt.position() \
            and self.textCursor().anchor() >= self.cursor_after_prompt.position()
        self.setReadOnly(not editable)
        return editable

    def keyPressEvent(self, e: QKeyEvent):
        if e.matches(QKeySequence.MoveToPreviousLine):
            pass
        elif e.matches(QKeySequence.MoveToNextLine):
            pass
        elif e.matches(QKeySequence.Paste):
            pass
        elif e.matches(QKeySequence.InsertParagraphSeparator):
            if not self.multi_line_mode:
                cmd = self.getCommand()
                self.push_command.emit(cmd)
                self.prompted = False
                self.checkEditable()
            else:
                super().keyPressEvent(e)
        elif e.matches(self.multi_line_return):
            if self.multi_line_mode:
                cmd = self.getCommand()
                cmd.replace('\u2029', '\n')
                self.push_command.emit(cmd)
                self.prompted = False
                self.checkEditable()
        else:
            super().keyPressEvent(e)

