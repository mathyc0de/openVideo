from tkinter import *
from tkinter import ttk
from editor import VideoEditor
from pyvidplayer2 import VideoTkinter
# root = Tk()
# frm = ttk.Frame(root, padding=10)
# frm.grid()
# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
# root.mainloop()



class App:
    def __init__(self) -> None:
        self.root = Tk()
        self.frame = ttk.Frame(self.root, padding=10)

        #Video Player
        self.video = VideoTkinter("./res/ace.mp4")          # Calling video player
        self.canvas = Canvas(self.frame, width = self.video.current_size[0], height = self.video.current_size[1], highlightthickness=0)
        self.homePage()                                     # Calling interface buttons
        self.root.mainloop()


    def __updateVideo(self) -> None:
        # Video player looping 
        
        self.video.draw(self.canvas, (self.video.current_size[0] / 2, self.video.current_size[1] / 2), force_draw=False)
        if self.video.active:
            self.root.after(16, self.__updateVideo) # for around 60 fps
        else:
            self.root.destroy()
    
    def __
          



    def homePage(self):
        # Interface buttons.

        self.frame.grid()
        self.canvas.grid(row=1, columnspan=3)
        self.__updateVideo()
        ttk.Button(self.frame, text = ">|II", command = ).grid(column=0, row=2)
        # ttk.Button(self.frame, text = "reverte essa porra", command = self.editor.reverse).grid(column=0, row=0)
        # ttk.Button(self.frame, text = "corta essa porra", command = self.editor.cut).grid(column=1, row=0)
        # ttk.Button(self.frame, text = "Escreve a porra do vídeo", command= self.editor.write).grid(column=2, row=0)
        # pyvidplayer2.VideoTkinter("./res/dog.mp4").play()


