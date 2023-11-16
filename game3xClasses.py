from random import randint

# restartGame IN updatPlayer
# allPlatforms IN updatePlayer->setNewFloor


class Platforms:
    width = 900  # Added class attribute for width
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
        print(type(GameCanvas))

    def updatePlatform(self,heightOfLastPlatform = 0, xOfLastPlatform=0, maxPlayerJumpHeight = 0):

        if self.x+self.width<0:
            self.newPlatform(heightOfLastPlatform, xOfLastPlatform, maxPlayerJumpHeight)
        else:
            self.scrollPlatform()

    #def changeScrollSpeedBy(self,delta):
        #self.scrollSpeed+=delta

    def scrollPlatform(self):
        self.GameCanvas.move(self.platformInt,-self.scrollSpeed,0)
        self.x-=self.scrollSpeed

    def newPlatform(self, prevHeight, xOfLastPlatform, jumpHeight):
        self.x = xOfLastPlatform + Platforms.width + 100  # Use class attribute width
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


class Player:


    width = 900

    def __init__(self,x,y,size,GameCanvas):
        """PROCEDURE, instatiating player square properties
        Args:
            x (int): player position on x axis
            y (int): player position on y axis
            size (int): player square dimesions
            GameCanvas (tkinter.Canvas): canvas everything for the game is drawn on including the player
        """
        self.initialX = x
        self.initialY = y
        self.size = size
        self.x = x
        self.y = y
        self.canvas = GameCanvas
        # player id on canvas 
        self.playerInt = self.canvas.create_rectangle(x,y,size+x,y+size,fill="green")
        # values related to movement
        self.vel = 0
        self.consecJumpFrames = 0
        self.maxConseqFrames=5
        self.gravity = 2
        self.jumpForce = -22
        self.onGround = True
        self.holdingJump=False
        self.jumpAvailable = False
        self.floor = self.y
        
    def updatePlayer(self,platforms,gameRestart):
        self.setNewFloor(platforms)
        self.setOnGround()
## checking if gravity should kick in yet
        ## if player not on ground
        if not self.onGround:
            # if they are holdidig jump for less than 5 frames
            if self.consecJumpFrames<self.maxConseqFrames and self.holdingJump:
                # continue velocity, but then increment frame count by 1
                self.consecJumpFrames+=1
                self.vel = self.jumpForce # just to make sure velocity is corect
            else:
                # add gravity to velocity to begin the fall
                self.vel += self.gravity
                # set jumpframes held to the max to begin the fall
                self.consecJumpFrames = self.maxConseqFrames
##      if the player + vel still has them above their floor
        if self.y + self.vel +self.size < self.floor:
            # move player to new y = old y + vel
            self.movePlayer(0,self.vel)
##      if player + velocity has them below the floor but player is above the floor
        elif self.y+self.vel+self.size>=self.floor and self.y+self.size<self.floor:
            # player attaches to ground
            self.movePlayer(0,self.floor - self.size -self.y)
            # velocity set to zero
            self.vel = 0
            # reset conseqative jump frames
            self.consecJumpFrames=0
        # if player on the floor just reset consequetive jump frames
        elif self.y + self.size == self.floor:
            self.consecJumpFrames=0
        elif self.y+self.size>700:
            gameRestart()   
        # if player below the floor
        else:
            gameRestart()
            
    def movePlayer(self,dx,dy):
        self.canvas.move(self.playerInt,dx,dy)
        self.y += dy
        self.x += dx

    def setNewFloor(self,platforms):
        value = False
        for p in platforms:
            if p.getPlatformX()<=self.x+self.size and p.getPlatformX()+p.width>=self.x+self.size:
                self.floor = p.getPlatformHeight()
                value = True
                break
        if value == False :
            self.floor = 800
    
    def setOnGround(self):
        if self.y+self.size==self.floor:
            self.onGround = True
        else: 
            self.onGround = False
        
    def setJumpAvailable(self):
        if self.y+self.size==self.floor:
            self.jumpAvailable =True
        else: 
            self.jumpAvailable = False

    def jump(self, event=None):
        """PROCEDURE, initiate jump

        Args:
            event (any, optional): may be used for jump nuance. Defaults to None.
        """        
        if self.onGround:
            self.vel = self.jumpForce
            self.onGround = False
            self.holdingJump=True

    def stopJump(self):
        """PROCEDURE, stops jump
        """
        self.holdingJump = False

    def maxJumpHeight(self)->int:
        """returns the max height of a jump

        Returns:
            int:max height of jump in pixels roughly, used for platform generation
        """
        return int((self.maxConseqFrames-1)*self.jumpForce + (self.jumpForce**2)//(2*self.gravity))

    def resetPosition(self):
        self.canvas.coords(self.playerInt,self.initialX,self.initialY,self.initialX+self.size,self.initialY+self.size)
        self.x = self.initialX
        self.y = self.initialY


class Obstacle:
    pass


class Coin:
    pass
