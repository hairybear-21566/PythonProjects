#####################
# SCREEN RESOLUTION : 1366 x 768
#####################

from tkinter import CENTER, Tk, Canvas, Button, RAISED, PhotoImage, NW, Entry, CENTER, Label
from random import randint
import gameV4xBosskey as Bk
from gameV4xPlatform import Platforms
from gameV4xPlayer import Player
from gameV4xBackgrounds import GameBackground

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
cheatCodes = ["double points", "baby steps", "pew pew"]  # Cheat Codes
bindedJump = "Up"                                       # global Jump
rankings = []                                           # rankings
game_loop_id = None                                     # gameloop ID
pause = False                                           # pause
# used to check if game is running
gameSpawned = False
score = 0                                               # score for current run
# hold boss key window instance
bossKeyWindow = None
PlayerName = None

# clear canvas


def clearCanvas():
    canvas.delete("all")
# setters and getters settings functions


def set_bind_jump():
    # Implement bind jump functionality
    pass


def get_bind_jump():
    return bindedJump


def set_score(n):
    global score
    score = n
    score_text.config(text="Score: "+str(n))

#############################################
# Main Menu Functions
#############################################

#######################


def startNewGame():
    global gameSpawned
    if not gameSpawned:
        global background1, background2, p1, platform1, platform2, platform3, allPlatforms, score_text

        clearCanvas()
        background1 = GameBackground(
            0, 0, "gameassets/starry-night.png", "background1", canvas, 1)

        background2 = GameBackground(
            1366, 0, "gameassets/starry-night.png", "background2", canvas, 1)

        score_text = Label(root, text="Score: "+str(score))
        canvas.create_window(width//2, height//2-300,
                             anchor=CENTER, window=score_text)


        playingGameMenuButton()
        p1 = Player(200, 400, 15, canvas)

        # creating platforms
        platform1 = Platforms(0, 500, 10, canvas)
        if randint(1, 2) == 1:
            platform2 = Platforms(1000, platform1.getPlatformHeight(
            )+int(p1.maxJumpHeight()//2), 10, canvas)
        else:
            platform2 = Platforms(1000, platform1.getPlatformHeight(
            )-int(p1.maxJumpHeight()//2), 10, canvas)

        if randint(1, 2) == 1:
            platform3 = Platforms(2000, platform2.getPlatformHeight(
            )+int(p1.maxJumpHeight()//2), 10, canvas)
        else:
            platform3 = Platforms(2000, platform2.getPlatformHeight(
            )-int(p1.maxJumpHeight()//2), 10, canvas)

        allPlatforms = [platform1, platform2, platform3]
        gameSpawned = True
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

    music_label = Label(root, text="Music:", font=(
        "Arial", 12), bg="black", fg="white")
    music_label_window = canvas.create_window(
        width // 2 - 50, height // 2 - 200, anchor=CENTER, window=music_label)

    music_toggle = Button(root, text="Toggle", font=("Arial", 12), bg="lightblue", fg="black", bd=3,
                          relief=RAISED, padx=10, pady=5, width=8, height=2, command=toggle_music)
    music_toggle_window = canvas.create_window(
        width // 2 + 50, height // 2 - 200, anchor=CENTER, window=music_toggle)

    bind_jump_button = Button(root, text="Bind Jump", font=("Arial", 12), bg="lightblue", fg="black", bd=3,
                              relief=RAISED, padx=10, pady=5, width=12, height=2, command=set_bind_jump)
    bind_jump_button_window = canvas.create_window(width // 2, height // 2 - 100, anchor=CENTER,
                                                   window=bind_jump_button)

    binded_jump_label = Label(root, text=f"Binded Jump: {get_bind_jump()}", font=(
        "Arial", 12), bg="black", fg="white")
    binded_jump_label_window = canvas.create_window(
        width // 2, height // 2, anchor=CENTER, window=binded_jump_label)

    back_button = Button(root, text="Back", font=("Arial", 12), bg="lightblue", fg="black", bd=3,
                         relief=RAISED, padx=10, pady=5, width=10, height=2, command=goBack)
    back_button_window = canvas.create_window(
        width // 2, height // 2 + 100, anchor=CENTER, window=back_button)


def loadMenu():
    entry = Entry(root, width=20)
    entry_window = canvas.create_window(
        width//2, height//2-200, anchor=CENTER, window=entry)

    startNewGameButton = Button(root, text="New Game", font=("Arial", 12), bg="lightblue",
                                fg="black", bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=startNewGame)

    loadGameButton = Button(root, text="Load Game", font=("Arial", 12), bg="lightblue",
                            fg="black", bd=3, relief=RAISED, padx=10, pady=5, width=16, height=2, command=loadGame)

    leaderboardButton = Button(root, text="Leaderboard", font=("Arial", 12), bg="lightblue",
                               fg="black", bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=leaderboard)

    settingsButton = Button(root, text="Settings", font=("Arial", 12), bg="lightblue",
                            fg="black", bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=settings)

    canvas.create_window(width//2, height//2-100,
                         anchor=CENTER, window=startNewGameButton)
    canvas.create_window(width//2, height//2,
                         anchor=CENTER, window=loadGameButton)
    canvas.create_window(width//2, height//2+100,
                         anchor=CENTER, window=leaderboardButton)
    canvas.create_window(width//2, height//2+200,
                         anchor=CENTER, window=settingsButton)

#############################################
# In Game Mangement Functions
#############################################


def inGameMenuPause():
    global btnPauseResume,  btnPauseCheats, btnPauseExit, pause

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

    canvas.create_window(width//2, height//2-100,
                         anchor=CENTER, window=btnPauseResume)
    canvas.create_window(width//2, height//2,
                         anchor=CENTER, window=btnPauseCheats)
    canvas.create_window(width//2, height//2+100,
                         anchor=CENTER, window=btnPauseExit)

    btn_MenuToPause.destroy()


def playingGameMenuButton():
    global btn_MenuToPause, pause
    MenuToPause = Button(root, text="Menu", font=("Arial", 12), bg="lightblue", fg="black",
                         bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=inGameMenuPause)
    btn_MenuToPause = MenuToPause
    canvas.create_window(150, 50, anchor=CENTER, window=MenuToPause)
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
    textEntryWindow = canvas.create_window(
        width//2, height//2-100, anchor=CENTER, window=textEntry)

    # Button to retrieve text
    textButton = Button(root, text="Get Text", command=get_text)
    textButtonWindow = canvas.create_window(
        width//2, height//2, anchor=CENTER, window=textButton)

    # Label to display the result
    resultLabel = Label(root, text="")
    resultLabelWindow = canvas.create_window(
        width//2, height//2-200, anchor=CENTER, window=resultLabel)

    # Back button
    backButton = Button(root, text="Back", command=goBack)
    backButtonWindow = canvas.create_window(
        width//2, height//2+100, anchor=CENTER, window=backButton)


def gameLoop():
    global pause, game_loop_id, score
    if not pause:
        set_score(score+1)
        p1.updatePlayer(allPlatforms, restartGame)
        background1.update_background()
        background2.update_background()
        maxJumpHeight = p1.maxJumpHeight()
        lastPlatForm = platform1
        for p in allPlatforms:
            if p.getPlatformX() > lastPlatForm.getPlatformX():
                lastPlatForm = p
        for platform in allPlatforms:
            platform.updatePlatform(heightOfLastPlatform=lastPlatForm.getPlatformHeight(
            ), xOfLastPlatform=lastPlatForm.getPlatformX(), maxPlayerJumpHeight=maxJumpHeight)
    game_loop_id = root.after(20, gameLoop)


def restartGame():
    global game_loop_id
    # only reset the position of the elements on the canvas
    if game_loop_id:
        p1.resetPosition()
        platform1.resetPos(platform1.initialX, platform1.initialY)
        if randint(1, 2) == 1:
            platform2.resetPos(
                1000, platform1.getPlatformHeight()-int(p1.maxJumpHeight()//2))
        else:
            platform2.resetPos(
                1000, platform1.getPlatformHeight()+int(p1.maxJumpHeight()//2))
        if randint(1, 2) == 1:
            platform3.resetPos(
                2000, platform2.getPlatformHeight()-int(p1.maxJumpHeight()//2))
        else:
            platform3.resetPos(
                2000, platform2.getPlatformHeight()+int(p1.maxJumpHeight()//2))
        set_score(0)

        # next we rest the positions of p1 and the platforms


def resetGame():
    # making new elements for the game completely here
    global  p1, platform1, platform2, platform3, allPlatforms,background1,background2

    clearCanvas()

    
    background1 = GameBackground(
            0, 0, "gameassets/starry-night.png", "background1", canvas, 1)

    background2 = GameBackground(
            1366, 0, "gameassets/starry-night.png", "background2", canvas, 1)

    score_text = Label(root, text="Score: "+str(score))
    canvas.create_window(width//2, height//2-300,
                             anchor=CENTER, window=score_text)
    

    playingGameMenuButton()
    p1 = Player(200, 400, 15, canvas)
    p1.vel = 0

    # creating platforms
    platform1 = Platforms(0, 500, 10, canvas)
    if randint(1, 2) == 1:
        platform2 = Platforms(1000, platform1.getPlatformHeight(
        )+int(p1.maxJumpHeight()//2), 10, canvas)
    else:
        platform2 = Platforms(1000, platform1.getPlatformHeight(
        )-int(p1.maxJumpHeight()//2), 10, canvas)

    if randint(1, 2) == 1:
        platform3 = Platforms(2000, platform2.getPlatformHeight(
        )+int(p1.maxJumpHeight()//2), 10, canvas)
    else:
        platform3 = Platforms(2000, platform2.getPlatformHeight(
        )-int(p1.maxJumpHeight()//2), 10, canvas)

    allPlatforms = [platform1, platform2, platform3]

# key binding related
# Function to set the flag when the up key is released


def key_press(event):
    if event.keysym == bindedJump:
        p1.jump()
    if event.keysym == "b":

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
