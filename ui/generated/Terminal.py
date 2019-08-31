# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Terminal.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TerminalDialog(object):
    def setupUi(self, TerminalDialog):
        TerminalDialog.setObjectName("TerminalDialog")
        TerminalDialog.resize(592, 392)
        self.verticalLayout = QtWidgets.QVBoxLayout(TerminalDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = REPLTextEdit(TerminalDialog)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)

        self.retranslateUi(TerminalDialog)
        QtCore.QMetaObject.connectSlotsByName(TerminalDialog)

    def retranslateUi(self, TerminalDialog):
        _translate = QtCore.QCoreApplication.translate
        TerminalDialog.setWindowTitle(_translate("TerminalDialog", "Debug Terminal"))
from ui.widgets.REPLTextEdit import REPLTextEdit
