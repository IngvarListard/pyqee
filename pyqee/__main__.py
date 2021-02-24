import locale
import sys
import mpv

from PySide6.QtWidgets import *
from PySide6.QtCore import *


class Test(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.container = QWidget(self)
        self.setCentralWidget(self.container)
        self.container.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.container.setAttribute(Qt.WA_NativeWindow)
        player = mpv.MPV(wid=str(int(self.container.winId())),
                         vo='x11',
                         log_handler=print,
                         loglevel='debug',
                         input_default_bindings=True,
                         input_vo_keyboard=True)
        player.play('test.webm')


app = QApplication(sys.argv)

locale.setlocale(locale.LC_NUMERIC, 'C')


def main():
    win = Test()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
