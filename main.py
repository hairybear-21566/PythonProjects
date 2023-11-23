################################
# SCREEN RESOLUTION : 1366 x 768
###############################
from tkinter import CENTER, Tk, Canvas, Button, RAISED, PhotoImage, NW, Entry, CENTER, Label
from random import randint
import Bosskey_Handler as Bk
from Platform_Class import Platforms
from Player_Class import Player
from Background_Class import GameBackground
from Player_Saves_Handler import save_Game, read_saves_binary_file
from Leaderboard_Handler import update_Leaderboard, read_leaderboard_binary_file
from Crow_Class import Crow
from typing import Union  # Union[int,float] <- allows for multiple type hints

# for commiting everything:
# git add --all --include-unmodified


class Game_State_Manger:
    # Creating application window

    def __init__(self):
        self.root = Tk()
        self.width = 1366
        self.height = 768
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x1 = (self.screen_width - self.width) // 2
        self.y1 = (self.screen_height - self.height) // 2
        self.root.geometry(f"{self.width}x{self.height}+{self.x1}+{self.y1}")
        self.root.config(bg="#444444")

        # Canvas creation
        self.canvas = Canvas(self.root, width=self.width,
                             height=self.height, bg="black")
        self.canvas.place(x=(1366-self.width)//2, y=(820-self.height)//2)

        # misc variable
        # Cheat Codes are "double points", "baby steps"(not ready), "pew pew"(definetley not ready)
        self.super_jump_keys = {"o": False, "p": False}
        self.cheat_codes = ["triple_points", "super_jump"]
        self.cheat_codes_actived = {s: False for s in self.cheat_codes}

        self.bindedJump = "space"                                       # global Jump
        self.game_loop_id = None                                     # gameloop ID
        self.pause = False                                           # pause
        # used to check if game is running
        self.gameSpawned = False
        self.gameRunning = True
        self.entry_focused = False
        # score for current run
        self.score = 0
        self.starting_scroll_speed = 6
        self.player_size = 25

        # hold boss key window instance
        self.bossKeyWindow = None
        # player name entered into the entry field in main menu
        self.PlayerName = None
        # last global stored saves array from binary file containing player saves
        self.current_Player_saves = []
        self.entry_var = None
        self.platform1 = None
        self.platform2 = None
        self.platform3 = None
        self.allPlatforms = None
        self.num_of_birds = 5
        self.bird_speed = 4
        self.start_bird_pos = 2000
        self.birds_array = None

        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        self.root.protocol("WM_DELETE_WINDOW", self.auto_save)
        self.loadMenu()
        self.root.mainloop()

    #############################
    # misc
    #############################

    def auto_save(self) -> None:

        try:

            save_Game(self.PlayerName, self.score, (self.p1.x, self.p1.y), self.p1.vel,
                      [[platform.getPlatformX(), platform.getPlatformHeight()]
                       for platform in self.allPlatforms],
                      [self.background1.x, self.background1.y],
                      [self.background2.x, self.background2.y],
                      [self.background_upper1.x, self.background_upper1.y], [
                          self.background_upper2.x, self.background_upper2.y],
                      self.platform1.scrollSpeed,
                      [[self.birds_array[i].image_x, self.birds_array[i].image_y, self.birds_array[i].scroll_speed, self.birds_array[i].tag] for i in range(len(self.birds_array))])

            self.set_score(0)
            self.clearCanvas()
            self.root.after_cancel(self.game_loop_id)
            self.gameRunning = False  # Stop the game loop
            self.pause = True

            self.root.destroy()
        except:
            self.root.destroy()

    def clearCanvas(self) -> None:
        self.canvas.delete("all")

    def set_score(self, n: int) -> None:

        self.score = n
        self.score_text.config(text="Score: "+str(n))

    def platform_offset(self) -> None:
        return randint(0, int(150//1.7))
        # return 150

    ##########################
    # main menu functions
    ##########################

    def startNewGame(self) -> None:
        self.root.focus_set()

        if self.PlayerName != "Player Name" or self.PlayerName.strip() == "":
            self.loadGame(True)
            self.gameRunning = True
            self.pause = False

    def loadGame(self, new: bool) -> None:

        self.root.focus_set()
        player_details_arr = False
        for p in read_saves_binary_file():
            if p["player_name"] == self.PlayerName:
                player_details_arr = list(p.values())
                # print(player_details_arr)
                break

        if player_details_arr == False or new == True:
            n2 = min(500 + int(self.platform_offset()), 700) if randint(1,
                                                                2) == 1 else max(500 - int(self.platform_offset()), 400)
            n3 = min(n2 + int(self.platform_offset()), 700) if randint(1,
                                                                       2) == 1 else max(n2 - int(self.platform_offset()), 400)
            player_details_arr = [
                self.PlayerName,
                0,
                [200, 400],
                0,
                [[0, 500], [1000, n2], [2000, n3],],
                [0, 0],
                [1366, 0],
                [0, 0],
                [1366, 0],
                self.starting_scroll_speed, [[self.start_bird_pos+1000*i, randint(
                    400, 600), self.bird_speed, "bird "+str(i)]for i in range(self.num_of_birds)]
            ]

        self.clearCanvas()
        self.gameSpawned = True
        self.background_upper1 = GameBackground(
            player_details_arr[7][0], player_details_arr[7][1], "gameassets/back-clouds.png", "background_upper1", self.canvas, 3)
        self.background_upper2 = GameBackground(
            player_details_arr[8][0], player_details_arr[8][1], "gameassets/back-clouds.png", "background_upper2", self.canvas, 3)

        self.background1 = GameBackground(
            player_details_arr[5][0], player_details_arr[5][1], "gameassets/starry-night.png", "background1", self.canvas, 1)

        self.background2 = GameBackground(
            player_details_arr[6][0], player_details_arr[6][1], "gameassets/starry-night.png", "background2", self.canvas, 1)

        self.score = player_details_arr[1]

        self.score_text = Label(self.root, bg="black", fg="white", font=(
            "Nimbus Mono PS", 12), text="Score: " + str(self.score))
        self.canvas.create_window(self.width // 2, self.height // 2 - 300,
                                  anchor=CENTER, window=self.score_text)

        self.playingGameMenuButton()
        self.p1 = Player(player_details_arr[2][0],
                         player_details_arr[2][1], self.player_size, self.canvas)
        self.p1.vel = player_details_arr[3]

        # creating platforms with correct initial x positions
        self.platform1 = Platforms(
            player_details_arr[4][0][0], player_details_arr[4][0][1], player_details_arr[9], self.canvas)
        self.platform2 = Platforms(
            player_details_arr[4][1][0], player_details_arr[4][1][1], player_details_arr[9], self.canvas)
        self.platform3 = Platforms(
            player_details_arr[4][2][0], player_details_arr[4][2][1], player_details_arr[9], self.canvas)

        # Update allPlatforms with the new platform instances
        self.allPlatforms = [self.platform1, self.platform2, self.platform3]

        self.birds_array = [Crow(player_details_arr[10][i][0],
                            player_details_arr[10][i][1],
                            player_details_arr[10][i][2],
                            f"gameassets/crows-64/crow-size-64-{str(1)}.png",
                                 player_details_arr[10][i][3],
                                 self.canvas) for i in range(len(player_details_arr[10]))]

        self.pause = False
        self.gameRunning = True
        self.gameLoop()

    def leaderboard(self) -> None:
        self.root.focus_set()
        self.clearCanvas()

        def goBack() -> None:
            self.clearCanvas()
            self.loadMenu()

        rankings = read_leaderboard_binary_file()
        places = len(rankings)
        i = 0

        self.label_title = Label(self.root, text="LEADERBOARD", font=(
            "Nimbus Mono PS", 30), bg="black", fg="white")
        label_title_window = self.canvas.create_window(
            self.width // 2, 100, anchor=CENTER, window=self.label_title)

        while i != places:

            label1 = Label(self.root, text=rankings[i]["player_name"], font=(
                "Nimbus Mono PS", 12), bg="black", fg="white")
            label1_window = self.canvas.create_window(
                self.width // 2 - 50, self.height // 2 - 200 + 100*i, anchor=CENTER, window=label1)

            label2 = Label(self.root, text=rankings[i]["score"], font=(
                "Nimbus Mono PS", 12), bg="black", fg="white")
            label2_window = self.canvas.create_window(
                self.width // 2 + 50, self.height // 2 - 200+100*i, anchor=CENTER, window=label2)
            i += 1

        back_button = Button(self.root, text="Back", font=("Nimbus Mono PS", 12), bg="black", fg="white",
                             bd=3, relief=RAISED, padx=10, pady=5, width=10, height=2, command=goBack)
        self.canvas.create_window(self.width // 2, self.height // 2 + 300,
                                  anchor=CENTER, window=back_button)

    def settings(self):

        self.root.focus_set()
        self.clearCanvas()

        def goBack() -> None:
            self.clearCanvas()
            self.loadMenu()

        def set_bind_jump(new_jump_bind: str) -> None:

            if new_jump_bind == "space":
                self.bindedJump = new_jump_bind
                bind_jump_button2.config(state="disabled")
                bind_jump_button.config(state="normal")
            else:
                self.bindedJump = new_jump_bind
                bind_jump_button2.config(state="normal")
                bind_jump_button.config(state="disabled")

        binded_jump_label = Label(self.root, text=f"Binded Jump: {self.bindedJump}", font=(
            "Nimbus Mono PS", 12), bg="black", fg="white")
        binded_jump_label_window = self.canvas.create_window(
            self.width // 2, self.height // 2-100, anchor=CENTER, window=binded_jump_label)

        bind_jump_button = Button(self.root, text="Up Arrow", font=("Nimbus Mono PS", 12), bg="black", fg="white", bd=3,
                                  relief=RAISED, padx=10, pady=5, width=12, height=2, command=lambda: set_bind_jump("Up"))
        bind_jump_button_window = self.canvas.create_window(self.width // 2 - 150, self.height // 2 - 20, anchor=CENTER,
                                                            window=bind_jump_button)

        bind_jump_button2 = Button(self.root, text="space", font=("Nimbus Mono PS", 12), bg="black", fg="white", bd=3,
                                   relief=RAISED, padx=10, pady=5, width=12, height=2, command=lambda: set_bind_jump("space"))
        bind_jump_button2_window = self.canvas.create_window(self.width // 2 + 150, self.height // 2 - 20, anchor=CENTER,
                                                             window=bind_jump_button2)

        set_bind_jump(self.bindedJump)

        back_button = Button(self.root, text="Back", font=("Nimbus Mono PS", 12), bg="black", fg="white", bd=3,
                             relief=RAISED, padx=10, pady=5, width=10, height=2, command=goBack)
        back_button_window = self.canvas.create_window(
            self.width // 2, self.height // 2 + 100, anchor=CENTER, window=back_button)

    def loadMenu(self):

        label_title = Label(self.root, text="NIGHT CRAWLER", font=(
            "C059", 40), bg="black", fg="dark red")
        label_title_window = self.canvas.create_window(
            self.width // 2, 100, anchor=CENTER, window=label_title)

        placeholder = "Player Name"

        def on_entry_change(event, running: bool) -> None:
            if running:
                self.root.after(1, update_change)

        def update_change() -> None:
            name = self.entry.get()
            self.PlayerName = name
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

        self.entry = Entry(self.root, width=20)
        self.entry.insert(0, placeholder)
        entry_window = self.canvas.create_window(
            self.width//2, self.height//2-200, anchor=CENTER, window=self.entry)
        # Bind the <Key> event to the entry field
        self.entry.bind('<Key>', lambda x: on_entry_change(
            x, self.gameRunning or self.gameSpawned))

        def on_entry_click(event: object) -> None:

            self.entry_focused = True
            if self.entry.get() == placeholder:
                self.entry.delete(0, "end")
                self.entry.config(fg='black')

        def on_focus_out(event: object) -> None:

            self.entry_focused = False
            if self.entry.get() == '':
                self.entry.insert(0, placeholder)
                self.entry.config(fg='grey')

        self.entry.bind('<FocusIn>', on_entry_click)
        self.entry.bind('<FocusOut>', on_focus_out)

        current_Player_saves = read_saves_binary_file()

        startNewGameButton = Button(self.root, text="New Game", font=("Nimbus Mono PS", 12), bg="black",
                                    fg="white", bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=self.startNewGame, state="disabled")

        loadGameButton = Button(self.root, text="Load Game", font=("Nimbus Mono PS", 12), bg="black",
                                fg="white", bd=3, relief=RAISED, padx=10, pady=5, width=16, height=2, command=lambda: self.loadGame(False), state="disabled")

        leaderboardButton = Button(self.root, text="Leaderboard", font=("Nimbus Mono PS", 12), bg="black",
                                   fg="white", bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=self.leaderboard)

        settingsButton = Button(self.root, text="Settings", font=("Nimbus Mono PS", 12), bg="black",
                                fg="white", bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=self.settings)

        self.canvas.create_window(self.width//2, self.height//2-100,
                                  anchor=CENTER, window=startNewGameButton)
        self.canvas.create_window(self.width//2, self.height//2,
                                  anchor=CENTER, window=loadGameButton)
        self.canvas.create_window(self.width//2, self.height//2+100,
                                  anchor=CENTER, window=leaderboardButton)
        self.canvas.create_window(self.width//2, self.height//2+200,
                                  anchor=CENTER, window=settingsButton)

    #############################################
    # In Game Mangement Functions
    #############################################

    def inGameMenuPause(self) -> None:
        self.pause = True
        PauseResume = Button(self.root, text="resume", font=("Nimbus Mono PS", 12), bg="black", fg="white",
                             bd=3, relief=RAISED, padx=10, pady=5, width=16, height=2, command=self.resumeGame)

        PauseCheats = Button(self.root, text="cheats", font=("Nimbus Mono PS", 12), bg="black", fg="white",
                             bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=self.cheatCodeEntry)

        PauseExit = Button(self.root, text="Save and Exit", font=("Nimbus Mono PS", 12), bg="black", fg="white",
                           bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=self.inGameExit)

        self.btnPauseResume = PauseResume
        self.btnPauseCheats = PauseCheats
        self.btnPauseExit = PauseExit

        self.canvas.create_window(self.width//2, self.height//2-100,
                                  anchor=CENTER, window=self.btnPauseResume)
        self.canvas.create_window(self.width//2, self.height//2,
                                  anchor=CENTER, window=self.btnPauseCheats)
        self.canvas.create_window(self.width//2, self.height//2+100,
                                  anchor=CENTER, window=self.btnPauseExit)

        self.btn_MenuToPause.destroy()

    def playingGameMenuButton(self) -> None:

        self.MenuToPause = Button(self.root, text="Menu", font=("Nimbus Mono PS", 12), bg="black", fg="white",
                                  bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=self.inGameMenuPause)
        self.btn_MenuToPause = self.MenuToPause
        self.in_game_menu_id = self.canvas.create_window(
            150, 50, anchor=CENTER, window=self.MenuToPause)
        self.pause = False

    def inGameExit(self) -> None:

        save_Game(self.PlayerName, self.score, (self.p1.x, self.p1.y), self.p1.vel,
                  [[platform.getPlatformX(), platform.getPlatformHeight()]
                   for platform in self.allPlatforms],
                  [self.background1.x, self.background1.y],
                  [self.background2.x, self.background2.y],
                  [self.background_upper1.x, self.background_upper1.y], [
                      self.background_upper2.x, self.background_upper2.y],
                  self.platform1.scrollSpeed,
                  [[self.birds_array[i].image_x, self.birds_array[i].image_y, self.birds_array[i].scroll_speed, self.birds_array[i].tag] for i in range(len(self.birds_array))])

        self.set_score(0)
        self.clearCanvas()
        self.root.after_cancel(self.game_loop_id)
        self.gameRunning = False  # Stop the game loop
        self.pause = True
        self.loadMenu()

    def resumeGame(self) -> None:

        self.pause = False
        arr = [self.btnPauseResume,  self.btnPauseCheats, self.btnPauseExit]
        for i in range(len(arr)):
            arr[i].destroy()
        self.playingGameMenuButton()
        self.gameLoop()

    def cheatCodeEntry(self) -> None:
        arr = [self.btnPauseResume,  self.btnPauseCheats, self.btnPauseExit]
        for i in range(len(arr)):
            arr[i].destroy()

        def set_triple_points(choice: bool) -> None:
            if choice:
                textButton1.config(state="disabled")
                textButton2.config(state="normal")
                self.cheat_codes_actived["triple_points"] = True
            else:
                textButton2.config(state="disabled")
                textButton1.config(state="normal")
                self.cheat_codes_actived["triple_points"] = False

        def goBack() -> None:
            textButton1.destroy()
            textButton2.destroy()
            self.canvas.delete(textButtonWindow1)
            self.canvas.delete(textButtonWindow2)
            self.canvas.delete(backButtonWindow)
            backButton.destroy()
            self.inGameMenuPause()

        textButton1 = Button(self.root, bg="black", fg="white", font=(
            "Nimbus Mono PS", 12), text="Activate triple points", command=lambda: set_triple_points(True))
        textButtonWindow1 = self.canvas.create_window(
            self.width//2-150, self.height//2-100, anchor=CENTER, window=textButton1)
        textButton2 = Button(self.root, bg="black", fg="white", font=(
            "Nimbus Mono PS", 12), text="Deactivate triple points", command=lambda: set_triple_points(False))
        textButtonWindow2 = self.canvas.create_window(
            self.width//2+150, self.height//2-100, anchor=CENTER, window=textButton2)

        set_triple_points(self.cheat_codes_actived["triple_points"])

        backButton = Button(self.root, bg="black", fg="white", font=(
            "Nimbus Mono PS", 12), text="Back", command=goBack)
        backButtonWindow = self.canvas.create_window(
            self.width//2, self.height//2+100, anchor=CENTER, window=backButton)

    ##########################
    # game cycle management
    ##########################

    def gameLoop(self) -> None:

        if self.gameRunning and not self.pause:
            self.set_score(
                self.score+(3 if self.cheat_codes_actived["triple_points"] else 1))
            again = self.p1.updatePlayer(self.allPlatforms, self.restartGame)
            if again:
                self.background1.update_background()
                self.background2.update_background()
                self.background_upper2.update_background()
                self.background_upper1.update_background()
                maxJumpHeight = self.p1.maxJumpHeight()
                for b in self.birds_array:
                    again2 = b.update_crow(
                        [self.p1.x, self.p1.y, self.p1.x+self.p1.size, self.p1.y+self.p1.size], self.restartGame)
                    if not again2:
                        break

                lastPlatForm = self.platform1
                for p in self.allPlatforms:
                    if p.getPlatformX() > lastPlatForm.getPlatformX():
                        lastPlatForm = p
                for platform in self.allPlatforms:
                    platform.updatePlatform(heightOfLastPlatform=lastPlatForm.getPlatformHeight(
                    ), xOfLastPlatform=lastPlatForm.getPlatformX(), maxPlayerJumpHeight=maxJumpHeight)
                    platform.changeScrollSpeed(
                        self.starting_scroll_speed, self.score)
            if again and again2:
                self.game_loop_id = self.root.after(20, self.gameLoop)

    def restartGame(self) -> None:
        def count_down_display(n: int) -> None:
            self.count = PhotoImage(file="gameassets/count-down"+str(n)+".png")
            countdown_label_id = self.canvas.create_image(self.width//2, self.height//2,
                                                          anchor=CENTER, image=self.count)
            self.root.after(
                800, lambda: delete_countdown_label(countdown_label_id))

        def delete_countdown_label(id: int) -> None:
            self.canvas.delete(id)

        if self.game_loop_id:

            self.gameRunning = True
            update_Leaderboard(self.PlayerName, self.score)

            self.p1.resetPosition()
            self.platform1.resetPos(0, 500)
            if randint(1, 2) == 1:
                self.platform2.resetPos(
                    1000, max(self.platform1.getPlatformHeight()-int(self.platform_offset()), 400))
            else:
                self.platform2.resetPos(
                    1000, min(700, self.platform1.getPlatformHeight()+int(self.platform_offset())))
            if randint(1, 2) == 1:
                self.platform3.resetPos(
                    2000, max(400, self. platform2.getPlatformHeight()-int(self.platform_offset())))
            else:
                self.platform3.resetPos(
                    2000, min(700, self.platform2.getPlatformHeight()+int(self.platform_offset())))

            self.set_score(0)

            for bird in range(len(self.birds_array)):
                self.birds_array[bird].reset_pos(bird, self.start_bird_pos)

            self.canvas.delete(self.in_game_menu_id)
            count_down_display(3)

            self.root.after(1000, lambda: count_down_display(2))
            self.root.after(2000, lambda: count_down_display(1))

            self.root.after(3000, lambda: (
                self.gameLoop(), self.playingGameMenuButton()))

    #########################
    # key event management
    #########################
    def key_press(self, event) -> None:

        try:
            if event.keysym == self.bindedJump:
                self.p1.jump()

        except:
            pass
        if event.keysym == "b" and self.root.focus_get() != self.entry:
            Bk.bossKeyCreate()

        if event.keysym == "t" and self.root.focus_get() != self.entry:
            self.cheat_codes_actived["triple_points"] = not self.cheat_codes_actived["triple_points"]

        if event.keysym == "o" and self.root.focus_get() != self.entry:
            self.super_jump_keys["o"] = True
            self.cheat_codes_actived["super_jump"] = self.super_jump_keys["o"] and self.super_jump_keys["p"]
            if self.cheat_codes_actived["super_jump"]:
                try:
                    self.p1.jumpForce = -27
                except:
                    pass

        if event.keysym == "p" and self.root.focus_get() != self.entry:
            self.super_jump_keys["p"] = True
            self.cheat_codes_actived["super_jump"] = self.super_jump_keys["o"] and self.super_jump_keys["p"]
            if self.cheat_codes_actived["super_jump"]:
                try:
                    self.p1.jumpForce = -27
                except:
                    pass


    def key_release(self, event) -> None:
        try:
            if event.keysym == self.bindedJump:
                self.p1.stopJump()
        except:
            pass
        if event.keysym == "o" and self.root.focus_get() != self.entry:
            self.super_jump_keys["o"] = False
            self.cheat_codes_actived["super_jump"] = False
            try:
                self.p1.jumpForce = -20
            except:
                pass

        if event.keysym == "p" and self.root.focus_get() != self.entry:
            self.super_jump_keys["p"] = False
            self.cheat_codes_actived["super_jump"] = False
            try:
                self.p1.jumpForce = -20
            except:
                pass


Game = Game_State_Manger()
