from __future__ import annotations
import sys
from PySide6.QtCore import QStandardPaths, Qt, Slot, QUrl, QSize, QRect
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog, QLabel, QVBoxLayout,
                               QMainWindow, QSlider, QStyle, QToolBar)
from PySide6.QtMultimedia import (QAudioOutput, QMediaFormat,
                                  QMediaPlayer)
from PySide6.QtMultimediaWidgets import QVideoWidget
from editor import VideoEditor
import os.path


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
        self.resize(800, 600)
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

    def resume(self):
        if self._player.playbackState() != QMediaPlayer.PlaybackState.PausedState and self._player.hasVideo():
            self.removeToolBar(self.tool_bar)
            self._tool_bar(True)
            self._player.pause()

        elif self._player.hasVideo():
            self.removeToolBar(self.tool_bar)
            self._tool_bar(False)
            self._player.play()

    
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
        self.reverse(menu)
        self.save(menu)

    
    def reverse(self, menu):
        icon = QIcon.fromTheme(QIcon.ThemeIcon.MediaSeekBackward)
        reverse_action = QAction(icon, "&Reverter...", self,
                              shortcut=QKeySequence.Open, triggered=self._reverse_video)
        menu.addAction(reverse_action)
    
    def save(self, menu):
        icon = QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave)
        save_action = QAction(icon, "&Salvar...", self,
                              shortcut=QKeySequence.Open, triggered=self._save_video)
        menu.addAction(save_action)

    
    def _tool_bar(self, paused: bool = True):
        self.tool_bar = QToolBar()
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.tool_bar)
        if paused:
            self._play_btn()
            self._stop_btn()
        else:
            self._pause_btn()
            self._stop_btn()



    def _play_btn(self):
        icon = QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart,
                            self.style().standardIcon(QStyle.SP_MediaPlay))
        self._play_action = self.tool_bar.addAction(icon, "Play")
        self._play_action.triggered.connect(self.resume)
    
    def _pause_btn(self):
        icon = QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackPause,
                            self.style().standardIcon(QStyle.SP_MediaPause))
        self._pause_action = self.tool_bar.addAction(icon, "Pause")
        self._pause_action.triggered.connect(self.resume)
    
    def _stop_btn(self):
        icon = QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStop,
                        self.style().standardIcon(QStyle.SP_MediaStop))
        self._stop_action = self.tool_bar.addAction(icon, "Stop")
        self._stop_action.triggered.connect(self._ensure_stopped)



    @Slot()
    def _ensure_stopped(self):
        if self._player.playbackState() != QMediaPlayer.PlaybackState.StoppedState:
            self._player.stop()

    @Slot()
    def _reverse_video(self):
        self._ensure_stopped()
        if self._player.hasVideo():
            url = self._player.source()
            path = url.toLocalFile() if isinstance(url, QUrl) else url.path()
            editor = VideoEditor(path)
            self._player.setSource(editor.reverse())
            self._player.pause()

    @Slot()
    def _save_video(self):
        self._ensure_stopped()
        if self._player.hasVideo():
            VideoEditor.save_video(self.filename)


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

        default_mimetype = MP4
        if default_mimetype in self._mime_types:
            file_dialog.selectMimeTypeFilter(default_mimetype)

        movies_location = QStandardPaths.writableLocation(QStandardPaths.MoviesLocation)
        file_dialog.setDirectory(movies_location)
        if file_dialog.exec() == QDialog.Accepted:
            url = file_dialog.selectedUrls()[0]
            self.filename = url.fileName()
            self._player.setSource(url)
            self._player.pause()

App()