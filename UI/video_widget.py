from __future__ import annotations
import sys
from PySide6.QtCore import QStandardPaths, Qt, Slot, QUrl, QSize, QRect, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog, QLabel, QVBoxLayout,
                               QMainWindow, QSlider, QStyle, QToolBar)
from PySide6.QtMultimedia import (QAudioOutput, QMediaFormat,
                                  QMediaPlayer)
from PySide6.QtMultimediaWidgets import QVideoWidget

class VideoWidget(QVideoWidget):

    def __init__(self):
        super().__init__()
        self._audio_output = QAudioOutput()
        self.player = QMediaPlayer()
        self.player.setAudioOutput(self._audio_output)
        self.player.setVideoOutput(self)
        self.tickpos = 0

    @Slot()
    def play(self):
        if self.player.hasVideo():
            self.player.play()
    
    @Slot()
    def pause(self):
        if self.player.playbackState() != QMediaPlayer.PlaybackState.PausedState and self.player.hasVideo():
            self.player.pause()

    @Slot()
    def stop(self):
        if self.player.playbackState() != QMediaPlayer.PlaybackState.StoppedState:
            self.player.stop()
        
    @Slot()
    def update_video(self, progress_value: int):
        if self.player.playbackState() != QMediaPlayer.PlaybackState.StoppedState and self.player.hasVideo():
            self.tickpos = progress_value
            self.player.setPosition(self.tickpos)
    
    @property
    def isPaused(self): return True if self.player.playbackState() == QMediaPlayer.PlaybackState.PausedState else False