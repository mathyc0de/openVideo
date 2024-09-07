from tkinter import *
from tkinter import ttk
from editor import VideoEditor
# root = Tk()
# frm = ttk.Frame(root, padding=10)
# frm.grid()
# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
# root.mainloop()

class App:
    def __init__(self) -> None:
        self.editor = VideoEditor("./res/dog.mp4")
        self.root = Tk()
        self.frame = ttk.Frame(self.root, padding=10)
        self.homePage()
        
        self.__run()


    def __run(self): self.root.mainloop()


    def homePage(self):
        self.frame.grid()
        ttk.Button(self.frame, text = "reverte essa porra", command = self.editor.reverse).grid(column=0, row=0)
        ttk.Button(self.frame, text = "corta essa porra", command = self.editor.cut).grid(column=1, row=0)
        ttk.Button(self.frame, text = "Escreve a porra do vídeo", command= self.editor.write).grid(column=2, row=0)