##################### 
# SCREEN RESOLUTION : 1366 x 768
#####################

from tkinter import CENTER, Tk, Canvas, Button, RAISED, PhotoImage, NW, Entry, CENTER,Label
from random import randint
import V3.game3xClasses as Classes
import V3.game3xBossKey as Bk

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

# misc variable
cheatCodes = ["double points", "baby steps", "pew pew"] # Cheat Codes
bindedJump = "Up"                                       # global Jump
rankings = []                                           #  rankings
game_loop_id = None                                     # gameloop ID
pause = False                                           # pause
gameSpawned = False                                     # used to check if game is running
score = 0                                               # score for current run
bossKeyWindow = None                                    # hold boss key window instance

############# clear canvas
def clearCanvas():
    canvas.delete("all")

#############################################
# Main Menu Functions
############################################# 

#######################
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
        p1 = Classes.Player(200,400,15,canvas)
        p1.vel = 0

        ### creating platforms
        platform1 = Classes.Platforms(0,500,10,canvas)
        if randint(1,2)==1:
            platform2 = Classes.Platforms(1000,platform1.getPlatformHeight()+int(p1.maxJumpHeight()//2),10,canvas)
        else:
            platform2 = Classes.Platforms(1000,platform1.getPlatformHeight()-int(p1.maxJumpHeight()//2),10,canvas)
        
        if randint(1,2)==1:
            platform3 = Classes.Platforms(2000,platform2.getPlatformHeight()+int(p1.maxJumpHeight()//2),10,canvas)
        else:
            platform3 = Classes.Platforms(2000,platform2.getPlatformHeight()-int(p1.maxJumpHeight()//2),10,canvas)
    
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
    entry = Entry(root, width=20)
    entry_window = canvas.create_window(150, 50, anchor=CENTER, window=entry)

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

    canvas.create_window(width//2, height//2-100, anchor=CENTER, window=startNewGameButton)
    canvas.create_window(width//2, height//2, anchor=CENTER, window=loadGameButton)
    canvas.create_window(width//2, height//2+100, anchor=CENTER, window=leaderboardButton)
    canvas.create_window(width//2, height//2+200, anchor=CENTER, window=settingsButton)

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

    #btnPauseResumeWindow = canvas.create_window(width//2, height//2-100, anchor=CENTER, window=btnPauseResume)
    #btnPauseCheatsWindow = canvas.create_window(width//2, height//2, anchor=CENTER, window=btnPauseCheats)
    #btnPauseExitWindow= canvas.create_window(width//2, height//2+100, anchor=CENTER, window=btnPauseExit)
    canvas.create_window(width//2, height//2-100, anchor=CENTER, window=btnPauseResume)
    canvas.create_window(width//2, height//2, anchor=CENTER, window=btnPauseCheats)
    canvas.create_window(width//2, height//2+100, anchor=CENTER, window=btnPauseExit)

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

    canvas.create_window(150,50, anchor=CENTER, window=MenuToPause)
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


####### game end and start
def gameLoop():
    global pause
    if not pause:
        p1.updatePlayer(allPlatforms,restartGame)

        maxJumpHeight = p1.maxJumpHeight()
        lastPlatForm = platform1

        for p in allPlatforms:
            if p.getPlatformX()>lastPlatForm.getPlatformX():
                lastPlatForm = p
    
        for platform in allPlatforms:
            platform.updatePlatform(heightOfLastPlatform = lastPlatForm.getPlatformHeight(), xOfLastPlatform=lastPlatForm.getPlatformX(),maxPlayerJumpHeight=maxJumpHeight)

        global game_loop_id
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
    global backgroundGame,p1, platform1,platform2,platform3, allPlatforms

    clearCanvas()

    backgroundGame = PhotoImage(file="gameassets/Free-City-Backgrounds-Pixel-Art2Mod.png")
    #relsize = backgroundGame.width()

    canvas.create_image(0, 0, image=backgroundGame, anchor=NW)
        #deleteMenuButtons()
        
    playingGameMenuButton()
    p1 = Classes.Player(200,400,15,canvas)
    p1.vel = 0

        ### creating platforms
    platform1 = Classes.Platforms(0,500,10,canvas)
    if randint(1,2)==1:
        platform2 = Classes.Platforms(1000,platform1.getPlatformHeight()+int(p1.maxJumpHeight()//2),10,canvas)
    else:
        platform2 = Classes.Platforms(1000,platform1.getPlatformHeight()-int(p1.maxJumpHeight()//2),10,canvas)
        
    if randint(1,2)==1:
        platform3 = Classes.Platforms(2000,platform2.getPlatformHeight()+int(p1.maxJumpHeight()//2),10,canvas)
    else:
        platform3 = Classes.Platforms(2000,platform2.getPlatformHeight()-int(p1.maxJumpHeight()//2),10,canvas)

    allPlatforms = [platform1,platform2, platform3]

### key binding related
# Function to set the flag when the up key is released
def key_press(event):
    if event.keysym == bindedJump:
        p1.jump()
    if event.keysym == "b":
        print("hi")
        Bk.bossKeyCreate()
    
# Function to clear the flag when the up key is released
def key_release(event):
    if event.keysym == bindedJump:
        p1.stopJump()
       

# Bind the key press and release events
root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)
loadMenu()
root.mainloop()
