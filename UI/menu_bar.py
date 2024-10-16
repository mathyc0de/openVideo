from __future__ import annotations
import sys
from PySide6.QtCore import QStandardPaths, Qt, Slot, QUrl, QSize, QRect, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QApplication, QDialog, QFileDialog, QLabel, QVBoxLayout,QMenuBar, QMenu,
                               QSlider, QStyle, QToolBar)
from PySide6.QtMultimedia import (QAudioOutput, QMediaFormat,
                                  QMediaPlayer)
class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()
        self.__file_menu = QMenu("&File")
        self.__edit_menu = QMenu("&Edit")
        self.__open_action = QAction(QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen), "&Open...", self, 
                                    shortcut=QKeySequence.Open)
        self.__reverse_action = QAction(QIcon.fromTheme(QIcon.ThemeIcon.MediaSeekBackward), "&Reverter...", self,
                              shortcut=QKeySequence.Open)
        self.__save_action = QAction(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave), "&Salvar...", self,
                              shortcut=QKeySequence.Open)
        self.__file_menu.addActions((self.__open_action, self.__save_action))
        self.__edit_menu.addAction(self.__reverse_action)
        self.addMenu(self.__file_menu)
        self.addMenu(self.__edit_menu)
    
    @property
    def open_action(self):
        return self.__open_action
    
    @property
    def reverse_action(self):
        return self.__reverse_action

    @property
    def save_action(self):
        return self.__save_action