import os

import mpv
from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMainWindow, QWidget, QToolBar, QWidgetAction, QVBoxLayout, QMenu, QSlider, QHBoxLayout, \
    QFileDialog

from pyqee.ui.resources import qrc_resources


CONFIG_DIR = os.environ.get('MPV_CONFIG_HOME')
RESPECT_USER_CONFIG = bool(os.environ.get('RESPECT_USER_CONFIG'))  # TODO change to get_bool_from_env


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pyqee")
        self.resize(600, 400)
        self.container = QWidget(self)

        self.setCentralWidget(self.container)

        self.container.setAttribute(Qt.WA_DontCreateNativeAncestors)
        self.container.setAttribute(Qt.WA_NativeWindow)

        self._create_actions()
        self._create_menu_bar()
        self._create_toolbars()
        self._create_context_menu()


        player = mpv.MPV(
            wid=str(int(self.container.winId())),
            vo='x11',
            log_handler=print,
            # loglevel='debug',
            input_default_bindings=True,
            input_vo_keyboard=True,
            player_operation_mode='pseudo-gui',
            script_opts='osc-layout=box,osc-seekbarstyle=bar,osc-deadzonesize=0,osc-minmousemove=3',
            osc=True,
            config='yes' if RESPECT_USER_CONFIG else 'no',
            config_dir=CONFIG_DIR
        )

        def test_(*args):
            if args[0] == 'dm':
                self.menu_.exec_(self.container.cursor().pos())

        @player.property_observer('time-pos')
        def barr(n, v):
            if v is not None:
                self.progress_slider.setValue(int(v))

        @player.on_key_press('f')
        def fullscreen():
            if self.windowState() & QtCore.Qt.WindowFullScreen:
                self.showNormal()
            else:
                print(456)
                self.showFullScreen()

        # player.register_event_callback()
        player.register_key_binding('MBTN_LEFT', 'cycle fullscreen')
        player.register_key_binding('MBTN_RIGHT', test_)
        # player.event_callback()
        player.play('test.webm')

    def _create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(self.open_action)

        video_menu = menu_bar.addMenu('&Video')
        video_menu.addAction(self.play_action)
        video_menu.addAction(self.pause_action)
        video_menu.addAction(self.next_track_action)
        video_menu.addAction(self.prev_track_action)

        audio_menu = menu_bar.addMenu('&Audio')
        subtitles_menu = menu_bar.addMenu('&Subtitles')
        help_menu = menu_bar.addMenu('&Help')

    def _create_toolbars(self):

        control_bar = QToolBar('Control')
        self.control_bar = control_bar
        control_bar.addActions((
            self.play_action,
            self.pause_action,
            self.next_track_action,
            self.prev_track_action,
        ))
        self.addToolBar(Qt.BottomToolBarArea, control_bar)

        self._create_progress_slider()

    def _create_actions(self):
        self.open_action = QAction(QIcon.fromTheme('document-open'), '&Open...', self)
        self.open_action.triggered.connect(self._open_file_name_dialog)
        self.play_action = QAction(QIcon.fromTheme('media-playback-start'), '&Play', self)
        self.pause_action = QAction(QIcon.fromTheme('media-playback-pause'), '&Pause', self)
        self.stop_action = QAction(QIcon.fromTheme('media-playback-stop'), '&Stop', self)
        self.next_track_action = QAction(QIcon.fromTheme('media-seek-forward'), '&Next track', self)
        self.prev_track_action = QAction(QIcon.fromTheme('media-seek-backward'), '&Prev track', self)

    def _create_context_menu(self):
        self.menu_ = QMenu()
        a = self.menu_.addAction("Test1")
        b = self.menu_.addAction("Test2")

    def _create_progress_slider(self):
        s = QSlider(Qt.Horizontal, self.control_bar)
        self.progress_slider = s
        s.setFocusPolicy(Qt.NoFocus)
        self.control_bar.addWidget(s)

        s.setRange(0, 100)

        s.valueChanged.connect(lambda *x, **y: print(x, y))

    def _open_file_name_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py)", options=options)
        if file_name:
            print(file_name)