# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './SSRInstallDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SSRInstallDialog(object):
    def setupUi(self, SSRInstallDialog):
        SSRInstallDialog.setObjectName("SSRInstallDialog")
        SSRInstallDialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(SSRInstallDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(SSRInstallDialog)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(SSRInstallDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SSRInstallDialog)
        self.buttonBox.accepted.connect(SSRInstallDialog.accept)
        self.buttonBox.rejected.connect(SSRInstallDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SSRInstallDialog)

    def retranslateUi(self, SSRInstallDialog):
        _translate = QtCore.QCoreApplication.translate
        SSRInstallDialog.setWindowTitle(_translate("SSRInstallDialog", "Dialog"))
