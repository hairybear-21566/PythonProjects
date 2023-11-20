from tkinter import PhotoImage,NW,Canvas
class GameBackground:
    def __init__(self, x:int, y:int, filepath:str, tag:str, canvas:Canvas,scrollspeed:int):
        self.initialX = x
        self.initialY = y
        self.x = x 
        self.y= y
        self.filepath = filepath
        self.tag = tag
        self.image = PhotoImage(file = filepath)
        self.image_object = canvas.create_image(x,y,anchor = NW, image = self.image, tags = tag)
        self.canvas = canvas
        self.canvas.tag_lower(tag)
        self.scrollspeed = scrollspeed
        self.width = self.image.width()
        
        

    def update_background(self):
        if self.x - self.scrollspeed <= -1366:
            self.x =  1366-(self.scrollspeed-(1366+self.x))
            self.canvas.coords(self.image_object,self.x,0)
        else:
            self.canvas.move(self.image_object,-self.scrollspeed,0)
            self.x -= self.scrollspeed
