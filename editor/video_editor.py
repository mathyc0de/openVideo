from .plugins import Plugins


class VideoEditor(Plugins):
    def __init__(self, path: str) -> None:
        super().__init__(path=path)
    