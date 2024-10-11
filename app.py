from __future__ import annotations
import sys
from PySide6.QtCore import QStandardPaths, Qt, Slot
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog,
                               QMainWindow, QSlider, QStyle, QToolBar)
from PySide6.QtMultimedia import (QAudioOutput, QMediaFormat,
                                  QMediaPlayer)
from PySide6.QtMultimediaWidgets import QVideoWidget



AVI = "video/x-msvideo"  # AVI


MP4 = 'video/mp4'


def get_supported_mime_types():
    result = []
    for f in QMediaFormat().supportedFileFormats(QMediaFormat.Decode):
        mime_type = QMediaFormat(f).mimeType()
        result.append(mime_type.name())
    return result



class App:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.window = HomePage()
        self.window.show()
        self.app.exec()


class HomePage(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenVideo")
        self._setupUI()
        self.setCentralWidget(self._video_widget)
    
    def _setupUI(self):
        self._video_player()
        self._tool_bar()
        self._menu_bar()
    
    def _video_player(self):
        self._audio_output = QAudioOutput()
        self._player = QMediaPlayer()
        self._player.setAudioOutput(self._audio_output)
        self._video_widget = QVideoWidget()
        self._player.setVideoOutput(self._video_widget)
        self.setCentralWidget(self._video_widget)
        self._mime_types = []
    
    def _menu_bar(self):
        self._file_section()
        self._editor_section()

    def _file_section(self):
        menu = self.menuBar().addMenu("&File")
        icon = QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen)
        open_action = QAction(icon, "&Open...", self,
                              shortcut=QKeySequence.Open, triggered=self.open)
        menu.addAction(open_action)
    
    def _editor_section(self):
        menu = self.menuBar().addMenu("&Edit")
        icon = QIcon.fromTheme(QIcon.ThemeIcon.MediaSeekBackward)
        reverse_action = QAction(icon, "&Reverter...", self,
                              shortcut=QKeySequence.Open, triggered=self._reverse_video)
        menu.addAction(reverse_action)

    
    def _tool_bar(self):
        tool_bar = QToolBar()
        self.addToolBar(tool_bar)
        self._play_btn(tool_bar)
        self._pause_btn(tool_bar)
        self._stop_btn(tool_bar)


    def _play_btn(self, tool_bar):
        icon = QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart,
                            self.style().standardIcon(QStyle.SP_MediaPlay))
        self._play_action = tool_bar.addAction(icon, "Play")
        self._play_action.triggered.connect(self._player.play)
    
    def _pause_btn(self, tool_bar):
        icon = QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackPause,
                            self.style().standardIcon(QStyle.SP_MediaPause))
        self._pause_action = tool_bar.addAction(icon, "Pause")
        self._pause_action.triggered.connect(self._player.pause)
    
    def _stop_btn(self, tool_bar):
        icon = QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStop,
                        self.style().standardIcon(QStyle.SP_MediaStop))
        self._stop_action = tool_bar.addAction(icon, "Stop")
        self._stop_action.triggered.connect(self._ensure_stopped)



    @Slot()
    def _ensure_stopped(self):
        if self._player.playbackState() != QMediaPlayer.StoppedState:
            self._player.stop()

    @Slot()
    def _reverse_video(self):
        self._ensure_stopped()
        if self._player.hasVideo():
            path = self._player.source().path()
            editor = VideoEditor(path)
            self._player.setSource(editor.reverse())
            self._player.play()


    @Slot()
    def open(self):
        self._ensure_stopped()
        file_dialog = QFileDialog(self)

        is_windows = sys.platform == 'win32'
        if not self._mime_types:
            self._mime_types = get_supported_mime_types()
            if (is_windows and AVI not in self._mime_types):
                self._mime_types.append(AVI)
            elif MP4 not in self._mime_types:
                self._mime_types.append(MP4)

        file_dialog.setMimeTypeFilters(self._mime_types)

        default_mimetype = AVI if is_windows else MP4
        if default_mimetype in self._mime_types:
            file_dialog.selectMimeTypeFilter(default_mimetype)

        movies_location = QStandardPaths.writableLocation(QStandardPaths.MoviesLocation)
        file_dialog.setDirectory(movies_location)
        if file_dialog.exec() == QDialog.Accepted:
            url = file_dialog.selectedUrls()[0]
            self._player.setSource(url)
            self._player.play()

App()