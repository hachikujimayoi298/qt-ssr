from PyQt5 import QtCore
from PyQt5.QtSql import QSqlRelationalTableModel
from PyQt5.QtWidgets import *

from Start import EXIT_CODE_RESET
from db import *
from ui.generated.MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # toolbar actions
        self.actionInitialize_Reset.triggered.connect(self.open_init_dialog)

        self.model = QSqlRelationalTableModel(self, db)
        self.model.setTable(Server.__tablename__)
        logical_headers = ['ID', 'Server', 'Port', 'Password', 'Encryption', 'Protocol', 'Protocol Params',
                           'Obfuscation', 'Obfuscation Params', 'Remark', 'Group']
        visual_headers = logical_headers.copy()
        displayed_columns = ['Remark', 'Server', 'Port', 'Group']
        for idx, header in enumerate(logical_headers):
            self.model.setHeaderData(idx, QtCore.Qt.Horizontal, header)

        self.tableView.setModel(self.model)
        for displayed_header in reversed(displayed_columns):
            idx = visual_headers.index(displayed_header)
            self.tableView.horizontalHeader().moveSection(idx, 0)
            visual_headers.pop(idx)
            visual_headers.insert(0, displayed_header)

        for idx, header in enumerate(logical_headers):
            if header not in displayed_columns:
                self.tableView.horizontalHeader().setSectionHidden(idx, True)


    @staticmethod
    def open_init_dialog():
        qApp.exit(EXIT_CODE_RESET)

    def add_server(self, server: dict):
        pass

    def bulk_add_server(self, servers: [dict]):
        pass

    def update_server(self, server: Server):
        pass

    def remove_server(self, server: Server):
        pass
