import os.path
from pathlib import Path
import cv2
import shutil

OUTPUT_DEFAULT = os.path.join("./output/tmp.mp4")

class VideoEditorInterface:
    def __init__(self, path: str) -> None:
        self.source = os.path.join(path)
        self.output = os.path.join(f"./output/{Path(self.source).stem}.mp4")
        os.makedirs("./output", exist_ok=True)
        shutil.copy(self.source, OUTPUT_DEFAULT)
        self.setup()

    
    def setup(self):
        self.cap = cv2.VideoCapture(OUTPUT_DEFAULT)
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        shape = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),  int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(self.output, fourcc, fps, shape)


    def read(self) -> list[cv2.Mat]:
        video = []
        while True:
            ret, img = self.cap.read()
            if not ret:
                break
            video.append(img)
        return video
    
    def write(self, video):
        for img in video:
            self.out.write(img)




class Transform:
    @staticmethod

    def reverse(video):
        videoReverse = []
        for img in video[::-1]:
            videoReverse.append(img)
        return videoReverse
    

    @staticmethod
    def cut(video: list[cv2.Mat]):
        cutie = len(video) // 2
        return video[cutie:]



class Plugins(VideoEditorInterface):
    def __init__(self, path) -> None:
        super().__init__(path = path)

    def reverse(self):
        video = self.read()
        for img in video[::-1]:
            self.out.write(img)
        self.cap.release()
        self.out.release()
        os.remove(OUTPUT_DEFAULT)
        os.rename(self.output, OUTPUT_DEFAULT)
        self.setup()

    def cut(self):
        video = self.read()
        cut = Transform.cut(video)
        self.write(cut)



class VideoEditor(Plugins):
    def __init__(self, path: str) -> None:
        super().__init__(path=path)
    









if __name__ == "__main__":
    VideoEditorInterface("./res/dog.mp4")