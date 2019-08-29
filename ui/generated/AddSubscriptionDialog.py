# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './AddSubscriptionDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddSubScrptionDialog(object):
    def setupUi(self, AddSubScrptionDialog):
        AddSubScrptionDialog.setObjectName("AddSubScrptionDialog")
        AddSubScrptionDialog.resize(500, 76)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddSubScrptionDialog.sizePolicy().hasHeightForWidth())
        AddSubScrptionDialog.setSizePolicy(sizePolicy)
        AddSubScrptionDialog.setMinimumSize(QtCore.QSize(500, 76))
        AddSubScrptionDialog.setMaximumSize(QtCore.QSize(500, 76))
        self.verticalLayout = QtWidgets.QVBoxLayout(AddSubScrptionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(AddSubScrptionDialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtWidgets.QLineEdit(AddSubScrptionDialog)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.verticalLayout.addLayout(self.formLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddSubScrptionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AddSubScrptionDialog)
        self.buttonBox.accepted.connect(AddSubScrptionDialog.accept)
        self.buttonBox.rejected.connect(AddSubScrptionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddSubScrptionDialog)

    def retranslateUi(self, AddSubScrptionDialog):
        _translate = QtCore.QCoreApplication.translate
        AddSubScrptionDialog.setWindowTitle(_translate("AddSubScrptionDialog", "Import from Subscription"))
        self.label.setText(_translate("AddSubScrptionDialog", "Subscription URL:"))
