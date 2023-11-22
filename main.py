#####################
# SCREEN RESOLUTION : 1366 x 768
#####################

from tkinter import CENTER, Tk, Canvas, Button, RAISED, PhotoImage, NW, Entry, CENTER, Label
from random import randint
import Bosskey_Handler as Bk
from Platform_Class import Platforms
from Player_Class import Player
from Background_Class import GameBackground
from Player_Saves_Handler import save_Game, read_saves_binary_file
from Leaderboard_Handler import update_Leaderboard, read_leaderboard_binary_file
from Crow_Class import Crow


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
cheat_codes = ["triple_points"]
cheat_codes_actived = {s: False for s in cheat_codes}

bindedJump = "space"                                       # global Jump
game_loop_id = None                                     # gameloop ID
pause = False                                           # pause
# used to check if game is running
gameSpawned = False
gameRunning = True
entry_focused = False
score = 0                                               # score for current run
starting_scroll_speed = 9
player_size = 15

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
num_of_birds=3
bird_speed=4
start_bird_pos=2000
birds_array = None

# [Crow(2000+i*1000,randint(450,650),bird_speed,f"GameTests/crow-size-32/crow-size-32-{str(1)}.png", "bird "+str(i), canvas) for i in range(num_of_birds)]


# clear canvas

def auto_save():
    global pause, gameRunning, game_loop_id
    try:

        save_Game(PlayerName, score, (p1.x, p1.y), p1.vel, [[platform.getPlatformX(
        ), platform.getPlatformHeight()] for platform in allPlatforms], [background1.x, background1.y], [background2.x, background2.y],
            [background_upper1.x, background_upper1.y], [background_upper2.x, background_upper2.y], 
            platform1.scrollSpeed,[[birds_array[i].image_x,birds_array[i].image_y,birds_array[i].scroll_speed,birds_array[i].tag] for i in range(len(birds_array))])

        set_score(0)
        clearCanvas()
        root.after_cancel(game_loop_id)
        gameRunning = False  # Stop the game loop
        pause = True

        root.destroy()
    except:
        root.destroy()


def clearCanvas():
    canvas.delete("all")

# setters and getters settings functions


def set_score(n):
    global score
    score = n
    score_text.config(text="Score: "+str(n))


