import os.path
from pathlib import Path
import cv2
import shutil

class VideoEditorInterface:
    def __init__(self, path: str) -> None:
        self.source = path
        self.__setup()

    def __copy(self):
        name = Path(self.source).stem
        path = os.path.join(self.source)
        os.makedirs("./output/", exist_ok = True)
        self.output = os.path.join(f"./output/{name}.mp4")
        shutil.copy(path, self.output)
    
    def __setup(self):
        self.__copy()
        self.cap = cv2.VideoCapture(self.output)
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

VideoEditorInterface("./res/dog.mp4")

















# import os.path
# from pathlib import Path
# import cv2

# class VideoEditorInterface:
#     def __init__(self, path: str) -> None:
#         self.name = Path(path).stem
#         self.path = os.path.join(path)
#         self.cap = cv2.VideoCapture(self.path)
#         self.__setup()
#         video = self.__read()
#         self.write(video)

#     def __setup(self):
#         os.makedirs("./output/", exist_ok = True)
#         path = os.path.join(f"./output/{self.name}.mp4")
#         fps = self.cap.get(cv2.CAP_PROP_FPS)
#         shape = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),  int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#         self.out = cv2.VideoWriter(path, fourcc, fps, shape)
        
#     def __read(self) -> list[cv2.Mat]:
#         video = []
#         while True:
#             ret, img = self.cap.read()
#             if not ret:
#                 break
#             video.append(img)
#         return video
    
#     def write(self, video):
#         for img in video:
#             self.out.write(img)