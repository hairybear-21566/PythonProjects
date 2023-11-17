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

    
            




'''
def updatePlatform(self, heightOfLastPlatform = 0, xOfLastPlatform=0, maxPlayerJumpHeight = 0):
        if self.x+self.width<0:
            self.newPlatform(heightOfLastPlatform, xOfLastPlatform, maxPlayerJumpHeight)
        else:
            self.scrollPlatform()

    def scrollPlatform(self):
        self.GameCanvas.move(self.platformInt,-self.scrollSpeed,0)
        self.x-=self.scrollSpeed

    def newPlatform(self, prevHeight, xOfLastPlatform, jumpHeight):
        self.x = xOfLastPlatform + 1000  # Use class attribute width
        if randint(1, 2) == 1:
            self.y = min(prevHeight + randint(0, int(jumpHeight // 2)), 700)
        else:
            self.y = max(prevHeight - randint(0, int(jumpHeight // 2)), 400)
        # Update the platform coordinates using class attribute width
        self.GameCanvas.coords(self.platformInt, self.x, self.y, self.x + Platforms.width, Platforms.screen_height)

'''