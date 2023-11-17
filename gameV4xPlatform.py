from random import randint

# restartGame IN updatPlayer
# allPlatforms IN updatePlayer->setNewFloor


class Platforms:
    width = 850  # Added class attribute for width thus the gap betweeen the platforms is 1000px - width in px)
    screen_height = 1366

    def __init__(self, x, y, scrollSpeed,GameCanvas,):
        self.initialX = x
        self.initialY = y
        self.x = x
        self.y = y
        self.scrollSpeed = scrollSpeed
        # Create the platform with the class attribute width
        self.platformInt = GameCanvas.create_rectangle(x, y, x + Platforms.width, Platforms.screen_height, fill="black")
        self.GameCanvas = GameCanvas

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

   
    def getPlatformHeight(self)->int:
        return self.y
    
    def getPlatformX(self)->int:
        return self.x
    
    def resetScrollSpeed(self):
        self.scrollSpeed = 10

    def resetPos(self,x,y):
        self.GameCanvas.coords(self.platformInt,x,y,x+self.width,768)
        self.x = x
        self.y = y
