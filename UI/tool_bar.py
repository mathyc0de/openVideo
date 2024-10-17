from __future__ import annotations
import sys
import os.path
from PySide6.QtCore import QStandardPaths, Qt, Slot, QUrl, QSize, QRect, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog, QLabel, QVBoxLayout,
                               QMainWindow, QSlider, QStyle, QToolBar)
from PySide6.QtMultimedia import (QAudioOutput, QMediaFormat,
                                  QMediaPlayer)

class ToolBar(QToolBar):
    def __init__(self, video_time: int = 0, tick_pos: int = 0):
        super().__init__()
        self.video_time = video_time
        self.tickpos = tick_pos
        self.setMovable(False)
        self.__fullscreen_icon = QIcon()
        self.__fullscreen_icon.addFile(os.path.join("./", "assets/", "fullscreen.png"))
        self.__play_action = QAction(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart,
                            self.style().standardIcon(QStyle.SP_MediaPlay)), "Play")
        self.__pause_action = QAction(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackPause,
                            self.style().standardIcon(QStyle.SP_MediaPause)), "Pause")
        self.__stop_action = QAction(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStop,
                        self.style().standardIcon(QStyle.SP_MediaStop)), "Stop")
        self.__fullscreen_action = QAction(self.__fullscreen_icon, "Fullscreen")
        self.__play_action.setDisabled(True)
        self.__progress = QSlider(orientation=Qt.Orientation.Horizontal)
        self.__progress.setMaximum(self.video_time)
        self.__progress.setValue(self.tickpos)
        self.pause()
    
    def have_actions(self) -> bool:
        return len(self.actions()) > 0

    
    def play(self):
        if self.have_actions():
            self.removeAction(self.__play_action)
            self.removeAction(self.__stop_action)
        self.addAction(self.__pause_action)
        self.addAction(self.__stop_action)
        self.addAction(self.__fullscreen_action)
        self.addWidget(self.progress)
    
    def pause(self):
        if self.have_actions():
            self.removeAction(self.__pause_action)
            self.removeAction(self.__stop_action)
        self.addAction(self.__play_action)
        self.addAction(self.__stop_action)
        self.addAction(self.__fullscreen_action)
        self.addWidget(self.progress)
    
    def stop(self):
        self.pause()
        self.set_progress_value(0)
        self.set_progress_limit(0)
        self.__play_action.setDisabled(True)

    
    def set_progress_value(self, player_pos: int):
        self.tickpos = player_pos
        self.__progress.setValue(self.tickpos)
    
    def set_progress_limit(self, limit: int):
        self.video_time = limit
        self.progress.setMaximum(self.video_time)
        self.progress.setTickInterval(self.video_time)
    

    @property
    def play_action(self) -> QAction:
        return self.__play_action

    @property
    def pause_action(self) -> QAction:
        return self.__pause_action
    
    @property
    def stop_action(self) -> QAction:
        return self.__stop_action
    
    @property
    def progress(self) -> QSlider:
        return self.__progress

    @property
    def fullscreen_action(self) -> QAction:
        return self.__fullscreen_action
