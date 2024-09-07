import cv2
from pathlib import Path
import os.path
from .plugins import Plugins

class VideoEditor(Plugins):
    def __init__(self, path: str) -> None:
        self.name = Path(path).stem
        self.path = os.path.join(path)
        self.cap = cv2.VideoCapture(self.path)
        self.__setup()
        self.result = self.__read()
        super().__init__(self.result)

    def __setup(self):
        os.makedirs("./output/", exist_ok = True)
        path = os.path.join(f"./output/{self.name}.mp4")
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        shape = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),  int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(path, fourcc, fps, shape)
        
    def __read(self) -> list[cv2.Mat]:
        video = []
        while True:
            ret, img = self.cap.read()
            if not ret:
                break
            video.append(img)
        return video
    
    def write(self):
        for img in self.result:
            self.out.write(img)
    

#https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html

# if __name__ == "__main__":
    # video_editor = VideoEditor("./res/dog.mp4")
#     video_editor.reverse()
    

