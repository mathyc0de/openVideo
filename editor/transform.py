import cv2

class Transform:

    @staticmethod
    def reverse(video: list[cv2.Mat]):
        videoReverse = []
        for img in video[::-1]:
            videoReverse.append(img)
        return videoReverse
    
    @staticmethod
    def cut(video: list[cv2.Mat]):
        cutie = len(video) // 2
        return video[cutie:]

    