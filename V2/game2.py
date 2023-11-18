from tkinter import CENTER, Tk, Canvas, Button, RAISED, PhotoImage, NW, Entry, CENTER,Label
from random import randint

# Creating application window 
root = Tk()
width = 1366
height = 768
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x1 = (screen_width - width) // 2
y1 = (screen_height - height) // 2
root.geometry(f"{width}x{height}+{x1}+{y1}")
root.config(bg="#444444")

# Canvas creation
canvas = Canvas(root, width=width, height=height, bg="black")
canvas.place(x=(1366-width)//2, y=(820-height)//2)

# Cheat Codes
cheatCodes = ["double points", "baby steps", "pew pew"]

# Jump
bindedJump = "Up"

# rankings
rankings = []

# gameloop ID
game_loop_id = None

# pause
pause = False

# used to check if game is running
gameSpawned = False

############# clear canvas
def clearCanvas():
    canvas.delete("all")

#############################################
# Main Menu Functions
############################################# 
def set_bind_jump():
        # Implement bind jump functionality
        pass

def get_bind_jump():
    return bindedJump

def startNewGame():
    global gameSpawned
    if not gameSpawned:
        global backgroundGame, btn_start_new_game,p1, platform1,platform2,platform3, allPlatforms
        print("starting...")
        clearCanvas()

        backgroundGame = PhotoImage(file="gameassets/Free-City-Backgrounds-Pixel-Art2Mod.png")
        relsize = backgroundGame.width()

        canvas.create_image(0, 0, image=backgroundGame, anchor=NW)
        #deleteMenuButtons()
        
        playingGameMenuButton()
        p1 = Player(200,400,15)
        p1.vel = 0

        ### creating platforms
        platform1 = Platforms(0,500,10)
        if randint(1,2)==1:
            platform2 = Platforms(1000,platform1.getPlatformHeight()+int(p1.maxJumpHeight()//2),10)
        else:
            platform2 = Platforms(1000,platform1.getPlatformHeight()-int(p1.maxJumpHeight()//2),10)
        
        if randint(1,2)==1:
            platform3 = Platforms(2000,platform2.getPlatformHeight()+int(p1.maxJumpHeight()//2),10)
        else:
            platform3 = Platforms(2000,platform2.getPlatformHeight()-int(p1.maxJumpHeight()//2),10)
        

        allPlatforms = [platform1,platform2, platform3]

        gameSpawned=True

        gameLoop()
    else:
        resetGame()


def loadGame():
    clearCanvas()
    print("loading game..")

def leaderboard():
    clearCanvas()
    print("leaderboard...")

def settings():
    clearCanvas()
    print("Settings")

    def toggle_music():
        # Implement toggle music functionality
        pass

    def goBack():
        clearCanvas()
        loadMenu()


    music_label = Label(root, text="Music:", font=("Arial", 12), bg="black", fg="white")
    music_label_window = canvas.create_window(width // 2 - 50, height // 2 - 200, anchor=CENTER, window=music_label)

    music_toggle = Button(root, text="Toggle", font=("Arial", 12), bg="lightblue", fg="black", bd=3,
                          relief=RAISED, padx=10, pady=5, width=8, height=2, command=toggle_music)
    music_toggle_window = canvas.create_window(width // 2 + 50, height // 2 - 200, anchor=CENTER, window=music_toggle)

    bind_jump_button = Button(root, text="Bind Jump", font=("Arial", 12), bg="lightblue", fg="black", bd=3,
                              relief=RAISED, padx=10, pady=5, width=12, height=2, command=set_bind_jump)
    bind_jump_button_window = canvas.create_window(width // 2, height // 2 - 100, anchor=CENTER,
                                                  window=bind_jump_button)

    binded_jump_label = Label(root, text=f"Binded Jump: {get_bind_jump()}", font=("Arial", 12), bg="black", fg="white")
    binded_jump_label_window = canvas.create_window(width // 2, height // 2, anchor=CENTER, window=binded_jump_label)

    back_button = Button(root, text="Back", font=("Arial", 12), bg="lightblue", fg="black", bd=3,
                         relief=RAISED, padx=10, pady=5, width=10, height=2, command=goBack)
    back_button_window = canvas.create_window(width // 2, height // 2 + 100, anchor=CENTER, window=back_button)

def loadMenu():
    #global btn_start_new_game, btn_load_game, btn_leaderboard
    global loadGameButton,startNewGameButton,leaderboardButton

    loadGameButton = Button(root,
                            text="load Game",
                            font=("Arial", 12),
                            bg="lightblue",
                            fg="black",
                            bd=3,
                            relief=RAISED,
                            padx=10,
                            pady=5,
                            width=16,
                            height=2,
                            command=loadGame)

    startNewGameButton = Button(root,
                                text="start",
                                font=("Arial", 12),
                                bg="lightblue",
                                fg="black",
                                bd=3,
                                relief=RAISED,
                                padx=10,
                                pady=5,
                                width=15,
                                height=2,
                                command=startNewGame)

    leaderboardButton = Button(root,
                               text="leaderboard",
                               font=("Arial", 12),
                               bg="lightblue",
                               fg="black",
                               bd=3,
                               relief=RAISED,
                               padx=10,
                               pady=5,
                               width=15,
                               height=2,
                               command=leaderboard)

    settingsButton = Button(root,
                           text="settings",
                                font=("Arial", 12),
                                bg="lightblue",
                                fg="black",
                                bd=3,
                                relief=RAISED,
                                padx=10,
                                pady=5,
                                width=15,
                                height=2,
                                command=settings)
    btn_start_new_game = startNewGameButton
    btn_load_game = loadGameButton
    btn_leaderboard = leaderboardButton
    btn_settings = settingsButton

    btn_start_new_game_window = canvas.create_window(width//2, height//2-100, anchor=CENTER, window=startNewGameButton)
    btn_load_game_window = canvas.create_window(width//2, height//2, anchor=CENTER, window=loadGameButton)
    btn_leaderboard_window = canvas.create_window(width//2, height//2+100, anchor=CENTER, window=leaderboardButton)
    btn_settings_window = canvas.create_window(width//2, height//2+200, anchor=CENTER, window=settingsButton)


#############################################
# In Game Mangement Functions
#############################################
def inGameMenuPause():
    global btnPauseResume,  btnPauseCheats,btnPauseExit, pause
    
    pause = True

    PauseResume = Button(root,
                            text="resume",
                            font=("Arial", 12),
                            bg="lightblue",
                            fg="black",
                            bd=3,
                            relief=RAISED,
                            padx=10,
                            pady=5,
                            width=16,
                            height=2,
                            command=resumeGame)

    PauseCheats = Button(root,
                                text="cheats",
                                font=("Arial", 12),
                                bg="lightblue",
                                fg="black",
                                bd=3,
                                relief=RAISED,
                                padx=10,
                                pady=5,
                                width=15,
                                height=2,
                                command=cheatCodeEntry)
    
    PauseExit = Button(root,
                               text="Save and Exit",
                               font=("Arial", 12),
                               bg="lightblue",
                               fg="black",
                               bd=3,
                               relief=RAISED,
                               padx=10,
                               pady=5,
                               width=15,
                               height=2,
                               command=inGameExit)

    btnPauseResume = PauseResume
    btnPauseCheats = PauseCheats
    btnPauseExit = PauseExit

    btnPauseResumeWindow = canvas.create_window(width//2, height//2-100, anchor=CENTER, window=btnPauseResume)
    btnPauseCheatsWindow = canvas.create_window(width//2, height//2, anchor=CENTER, window=btnPauseCheats)
    btnPauseExitWindow= canvas.create_window(width//2, height//2+100, anchor=CENTER, window=btnPauseExit)

    btn_MenuToPause.destroy()

def playingGameMenuButton():
    global btn_MenuToPause,pause
    MenuToPause = Button(root,
                               text="Menu",
                               font=("Arial", 12),
                               bg="lightblue",
                               fg="black",
                               bd=3,
                               relief=RAISED,
                               padx=10,
                               pady=5,
                               width=15,
                               height=2,
                               command=inGameMenuPause)
    btn_MenuToPause = MenuToPause

    btn_MenuToPause_window = canvas.create_window(150,50, anchor=CENTER, window=MenuToPause)
    pause = False

    pass

def inGameExit():
    clearCanvas()
    
    loadMenu()

def resumeGame():
    global pause
    pause = False
    arr = [btnPauseResume,  btnPauseCheats, btnPauseExit]
    for i in range(len(arr)):
        arr[i].destroy()
    playingGameMenuButton()

def cheatCodeEntry():
    arr = [btnPauseResume,  btnPauseCheats, btnPauseExit]
    for i in range(len(arr)):
        arr[i].destroy()

    def get_text():
        text = textEntry.get()
        resultLabel.config(text=f"You entered: {text}")

    def goBack():
        textEntry.destroy()
        textButton.destroy()
        resultLabel.destroy()
        backButton.destroy()
        inGameMenuPause()

    # Entry widget
    textEntry = Entry(root, width=30)
    textEntryWindow = canvas.create_window(width//2, height//2-100, anchor=CENTER, window=textEntry)

    # Button to retrieve text
    textButton = Button(root, text="Get Text", command=get_text)
    textButtonWindow = canvas.create_window(width//2, height//2, anchor=CENTER, window=textButton)

    # Label to display the result
    resultLabel = Label(root, text="")
    resultLabelWindow = canvas.create_window(width//2, height//2-200, anchor=CENTER, window=resultLabel)

    # Back button
    backButton = Button(root, text="Back", command=goBack)
    backButtonWindow = canvas.create_window(width//2, height//2+100, anchor=CENTER, window=backButton)

####### game running functions
    ### key binding related
# Function to set the flag when the up key is released
def key_press(event):
        if event.keysym == bindedJump:
            p1.jump()
    
# Function to clear the flag when the up key is released
def key_release(event):
    if event.keysym == bindedJump:
        p1.stopJump()

####### game end and start
def gameLoop():
    global pause
    if not pause:
        p1.updatePlayer()

        maxJumpHeight = p1.maxJumpHeight()
        lastPlatForm = platform1

        for p in allPlatforms:
            if p.getPlatformX()>lastPlatForm.getPlatformX():
                lastPlatForm = p
    
        for platform in allPlatforms:
            platform.updatePlatform(lastPlatForm.getPlatformHeight(),lastPlatForm.getPlatformX(),maxJumpHeight)

        global game_loop_id
        
    else:
        #p1.resetPosition()
        #platform1.resetPos(platform1.initialX,platform1.initialY)
        #platform2.resetPos(1000,platform1.getPlatformHeight()+int(p1.maxJumpHeight()//2))
        #platform3.resetPos(2000,platform2.getPlatformHeight()+int(p1.maxJumpHeight()//2))
        pass
    game_loop_id = root.after(16, gameLoop)

def restartGame():
    global game_loop_id
    ########################### only reset the position of the elements on the canvas
    if game_loop_id:
        p1.resetPosition()
        
        platform1.resetPos(platform1.initialX,platform1.initialY)
        if randint(1,2)==1:
            platform2.resetPos(1000,platform1.getPlatformHeight()-int(p1.maxJumpHeight()//2))
        else:
            platform2.resetPos(1000,platform1.getPlatformHeight()+int(p1.maxJumpHeight()//2))
        if randint(1,2)==1:
            platform3.resetPos(2000,platform2.getPlatformHeight()-int(p1.maxJumpHeight()//2))
        else:
            platform3.resetPos(2000,platform2.getPlatformHeight()+int(p1.maxJumpHeight()//2))
        
        ### next we rest the positions of p1 and the platforms

def resetGame():
    ################ making new elements for the game completely here
    global backgroundGame, btn_start_new_game,p1, platform1,platform2,platform3, allPlatforms

    clearCanvas()

    backgroundGame = PhotoImage(file="gameassets/Free-City-Backgrounds-Pixel-Art2Mod.png")
    relsize = backgroundGame.width()

    canvas.create_image(0, 0, image=backgroundGame, anchor=NW)
        #deleteMenuButtons()
        
    playingGameMenuButton()
    p1 = Player(200,400,15)
    p1.vel = 0

        ### creating platforms
    platform1 = Platforms(0,500,10)
    if randint(1,2)==1:
        platform2 = Platforms(1000,platform1.getPlatformHeight()+int(p1.maxJumpHeight()//2),10)
    else:
        platform2 = Platforms(1000,platform1.getPlatformHeight()-int(p1.maxJumpHeight()//2),10)
        
    if randint(1,2)==1:
        platform3 = Platforms(2000,platform2.getPlatformHeight()+int(p1.maxJumpHeight()//2),10)
    else:
        platform3 = Platforms(2000,platform2.getPlatformHeight()-int(p1.maxJumpHeight()//2),10)

    

    allPlatforms = [platform1,platform2, platform3]


####### game Objects
class Obstacles:
    pass

class Platforms:
    width = 900  # Added class attribute for width

    def __init__(self, x, y, scrollSpeed):
        self.initialX = x
        self.initialY = y
        self.x = x
        self.y = y
        self.scrollSpeed = scrollSpeed
        # Create the platform with the class attribute width
        self.platformInt = canvas.create_rectangle(x, y, x + Platforms.width, screen_height, fill="black")

    def updatePlatform(self,heightOfLastPlatform = 0, xOfLastPlatform=0, maxPlayerJumpHeight = 0):

        if self.x+self.width<0:
            self.newPlatform(heightOfLastPlatform, xOfLastPlatform, maxPlayerJumpHeight)
        else:
            self.scrollPlatform()

    #def changeScrollSpeedBy(self,delta):
        #self.scrollSpeed+=delta

    def scrollPlatform(self):
        canvas.move(self.platformInt,-self.scrollSpeed,0)
        self.x-=self.scrollSpeed

    def newPlatform(self, prevHeight, xOfLastPlatform, jumpHeight):
        self.x = xOfLastPlatform + Platforms.width + 100  # Use class attribute width
        if randint(1, 2) == 1:
            self.y = min(prevHeight + randint(0, int(jumpHeight // 2)), 700)
        else:
            self.y = max(prevHeight - randint(0, int(jumpHeight // 2)), 400)

        # Update the platform coordinates using class attribute width
        canvas.coords(self.platformInt, self.x, self.y, self.x + Platforms.width, screen_height)

   
    def getPlatformHeight(self)->int:
        return self.y
    
    def getPlatformX(self)->int:
        return self.x
    
    def resetScrollSpeed(self):
        self.scrollSpeed = 10

    def resetPos(self,x,y):
        canvas.coords(self.platformInt,x,y,x+self.width,768)
        self.x = x
        self.y = y
    
class Player:

    width = 900

    def __init__(self,x,y,size):
        """PROCEDURE, instatiating player square

        Args:
            x (int): player position on x axis
            y (int): player position on y axis
            size (int): player square dimesions
               
        """
        self.initialX = x
        self.initialY = y
        self.size = size
        self.x = x
        self.y = y
        # player id on canvas 
        self.playerInt = canvas.create_rectangle(x,y,size+x,y+size,fill="green")
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

    def updatePlayer(self):
        """PROCEDURE, updating player location
        """
        self.setNewFloor()
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
            restartGame()   

        # if player below the floor
        else:
            restartGame()
            

    def movePlayer(self,dx,dy):
        canvas.move(self.playerInt,dx,dy)
        self.y += dy
        self.x += dx

    def setNewFloor(self):
        value = False
        for p in allPlatforms:
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
        canvas.coords(self.playerInt,self.initialX,self.initialY,self.initialX+self.size,self.initialY+self.size)
        self.x = self.initialX
        self.y = self.initialY

        

# Bind the key press and release events
root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)
        

loadMenu()
root.mainloop()
