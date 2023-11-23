from tkinter import Canvas,NW,PhotoImage
from random import randint

class Player:

    def __init__(self,x:int,y:int,size:int,GameCanvas:Canvas):
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
        #self.playerInt = self.canvas.create_rectangle(x,y,size+x,y+size,outline="green")
        # values related to movement
        self.vel = 0
        self.consecJumpFrames = 0
        self.maxConseqFrames=5
        self.gravity = 1.5
        self.jumpForce = -20
        self.onGround = True
        self.holdingJump=False
        self.jumpAvailable = False
        self.floor = self.y
        # animations
        self.run_frame = 0 # frames range from 0 to 7
        self.jump_frame = 2 # frames range from 0 to 2
        self.land_frame = 0 #frames range from 0 to 8
        self.image = PhotoImage(f"gameassets/player-jump/tile00{self.jump_frame}.png")
        self.diff = int((48 - self.size)//2)
        #self.image_object = self.canvas.create_image(x,y,anchor = NW, image = self.image,tags="player")
        self.image_object = self.canvas.create_image(self.x-self.diff,self.y-self.diff,anchor = NW, image = self.image,tags="player")
        self.canvas.tag_raise("player")
        self.landing = True
        self.still_animating_jump = True
        self.run_count = 0
        
    def updatePlayer(self,platforms:list,gameRestart):
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
            self.reset_frames() 
            gameRestart()
            return False 
        # if player below the floor
        else:
            self.reset_frames() 
            gameRestart() 
            return False
        self.animate()
        return True
    
    def animate(self):
        pass
        #if not on the ground use jump animations
            # if jump_frame != 2 then (jump_frame = jump_frame + 1 AND landing = True AND self.run_frame = 0 AND self.land_frame = 0)
        # else if player on ground
            # if player landing and land_frame<9 THEN load land_frame THEN land_frame+=1
            # else player landing = False THEN load player running THEN run_frame += 1 if run_frame<7 else run_frame = 0

        #if not on the ground use jump animations
        if not self.onGround:
            # if jump_frame != 2 then (jump_frame = jump_frame + 1 AND landing = True AND self.run_frame = 0 AND self.land_frame = 0)
            if self.jump_frame<2:
                '''
                self.image.config(file=f_path)
                
                self.canvas.itemconfig(self.image_object, image=self.image)
                '''
                self.image.config(file=f"gameassets/player-jump/tile00{self.jump_frame}.png")
                self.canvas.itemconfig(self.image_object, image=self.image)
                self.jump_frame+=1
                self.run_frame = 0
                self.land_frame = 0
                self.landing = True
                self.run_count = 0
            elif self.still_animating_jump:
                self.still_animating_jump=False
                self.image.config(file="gameassets/player-jump/tile002.png")
                self.canvas.itemconfig(self.image_object, image=self.image)

        # else if player on ground
        else:
            # if player landing and land_frame<9 THEN load land_frame THEN land_frame+=1 AND jump_frame = 0
            if self.landing and self.land_frame<9:
                self.image.config(file=f"gameassets/player-land/tile00{self.land_frame}.png")
                self.canvas.itemconfig(self.image_object, image=self.image)
                self.land_frame+=1
                self.jump_frame=0

            # else player landing = False THEN load player running THEN if run_count==4 THEN(run_frame += 1 if run_frame<7 else run_frame = 0) 
                                                                        # else run_count+=1
            else:
                self.landing=False
                self.image.config(file=f"gameassets/player-run/tile00{self.run_frame}.png")
                self.canvas.itemconfig(self.image_object, image=self.image)
                if self.run_count==4:
                    self.run_frame = self.run_frame+1 if self.run_frame<7 else 0
                    self.run_count = 0
                else:
                    self.run_count +=1
                


    def reset_frames(self):
        self.run_frame = 0  # frames range from 0 to 7
        self.jump_frame = 2  # frames range from 0 to 2
        self.land_frame = 0  # frames range from 0 to 8
        self.image = PhotoImage(file="gameassets/player-jump/tile002.png")
        self.diff = int((48 - self.size) // 2)
        self.canvas.itemconfig(self.image_object, image=self.image)
        self.landing = True
        self.still_animating_jump = True
        self.run_count = 0
    def movePlayer(self,dx:int,dy:int):
        #self.canvas.move(self.playerInt,dx,dy)
        self.y += dy
        self.x += dx
        #def move_image(self,dx:int,dy:int):
        self.canvas.move(self.image_object,dx,dy)

    def setNewFloor(self,platforms:list):
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
        return 150

    def resetPosition(self):

        #self.canvas.coords(self.playerInt,200,400,200+self.size,400+self.size)
        self.x = 200
        self.y = 400
        self.vel = 0
        self.reset_image()
        self.reset_frames()

    def reset_image(self):
        self.canvas.coords(self.image_object,self.x-self.diff,self.y-self.diff)
        