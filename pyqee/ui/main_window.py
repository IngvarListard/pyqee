import os

import mpv
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QToolBar

from pyqee.ui.resources import qrc_resources


CONFIG_DIR = os.environ.get('MPV_CONFIG_HOME')
RESPECT_USER_CONFIG = bool(os.environ.get('RESPECT_USER_CONFIG'))  # TODO change to get_bool_from_env


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_menu_bar()
        self._create_toolbars()
        self.setWindowTitle("Pyqee")
        self.resize(600, 400)
        self.container = QWidget(self)
        self.setCentralWidget(self.container)
        self.container.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.container.setAttribute(Qt.WA_NativeWindow)
        player = mpv.MPV(
            wid=str(int(self.container.winId())),
            vo='x11',
            log_handler=print,
            loglevel='debug',
            input_default_bindings=True,
            input_vo_keyboard=True,
            player_operation_mode='pseudo-gui',
            script_opts='osc-layout=box,osc-seekbarstyle=bar,osc-deadzonesize=0,osc-minmousemove=3',
            osc=True,
            config='yes' if RESPECT_USER_CONFIG else 'no',
            config_dir=CONFIG_DIR
        )
        player.play('test.webm')

    def _create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('&File')
        video_menu = menu_bar.addMenu('&Video')
        audio_menu = menu_bar.addMenu('&Audio')
        subtitles_menu = menu_bar.addMenu('&Subtitles')
        help_menu = menu_bar.addMenu('&Help')

    def _create_toolbars(self):
        control_bar = QToolBar('Control')
        help_toolbar = self.addToolBar(Qt.BottomToolBarArea, control_bar)
