###
#crow class
####

from tkinter import PhotoImage, Canvas, NW

class Crow:

    def __init__(self,x:int,y:int,scrollSpeed:int,filepath:str,size:int,canvas:Canvas):

        self.x = x
        self.y = y
        self.scroll_speed =scrollSpeed
        self.frame = 1
        self.filepath = f"GameTests/crow-size-32/crow-size-32-{str(1)}.png"

        self.image = PhotoImage(file = filepath).subsample(4)
        
        self.image_object = canvas.create_image(x,y,anchor = NW, image = self.image)
        self.canvas = canvas
        

    def animate(self,frame):
        if self.frame != frame:
            self.filepath = f"GameTests/crow-size-32/crow-size-32-{str(frame)}.png"
            self.image = PhotoImage(file=self.filepath)
            self.image = self.image.subsample(4)
            self.canvas.itemconfig(self.image_object, image=self.image)
            self.frame = frame  # Update the frame attribute
            
