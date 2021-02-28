import locale
import sys

from PySide6.QtWidgets import *

from pyqee.ui.main_window import MainWindow

app = QApplication(sys.argv)

locale.setlocale(locale.LC_NUMERIC, 'C')


if __name__ == '__main__':
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
