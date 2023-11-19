#####################
# SCREEN RESOLUTION : 1366 x 768
#####################

from tkinter import CENTER, Tk, Canvas, Button, RAISED, PhotoImage, NW, Entry, CENTER, Label,StringVar
from random import randint
import gameV4xBosskey as Bk
from gameV4xPlatform import Platforms
from gameV4xPlayer import Player
from gameV4xBackgrounds import GameBackground
from gameV4xSaverStorer import save_Game, read_saves_binary_file

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
gameSpawned = False                                     # used to check if game is running
score = 0                                               # score for current run
bossKeyWindow = None                                    # hold boss key window instance
PlayerName = None                                       # player name entered into the entry field in main menu
current_Player_saves = []                                 # last global stored saves array from binary file containing player saves
entry_var = None
platform1 = None
platform2 = None
platform3 = None
allPlatforms = None

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


def spawnEverything():
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


def startNewGame():
    global gameRunning, pause,entry
    if PlayerName != "Player Name" or PlayerName.strip() == "":

        
        spawnEverything()
        gameRunning = True
        gameLoop()
        pause = False
        #entry.bind('<FocusIn>', on_entry_click)
        #entry.bind('<FocusOut>', on_focus_out)
            

def loadGame():
    global background1, background2, p1, platform1, platform2, platform3, allPlatforms, score_text, pause, gameRunning

    player_has_load_data = False
    for p in read_saves_binary_file():
        if p["player_name"] == PlayerName:
            player_details_arr = list(p.values())
            print(player_details_arr)

            player_has_load_data = True
            break

    if player_details_arr:
        clearCanvas()
        background1 = GameBackground(
            player_details_arr[5][0], player_details_arr[5][1], "gameassets/starry-night.png", "background1", canvas, 1)

        background2 = GameBackground(
            player_details_arr[6][0], player_details_arr[6][1], "gameassets/starry-night.png", "background2", canvas, 1)

        score_text = Label(root, text="Score: " + str(player_details_arr[1]))
        canvas.create_window(width // 2, height // 2 - 300,
                             anchor=CENTER, window=score_text)

        playingGameMenuButton()
        p1 = Player(player_details_arr[2][0], player_details_arr[2][1], 15, canvas)
        p1.vel = player_details_arr[3]

        # creating platforms with correct initial x positions
        platform1 = Platforms(player_details_arr[4][0][0], player_details_arr[4][0][1], 10, canvas)
        platform2 = Platforms(player_details_arr[4][1][0], player_details_arr[4][1][1], 10, canvas)
        platform3 = Platforms(player_details_arr[4][2][0], player_details_arr[4][2][1], 10, canvas)

        # Update allPlatforms with the new platform instances
        allPlatforms = [platform1, platform2, platform3]

        pause = False
        gameRunning = True
        gameLoop()



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
    global entry
    ###################### entry 
    placeholder = "Player Name"

    def on_entry_change(event):
        root.after(1,lambda:update_change(event))

    
    def update_change(event):
        global PlayerName
        name = entry.get()
        PlayerName = name
        
        print(name, placeholder)

        found = False
        for d in current_Player_saves:
            if d["player_name"] == name:
                loadGameButton.config(state="normal")
                startNewGameButton.config(state="normal")
                found = True
                break
        if name == placeholder or name.strip()=="":
            loadGameButton.config(state="disabled")
            startNewGameButton.config(state="disabled")
        elif not found:
            loadGameButton.config(state="disabled")
            startNewGameButton.config(state="normal")
    
    entry = Entry(root, width=20)
    entry.insert(0, placeholder)
    entry_window = canvas.create_window(
        width//2, height//2-200, anchor=CENTER, window=entry)
    # Bind the <Key> event to the entry field
    entry.bind('<Key>', on_entry_change)
    def on_entry_click(event):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg='black')

    def on_focus_out(event):
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.config(fg='grey')

    entry.bind('<FocusIn>', on_entry_click)
    entry.bind('<FocusOut>', on_focus_out)
    
    #canvas.tag_unbind(entry_window, '<FocusIn>')
    #canvas.tag_unbind(entry_window, '<FocusOut>')
    ####################

    current_Player_saves = read_saves_binary_file()



    startNewGameButton = Button(root, text="New Game", font=("Arial", 12), bg="lightblue",
                                fg="black", bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=startNewGame,state = "disabled")

    loadGameButton = Button(root, text="Load Game", font=("Arial", 12), bg="lightblue",
                            fg="black", bd=3, relief=RAISED, padx=10, pady=5, width=16, height=2, command=loadGame, state = "disabled")

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

    PauseResume = Button(root, text="resume", font=("Arial", 12), bg="lightblue", fg="black",
                         bd=3, relief=RAISED, padx=10, pady=5, width=16, height=2, command=resumeGame)

    PauseCheats = Button(root, text="cheats", font=("Arial", 12), bg="lightblue", fg="black",
                         bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=cheatCodeEntry)

    PauseExit = Button(root, text="Save and Exit", font=("Arial", 12), bg="lightblue", fg="black",
                       bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=inGameExit)

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
    global pause, gameRunning, game_loop_id
    
    save_Game(PlayerName, score, (p1.x, p1.y), p1.vel,[[platform.getPlatformX(
        ), platform.getPlatformHeight()] for platform in allPlatforms], [background1.x,background1.y],[background2.x,background2.y])
    
    set_score(0)
    clearCanvas()
    root.after_cancel(game_loop_id)
    gameRunning = False  # Stop the game loop
    pause = True
    loadMenu()


def resumeGame():
    global pause
    pause = False
    arr = [btnPauseResume,  btnPauseCheats, btnPauseExit]
    for i in range(len(arr)):
        arr[i].destroy()
    playingGameMenuButton()
    gameLoop()


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
    global pause, game_loop_id, gameRunning
    if gameRunning and not pause:
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
    global game_loop_id, platform1,platform2,platform3
    # only reset the position of the elements on the canvas
    if game_loop_id:
        p1.resetPosition()
        platform1.resetPos(0, 500) # platform1.initalX replaced with 0
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


# key binding related
# Function to set the flag when the up key is released


def key_press(event):
    try:
        if event.keysym == bindedJump:
            p1.jump()
        if event.keysym == "b":
            Bk.bossKeyCreate()
    except:pass

# Function to clear the flag when the up key is released


def key_release(event):
    try:
        if event.keysym == bindedJump:
            p1.stopJump()
    except:pass


# Bind the key press and release events
root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)
loadMenu()
root.mainloop()
