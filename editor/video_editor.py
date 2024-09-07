import cv2
from pathlib import Path
from .plugins import Plugins


class VideoEditor(Plugins):
    def __init__(self, path: str) -> None:
        super().__init__(path=path)
    

#https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html

# if __name__ == "__main__":
    # video_editor = VideoEditor("./res/dog.mp4")
#     video_editor.reverse()
    

