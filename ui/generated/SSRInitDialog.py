# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './SSRInitDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InitDialog(object):
    def setupUi(self, InitDialog):
        InitDialog.setObjectName("InitDialog")
        InitDialog.resize(500, 133)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(InitDialog.sizePolicy().hasHeightForWidth())
        InitDialog.setSizePolicy(sizePolicy)
        InitDialog.setMinimumSize(QtCore.QSize(500, 133))
        InitDialog.setMaximumSize(QtCore.QSize(500, 133))
        self.verticalLayout = QtWidgets.QVBoxLayout(InitDialog)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.descriptionLabel = QtWidgets.QLabel(InitDialog)
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setObjectName("descriptionLabel")
        self.verticalLayout.addWidget(self.descriptionLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(InitDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(InitDialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(InitDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(InitDialog)
        self.buttonBox.accepted.connect(InitDialog.accept)
        self.buttonBox.rejected.connect(InitDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(InitDialog)

    def retranslateUi(self, InitDialog):
        _translate = QtCore.QCoreApplication.translate
        InitDialog.setWindowTitle(_translate("InitDialog", "Select SSR folder"))
        self.descriptionLabel.setText(_translate("InitDialog", "This folder will contain a copy of SSR python and the config file for the client when initialization finished. This will delete ALL of your configurations and servers."))
        self.pushButton.setText(_translate("InitDialog", "Browse..."))
