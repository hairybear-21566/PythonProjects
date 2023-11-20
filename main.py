#####################
# SCREEN RESOLUTION : 1366 x 768
#####################

from tkinter import CENTER, Tk, Canvas, Button, RAISED, PhotoImage, NW, Entry, CENTER, Label, StringVar
from random import randint
import Bosskey_Handler as Bk
from Platform_Class import Platforms
from Player_Class import Player
from Background_Class import GameBackground
from Player_Saves_Handler import save_Game, read_saves_binary_file
from Leaderboard_Handler import update_Leaderboard, read_leaderboard_binary_file


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
# Cheat Codes are "double points", "baby steps"(not ready), "pew pew"(definetley not ready)
cheat_codes = ["double points"]
cheat_codes_actived = {s: False for s in cheat_codes}

bindedJump = "Up"                                       # global Jump
game_loop_id = None                                     # gameloop ID
pause = False                                           # pause
# used to check if game is running
gameSpawned = False
gameRunning = True
entry_focused = False
score = 0                                               # score for current run
# hold boss key window instance
bossKeyWindow = None
# player name entered into the entry field in main menu
PlayerName = None
# last global stored saves array from binary file containing player saves
current_Player_saves = []
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

def platform_offset():
    global p1
    return randint(0,int(150//1.7))
    #return 150
    
#############################################
# Main Menu Functions
#############################################

#######################


def spawnEverything():
    global background1, background2, p1, platform1, platform2, platform3, allPlatforms, score_text, gameSpawned, background_upper1, background_upper2

    gameSpawned = True

    clearCanvas()
    

    background_upper1 = GameBackground(
        0, 0, "gameassets/back-clouds.png", "background_upper1", canvas, 2)
    background_upper2 = GameBackground(
        1366, 0, "gameassets/back-clouds.png", "background_upper2", canvas, 2)
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
        platform2 = Platforms(1000, min(700,platform1.getPlatformHeight(
        )+int(platform_offset())), 10, canvas)
    else:
        platform2 = Platforms(1000, max(platform1.getPlatformHeight(
        )-int(platform_offset()),400), 10, canvas)

    if randint(1, 2) == 1:
        platform3 = Platforms(2000, min(700,platform2.getPlatformHeight(
        )+int(platform_offset())), 10, canvas)
    else:
        platform3 = Platforms(2000, max(400,platform2.getPlatformHeight(
        )-int(platform_offset())), 10, canvas)

    allPlatforms = [platform1, platform2, platform3]


def startNewGame():
    root.focus_set()
    global gameRunning, pause, entry
    if PlayerName != "Player Name" or PlayerName.strip() == "":

        spawnEverything()
        gameRunning = True
        gameLoop()
        pause = False
        # entry.bind('<FocusIn>', on_entry_click)
        # entry.bind('<FocusOut>', on_focus_out)


def loadGame():
    global background1, background2, p1, platform1, platform2, platform3, allPlatforms, score_text, pause, gameRunning, background_upper1, background_upper2
    root.focus_set()
    player_details_arr = None
    
    for p in read_saves_binary_file():
        if p["player_name"] == PlayerName:
            player_details_arr = list(p.values())
            # print(player_details_arr)
            break

    if player_details_arr:
        clearCanvas()
        background_upper1 = GameBackground(
        player_details_arr[7][0], player_details_arr[7][1], "gameassets/back-clouds.png", "background_upper1", canvas, 2)
        background_upper2 = GameBackground(
        player_details_arr[8][0], player_details_arr[8][1], "gameassets/back-clouds.png", "background_upper2", canvas, 2)

        background1 = GameBackground(
            player_details_arr[5][0], player_details_arr[5][1], "gameassets/starry-night.png", "background1", canvas, 1)

        background2 = GameBackground(
            player_details_arr[6][0], player_details_arr[6][1], "gameassets/starry-night.png", "background2", canvas, 1)
        
        

        score_text = Label(root, text="Score: " + str(player_details_arr[1]))
        canvas.create_window(width // 2, height // 2 - 300,
                             anchor=CENTER, window=score_text)

        playingGameMenuButton()
        p1 = Player(player_details_arr[2][0],
                    player_details_arr[2][1], 15, canvas)
        p1.vel = player_details_arr[3]

        # creating platforms with correct initial x positions
        platform1 = Platforms(
            player_details_arr[4][0][0], player_details_arr[4][0][1], 10, canvas)
        platform2 = Platforms(
            player_details_arr[4][1][0], player_details_arr[4][1][1], 10, canvas)
        platform3 = Platforms(
            player_details_arr[4][2][0], player_details_arr[4][2][1], 10, canvas)

        # Update allPlatforms with the new platform instances
        allPlatforms = [platform1, platform2, platform3]

        pause = False
        gameRunning = True
        gameLoop()


def leaderboard():
    root.focus_set()
    clearCanvas()

    def goBack():
        clearCanvas()
        loadMenu()

    rankings = read_leaderboard_binary_file()
    places = len(rankings)
    i = 0

    label_title = Label(root, text="LEADERBOARD", font=(
        "Nimbus Mono PS", 30), bg="black", fg="white")
    label_title_window = canvas.create_window(
        width // 2, 100, anchor=CENTER, window=label_title)

    while i != places:

        label1 = Label(root, text=rankings[i]["player_name"], font=(
            "Nimbus Mono PS", 12), bg="black", fg="white")
        label1_window = canvas.create_window(
            width // 2 - 50, height // 2 - 200 + 100*i, anchor=CENTER, window=label1)

        label2 = Label(root, text=rankings[i]["score"], font=(
            "Nimbus Mono PS", 12), bg="black", fg="white")
        label2_window = canvas.create_window(
            width // 2 + 50, height // 2 - 200+100*i, anchor=CENTER, window=label2)
        i += 1

        # music_toggle = Button(root, text="Toggle", font=("Nimbus Mono PS", 12), bg="black", fg="white", bd=3,
        #                 relief=RAISED, padx=10, pady=5, width=8, height=2, )
        # music_toggle_window = canvas.create_window(
        # width // 2 + 50, height // 2 - 200, anchor=CENTER, window=music_toggle)

    back_button = Button(root, text="Back", font=("Nimbus Mono PS", 12), bg="black", fg="white",
                         bd=3, relief=RAISED, padx=10, pady=5, width=10, height=2, command=goBack)
    canvas.create_window(width // 2, height // 2 + 300,
                         anchor=CENTER, window=back_button)


def settings():
    root.focus_set()
    clearCanvas()

    def toggle_music():
        # Implement toggle music functionality
        pass

    def goBack():
        clearCanvas()
        loadMenu()

    music_label = Label(root, text="Music:", font=(
        "Nimbus Mono PS", 12), bg="black", fg="white")
    music_label_window = canvas.create_window(
        width // 2 - 50, height // 2 - 200, anchor=CENTER, window=music_label)

    music_toggle = Button(root, text="Toggle", font=("Nimbus Mono PS", 12), bg="black", fg="white", bd=3,
                          relief=RAISED, padx=10, pady=5, width=8, height=2, command=toggle_music)
    music_toggle_window = canvas.create_window(
        width // 2 + 50, height // 2 - 200, anchor=CENTER, window=music_toggle)

    bind_jump_button = Button(root, text="Bind Jump", font=("Nimbus Mono PS", 12), bg="black", fg="white", bd=3,
                              relief=RAISED, padx=10, pady=5, width=12, height=2, command=set_bind_jump)
    bind_jump_button_window = canvas.create_window(width // 2, height // 2 - 100, anchor=CENTER,
                                                   window=bind_jump_button)

    binded_jump_label = Label(root, text=f"Binded Jump: {get_bind_jump()}", font=(
        "Nimbus Mono PS", 12), bg="black", fg="white")
    binded_jump_label_window = canvas.create_window(
        width // 2, height // 2, anchor=CENTER, window=binded_jump_label)

    back_button = Button(root, text="Back", font=("Nimbus Mono PS", 12), bg="black", fg="white", bd=3,
                         relief=RAISED, padx=10, pady=5, width=10, height=2, command=goBack)
    back_button_window = canvas.create_window(
        width // 2, height // 2 + 100, anchor=CENTER, window=back_button)


def loadMenu():
    global entry, entry_focused

    label_title = Label(root, text="NIGHT CRAWLER", font=(
        "C059", 40), bg="black", fg="dark red")
    label_title_window = canvas.create_window(
        width // 2, 100, anchor=CENTER, window=label_title)
    # entry
    placeholder = "Player Name"
    

    def on_entry_change(event, running):
        if running:
            root.after(1, update_change)

    def update_change():
        global PlayerName
        name = entry.get()
        PlayerName = name
        found = False

        for d in current_Player_saves:
            if d["player_name"] == name:
                loadGameButton.config(state="normal")
                startNewGameButton.config(state="normal")
                found = True
                break
        if name == placeholder or name.strip() == "":
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
    entry.bind('<Key>', lambda x: on_entry_change(
        x, gameRunning or gameSpawned))

    def on_entry_click(event):
        global entry_focused
        entry_focused = True
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg='black')

    def on_focus_out(event):
        global entry_focused
        entry_focused = False
        if entry.get() == '':
            entry.insert(0, placeholder)
            entry.config(fg='grey')

    entry.bind('<FocusIn>', on_entry_click)
    entry.bind('<FocusOut>', on_focus_out)

    # canvas.tag_unbind(entry_window, '<FocusIn>')
    # canvas.tag_unbind(entry_window, '<FocusOut>')
    ####################

    current_Player_saves = read_saves_binary_file()

    startNewGameButton = Button(root, text="New Game", font=("Nimbus Mono PS", 12), bg="black",
                                fg="white", bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=startNewGame, state="disabled")

    loadGameButton = Button(root, text="Load Game", font=("Nimbus Mono PS", 12), bg="black",
                            fg="white", bd=3, relief=RAISED, padx=10, pady=5, width=16, height=2, command=loadGame, state="disabled")

    leaderboardButton = Button(root, text="Leaderboard", font=("Nimbus Mono PS", 12), bg="black",
                               fg="white", bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=leaderboard)

    settingsButton = Button(root, text="Settings", font=("Nimbus Mono PS", 12), bg="black",
                            fg="white", bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=settings)

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

    PauseResume = Button(root, text="resume", font=("Nimbus Mono PS", 12), bg="black", fg="white",
                         bd=3, relief=RAISED, padx=10, pady=5, width=16, height=2, command=resumeGame)

    PauseCheats = Button(root, text="cheats", font=("Nimbus Mono PS", 12), bg="black", fg="white",
                         bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=cheatCodeEntry)

    PauseExit = Button(root, text="Save and Exit", font=("Nimbus Mono PS", 12), bg="black", fg="white",
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
    MenuToPause = Button(root, text="Menu", font=("Nimbus Mono PS", 12), bg="black", fg="white",
                         bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=inGameMenuPause)
    btn_MenuToPause = MenuToPause
    canvas.create_window(150, 50, anchor=CENTER, window=MenuToPause)
    pause = False
    pass


def inGameExit():
    global pause, gameRunning, game_loop_id

    save_Game(PlayerName, score, (p1.x, p1.y), p1.vel, [[platform.getPlatformX(
    ), platform.getPlatformHeight()] for platform in allPlatforms], [background1.x, background1.y], [background2.x, background2.y],
    [background_upper1.x,background_upper1.y],[background_upper2.x,background_upper2.y])

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
        
    # Label to display the result
    resultLabel = Label(root, text="")
    resultLabelWindow = canvas.create_window(
        width//2, height//2-200, anchor=CENTER, window=resultLabel)

    # Entry widget
    textEntry = Entry(root, width=30)
    textEntryWindow = canvas.create_window(
        width//2, height//2-100, anchor=CENTER, window=textEntry)

    # Button to retrieve text
    textButton = Button(root, text="Get Text", command=get_text)
    textButtonWindow = canvas.create_window(
        width//2, height//2, anchor=CENTER, window=textButton)

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
        background_upper2.update_background()
        background_upper1.update_background()
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
    global game_loop_id, platform1, platform2, platform3
    # only reset the position of the elements on the canvas
    if game_loop_id:
        gameRunning = True
        update_Leaderboard(PlayerName, score)
        print(read_leaderboard_binary_file())
        p1.resetPosition()
        platform1.resetPos(0, 500) 
        if randint(1, 2) == 1:
            platform2.resetPos(
                1000, max(platform1.getPlatformHeight()-int(platform_offset()),400))
        else:
            platform2.resetPos(
                1000, min(700,platform1.getPlatformHeight()+int(platform_offset())))
        if randint(1, 2) == 1:
            platform3.resetPos(
                2000, max(400,platform2.getPlatformHeight()-int(platform_offset())))
        else:
            platform3.resetPos(
                2000, min(700,platform2.getPlatformHeight()+int(platform_offset())))
        set_score(0)

        # next we rest the positions of p1 and the platforms


# key binding related
# Function to set the flag when the up key is released



def key_press(event):
    global entry
    try:
        if event.keysym == bindedJump:
            p1.jump()

    except:
        pass
    if event.keysym == "b" and root.focus_get() != entry:
        Bk.bossKeyCreate()

# Function to clear the flag when the up key is released


def key_release(event):
    try:
        if event.keysym == bindedJump:
            p1.stopJump()
    except:
        pass


# Bind the key press and release events
root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)
loadMenu()
root.mainloop()
