from .transform import Transform
from .video_editor_interface import VideoEditorInterface

class Plugins(VideoEditorInterface):
    def __init__(self, path) -> None:
        super().__init__(path = path)

    def reverse(self): self.result = Transform.reverse(self.result)

    def cut(self): self.result = Transform.cut(self.result) 