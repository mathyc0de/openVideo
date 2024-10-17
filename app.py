from __future__ import annotations
import sys
from PySide6.QtCore import QStandardPaths, Qt, Slot, QUrl, QSize, QRect, Qt, QTimer
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog, QLabel, QVBoxLayout, QWidget,
                               QMainWindow, QSlider, QStyle, QToolBar)
from PySide6.QtMultimedia import (QAudioOutput, QMediaFormat,
                                  QMediaPlayer)
from UI import VideoWidget, ToolBar, MenuBar
from editor import VideoEditor



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
        self.setAcceptDrops(True)
        self.resize(800, 600)
        self.initState()


    def initState(self):
        self._mime_types = get_supported_mime_types()
        self.video_widget = VideoWidget()
        self.player = self.video_widget.player
        self.tool_bar = ToolBar(tick_pos = self.video_widget.tickpos)
        self.tool_bar.play_action.triggered.connect(self.play)
        self.tool_bar.pause_action.triggered.connect(self.pause)
        self.tool_bar.stop_action.triggered.connect(self.stop)
        self.tool_bar.progress.sliderMoved.connect(lambda: self.video_widget.update_video(self.tool_bar.progress.value()))
        self.tool_bar.fullscreen_action.triggered.connect(self.fullscreen)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.tool_bar)
        self.menu_bar = MenuBar()
        self.menu_bar.open_action.triggered.connect(self.open)
        self.menu_bar.reverse_action.triggered.connect(self.reverse_video)
        self.menu_bar.save_action.triggered.connect(self.save_video)
        self.setMenuBar(self.menu_bar)
    
    def not_have_video(self): return self.player.playbackState() == QMediaPlayer.PlaybackState.StoppedState or not self.player.hasVideo()
    
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        firstURL = files[0]
        self.open(firstURL)
    
    @Slot()
    def play(self):
        self.video_widget.play()
        self.tool_bar.play()
    
    @Slot()
    def pause(self):
        self.video_widget.pause()
        self.tool_bar.pause()
    
    @Slot()
    def stop(self):
        self.video_widget.stop()
        self.tool_bar.stop()
        self.takeCentralWidget()

    @Slot()
    def fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    @Slot()
    def progress_handler(self):
        time = self.player.duration()
        self.tool_bar.set_progress_limit(time)
    
    @Slot()
    def increment_time(self):
        self.tickpos = self.player.position()
        self.tool_bar.progress.setValue(self.tickpos)

    @Slot()
    def reverse_video(self):
        if self.not_have_video(): return
        self.pause()
        url = self.player.source()
        path = url.toLocalFile() if isinstance(url, QUrl) else url.path()
        editor = VideoEditor(path)
        self.player.setSource(editor.reverse())
        self.player.pause()

    @Slot()
    def save_video(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.StoppedState: return
        self.pause()
        url = self.player.source()
        path = url.toLocalFile() if isinstance(url, QUrl) else url.path()
        VideoEditor.save_video(self.filename, url = path)


    @Slot()
    def open(self, draggedURL):
        self.takeCentralWidget()
        if (draggedURL):
            self.setCentralWidget(self.video_widget)
            url = draggedURL
            self.player.setSource(url)
            self.player.pause()
            self.filename = url.split('/')[-1]
            self.player.durationChanged.connect(self.progress_handler)
            self.player.positionChanged.connect(self.increment_time)
            self.tool_bar.play_action.setEnabled(True)
            return

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
            self.setCentralWidget(self.video_widget)
            url = file_dialog.selectedUrls()[0]
            self.filename = url.fileName()
            self.player.durationChanged.connect(self.progress_handler)
            self.player.positionChanged.connect(self.increment_time)
            self.player.setSource(url)
            self.player.pause()
            self.tool_bar.play_action.setEnabled(True)