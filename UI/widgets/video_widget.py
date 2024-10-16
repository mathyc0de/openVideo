from PySide6.QtMultimediaWidgets import QVideoWidget
class VideoWidget(QVideoWidget):

    def __init__(self, parent=None):
        super().__init__(parent)