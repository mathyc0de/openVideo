import os.path
from pathlib import Path
import cv2
import shutil
from math import ceil

"""
Python PIP's package for open-cv is >>self-contained<< (can't access system packages)
and its linux version is >>shipped only with open codecs<< apparently.

This results in the opencv module shipped from PIP not being able to edit .mp4 videos in Linux.

TODO: Recompile the OpenCV package so it can use proprietary codecs as .mp4.
"""

OUTPUT_DEFAULT = os.path.join("./output/tmp.mp4")

def delete_temp():
    if os.path.isfile(OUTPUT_DEFAULT):
        os.remove(OUTPUT_DEFAULT)

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
        self.out.release()



class VideoEditor(VideoEditorInterface):
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
        # self.setup()
        # frame_index = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        # while frame_index != 0:
        #     self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        #     _, frame = self.cap.read()
        #     self.out.write(frame)
        #     frame_index -=1
        #     print(frame_index)
        # self.out.release()
        # self.cap.release()
        return OUTPUT_DEFAULT
    
    @staticmethod
    def save_video(filename):
        path = os.path.join("./output/", filename)
        shutil.copy(OUTPUT_DEFAULT, path)
        
    @staticmethod
    def get_time(path: str) -> int:
        cap = cv2.VideoCapture(path)
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        return int(frames // fps)

    def cut(self):
        video = self.read()
        cutie = len(video) // 2
        self.write(cutie)