def platform_offset():
    global p1
    return randint(0, int(150//1.7))
    # return 150

#############################################
# Main Menu Functions
#############################################


def startNewGame():
    root.focus_set()
    global gameRunning, pause, entry
    if PlayerName != "Player Name" or PlayerName.strip() == "":
        loadGame(True)
        gameRunning = True
        pause = False


def loadGame(new):
    global birds_array,background1, score, background2, p1, platform1, platform2, platform3,num_of_birds, bird_speed, start_bird_pos
    global allPlatforms, score_text, pause, gameRunning, background_upper1, background_upper2, gameSpawned
    root.focus_set()
    player_details_arr = False

    for p in read_saves_binary_file():
        if p["player_name"] == PlayerName:
            player_details_arr = list(p.values())
            # print(player_details_arr)
            break

    if player_details_arr == False or new==True:
        n2 = min(500 + int(platform_offset()), 700) if randint(1,
                                                               2) == 1 else max(500 - int(platform_offset()), 400)
        n3 = min(n2 + int(platform_offset()), 700) if randint(1,
                                                              2) == 1 else max(n2 - int(platform_offset()), 400)
        player_details_arr = [
            PlayerName,
            0,
            [200, 400],
            0,
            [
                [0, 500],
                [1000, n2],
                [2000, n3],

            ],
            [0, 0],
            [1366, 0],
            [0, 0],
            [1366, 0],
            starting_scroll_speed,[[start_bird_pos+1000*i,randint(400,600),2,"bird "+str(i)]for i in range(num_of_birds)] 
            # x:int,y:int,scrollSpeed:int,filepath:str,tag_id:str,canvas:Canvas
            # what we save: x, y, scrollSpeed,tag
        ]

    clearCanvas()
    gameSpawned = True
    background_upper1 = GameBackground(
        player_details_arr[7][0], player_details_arr[7][1], "gameassets/back-clouds.png", "background_upper1", canvas, 2)
    background_upper2 = GameBackground(
        player_details_arr[8][0], player_details_arr[8][1], "gameassets/back-clouds.png", "background_upper2", canvas, 2)

    background1 = GameBackground(
        player_details_arr[5][0], player_details_arr[5][1], "gameassets/starry-night.png", "background1", canvas, 1)

    background2 = GameBackground(
        player_details_arr[6][0], player_details_arr[6][1], "gameassets/starry-night.png", "background2", canvas, 1)

    score = player_details_arr[1]

    score_text = Label(root, bg="black", fg="white", font=(
        "Nimbus Mono PS", 12), text="Score: " + str(score))
    canvas.create_window(width // 2, height // 2 - 300,
                         anchor=CENTER, window=score_text)

    playingGameMenuButton()
    p1 = Player(player_details_arr[2][0],
                player_details_arr[2][1], player_size, canvas)
    p1.vel = player_details_arr[3]

    # creating platforms with correct initial x positions
    platform1 = Platforms(
        player_details_arr[4][0][0], player_details_arr[4][0][1], player_details_arr[9], canvas)
    platform2 = Platforms(
        player_details_arr[4][1][0], player_details_arr[4][1][1], player_details_arr[9], canvas)
    platform3 = Platforms(
        player_details_arr[4][2][0], player_details_arr[4][2][1], player_details_arr[9], canvas)

    # Update allPlatforms with the new platform instances
    allPlatforms = [platform1, platform2, platform3]

    birds_array = [Crow(player_details_arr[10][i][0],
                        player_details_arr[10][i][1],
                        player_details_arr[10][i][2],
                        f"GameTests/crow-size-32/crow-size-32-{str(1)}.png", 
                        player_details_arr[10][i][3],
                        canvas) for i in range(len(player_details_arr[10]))]


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

    back_button = Button(root, text="Back", font=("Nimbus Mono PS", 12), bg="black", fg="white",
                         bd=3, relief=RAISED, padx=10, pady=5, width=10, height=2, command=goBack)
    canvas.create_window(width // 2, height // 2 + 300,
                         anchor=CENTER, window=back_button)


def settings():
    global bindedJump
    root.focus_set()
    clearCanvas()

    def goBack():
        clearCanvas()
        loadMenu()

    def set_bind_jump(new_jump_bind: str):
        global bindedJump
        print(new_jump_bind)
        if new_jump_bind == "space":
            bindedJump = new_jump_bind
            bind_jump_button2.config(state="disabled")
            bind_jump_button.config(state="normal")
        else:
            bindedJump = new_jump_bind
            bind_jump_button2.config(state="normal")
            bind_jump_button.config(state="disabled")

        pass

    def get_bind_jump():
        global bindedJump
        return bindedJump

    binded_jump_label = Label(root, text=f"Binded Jump: {get_bind_jump()}", font=(
        "Nimbus Mono PS", 12), bg="black", fg="white")
    binded_jump_label_window = canvas.create_window(
        width // 2, height // 2-100, anchor=CENTER, window=binded_jump_label)

    bind_jump_button = Button(root, text="Up Arrow", font=("Nimbus Mono PS", 12), bg="black", fg="white", bd=3,
                              relief=RAISED, padx=10, pady=5, width=12, height=2, command=lambda: set_bind_jump("Up"))
    bind_jump_button_window = canvas.create_window(width // 2 - 150, height // 2 - 20, anchor=CENTER,
                                                   window=bind_jump_button)

    bind_jump_button2 = Button(root, text="space", font=("Nimbus Mono PS", 12), bg="black", fg="white", bd=3,
                               relief=RAISED, padx=10, pady=5, width=12, height=2, command=lambda: set_bind_jump("space"))
    bind_jump_button2_window = canvas.create_window(width // 2 + 150, height // 2 - 20, anchor=CENTER,
                                                    window=bind_jump_button2)

    set_bind_jump(bindedJump)

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
                            fg="white", bd=3, relief=RAISED, padx=10, pady=5, width=16, height=2, command=lambda: loadGame(False), state="disabled")

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
    global btn_MenuToPause, pause, in_game_menu_id
    MenuToPause = Button(root, text="Menu", font=("Nimbus Mono PS", 12), bg="black", fg="white",
                         bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=inGameMenuPause)
    btn_MenuToPause = MenuToPause
    in_game_menu_id = canvas.create_window(
        150, 50, anchor=CENTER, window=MenuToPause)
    pause = False
    pass


def inGameExit():
    global pause, gameRunning, game_loop_id

    save_Game(PlayerName, score, (p1.x, p1.y), p1.vel, [[platform.getPlatformX(
    ), platform.getPlatformHeight()] for platform in allPlatforms], [background1.x, background1.y], [background2.x, background2.y],
        [background_upper1.x, background_upper1.y], [background_upper2.x, background_upper2.y], platform1.scrollSpeed,
        [[birds_array[i].image_x,birds_array[i].image_y,birds_array[i].scroll_speed,birds_array[i].tag] for i in range(len(birds_array))])

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

    def set_triple_points(choice):
        if choice:
            textButton1.config(state="disabled")
            textButton2.config(state="normal")
            cheat_codes_actived["triple_points"] = True
        else:
            textButton2.config(state="disabled")
            textButton1.config(state="normal")
            cheat_codes_actived["triple_points"] = False


    def goBack():
        textButton1.destroy()
        textButton2.destroy()
        canvas.delete(textButtonWindow1)
        canvas.delete(textButtonWindow2)
        canvas.delete(backButtonWindow)
        backButton.destroy()
        inGameMenuPause()

    textButton1 = Button(root, bg="black", fg="white", font=(
        "Nimbus Mono PS", 12), text="Activate triple points", command=lambda: set_triple_points(True))
    textButtonWindow1 = canvas.create_window(
        width//2-150, height//2-100, anchor=CENTER, window=textButton1)
    textButton2 = Button(root, bg="black", fg="white", font=(
        "Nimbus Mono PS", 12), text="Deactivate triple points", command=lambda: set_triple_points(False))
    textButtonWindow2 = canvas.create_window(
        width//2+150, height//2-100, anchor=CENTER, window=textButton2)

    set_triple_points(cheat_codes_actived["triple_points"])

    backButton = Button(root, bg="black", fg="white", font=(
        "Nimbus Mono PS", 12), text="Back", command=goBack)
    backButtonWindow = canvas.create_window(
        width//2, height//2+100, anchor=CENTER, window=backButton)


def gameLoop():
    global pause, game_loop_id, gameRunning
    if gameRunning and not pause:

        set_score(score+(3 if cheat_codes_actived["triple_points"] else 1))
        again = p1.updatePlayer(allPlatforms, restartGame)
        if again:
            background1.update_background()
            background2.update_background()
            background_upper2.update_background()
            background_upper1.update_background()
            maxJumpHeight = p1.maxJumpHeight()
            for b in birds_array:
                again2=b.update_crow([p1.x,p1.y,p1.x+p1.size,p1.y+p1.size],restartGame)
                if not again2:
                    break
                
            lastPlatForm = platform1
            for p in allPlatforms:
                if p.getPlatformX() > lastPlatForm.getPlatformX():
                    lastPlatForm = p
            for platform in allPlatforms:
                platform.updatePlatform(heightOfLastPlatform=lastPlatForm.getPlatformHeight(
            ), xOfLastPlatform=lastPlatForm.getPlatformX(), maxPlayerJumpHeight=maxJumpHeight)
                platform.changeScrollSpeed(starting_scroll_speed, score)
        
        if again and again2:
            game_loop_id = root.after(20, gameLoop)


def restartGame():
    def count_down_display(n):
        global countdown_label_id, count
        count = PhotoImage(file="gameassets/count-down"+str(n)+".png")
        countdown_label_id = canvas.create_image(width//2, height//2,
                                                 anchor=CENTER, image=count)
        root.after(800, delete_countdown_label)

    def delete_countdown_label():
        canvas.delete(countdown_label_id)

    global game_loop_id, platform1, platform2, platform3, countdown_label_id, in_game_menu_id, gameRunning, start_bird_pos
    # only reset the position of the elements on the canvas

    if game_loop_id:

        gameRunning = True
        update_Leaderboard(PlayerName, score)

        p1.resetPosition()
        platform1.resetPos(0, 500)
        if randint(1, 2) == 1:
            platform2.resetPos(
                1000, max(platform1.getPlatformHeight()-int(platform_offset()), 400))
        else:
            platform2.resetPos(
                1000, min(700, platform1.getPlatformHeight()+int(platform_offset())))
        if randint(1, 2) == 1:
            platform3.resetPos(
                2000, max(400, platform2.getPlatformHeight()-int(platform_offset())))
        else:
            platform3.resetPos(
                2000, min(700, platform2.getPlatformHeight()+int(platform_offset())))
        set_score(0)

        for bird in range(len(birds_array)):
            birds_array[bird].reset_pos(bird,start_bird_pos)

        canvas.delete(in_game_menu_id)
        count_down_display(3)

        root.after(1000, lambda: count_down_display(2))
        root.after(2000, lambda: count_down_display(1))

        root.after(3000, lambda: (gameLoop(), playingGameMenuButton()))

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

    if event.keysym == "t":
        cheat_codes_actived["triple_points"] = not cheat_codes_actived["triple_points"]

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
root.protocol("WM_DELETE_WINDOW", auto_save)
loadMenu()
root.mainloop()
