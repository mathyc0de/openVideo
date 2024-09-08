from .transform import Transform
from .video_editor_interface import VideoEditorInterface

class Plugins(VideoEditorInterface):
    def __init__(self, path) -> None:
        super().__init__(path = path)

    def reverse(self):
        video = self.read()
        reverse = Transform.reverse(video)
        self.write(reverse)
        video = None

    def cut(self):
        video = self.read()
        cut = Transform.cut(video)
        self.write(cut)