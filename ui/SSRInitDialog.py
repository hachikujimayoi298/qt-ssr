import os

from PyQt5.QtWidgets import *

from ui.SSRInstallDialog import SSRInstallDialog
from ui.generated.SSRInitDialog import Ui_InitDialog


class SSRInitDialog(QDialog, Ui_InitDialog):

    def __init__(self, *args, **kwargs):
        super(QDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.browse_ssr_folder)

        self.path = self.set_default_path()
        self.accepted.connect(self.install)

    def set_default_path(self):
        home = os.environ['HOME']
        default_path = os.path.join(home, '.config')
        self.lineEdit.setText(default_path)
        return default_path

    def browse_ssr_folder(self):
        path = QFileDialog.getExistingDirectory(self, directory=self.lineEdit.text())
        if path:
            self.lineEdit.setText(path)
            self.path = path

    def install(self):
        dlg = SSRInstallDialog(path=self.path)
        dlg.exec_()
