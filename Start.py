import importlib
import sys

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication

import db_params
from ui.SSRInitDialog import SSRInitDialog

EXIT_CODE_REBOOT = -12345678
EXIT_CODE_RESET = -12345679

if __name__ == '__main__':
    exit_code = EXIT_CODE_REBOOT

    while exit_code == EXIT_CODE_REBOOT or exit_code == EXIT_CODE_RESET:
        app = QApplication(sys.argv)
        QApplication.setApplicationName('Qt-ShadowsocksR')
        QApplication.setOrganizationName('HachikujiMayoi298')

        settings = QSettings()
        path = settings.value('SSR/db_path')
        if exit_code == EXIT_CODE_RESET or not path:
            dlg = SSRInitDialog()
            dlg.exec()
            settings.sync()
            path = settings.value('SSR/db_path')

        db_params.path = path
        if not path:
            app.exit(1)

        if exit_code == EXIT_CODE_REBOOT or exit_code == EXIT_CODE_RESET:
            import db
            importlib.reload(db)

        from ui.MainWindow import MainWindow

        window = MainWindow()
        window.show()
        exit_code = app.exec()
        app = None

    sys.exit(exit_code)
