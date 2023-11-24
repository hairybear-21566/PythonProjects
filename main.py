################################
# SCREEN RESOLUTION : 1366 x 768
################################

################################
# Royalty Free Art Credits
# crow sprite sheets: https://meitdev.itch.io/crow
# player sprite sheets: https://plooody.itch.io/infinite-runner-pack
################################

from tkinter import CENTER, Tk, Canvas, Button, RAISED, PhotoImage, NW, Entry, CENTER, Label
from random import randint
import boss_key_handler as Bk
from platform_class import Platforms
from player_class import Player
from background_class import GameBackground
from player_saves import save_game, read_saves_binary_file
from leaderboard_handler import update_Leaderboard, read_leaderboard_binary_file
from crow_class import Crow


class GameStateManager:

    def __init__(self):
        """setting up all the core variables, constants, objects
        """
        # Creating application window
        self.root = Tk()   # type Tk
        self.WIDTH = 1366  # int, CONSTANT
        self.HEIGHT = 768  # int, CONSTANT
        self.SCREEN_WIDTH = self.root.winfo_screenwidth()   # int
        self.SCREEN_HEIGHT = self.root.winfo_screenheight()  # int
        self.X1 = (self.SCREEN_WIDTH - self.WIDTH) // 2     # int
        self.Y1 = (self.SCREEN_HEIGHT - self.HEIGHT) // 2   # int
        # below centers window and makes window 1366 x 768
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}+{self.X1}+{self.Y1}")
        self.root.config(bg="#444444") # setting background to black

        # Canvas creation
        self.canvas = Canvas(self.root, width=self.WIDTH,
                             height=self.HEIGHT, bg="black")  # tkinter.Canvas
        self.canvas.place(x=(1366-self.WIDTH)//2, y=(820-self.HEIGHT)//2)

        # misc variable
        # Cheat Codes are "double points", "super jump",
        # "pew pew"(definetley not ready)
        self.super_jump_keys = {"o": False, "p": False}  # dict{str:bool}
        self.cheat_codes = ["triple_points", "super_jump"]  # list[str]
        self.cheat_codes_actived = {
            s: False for s in self.cheat_codes}  # dict{str:bool}

        self.binded_jump = "space"  # str, global Jump
        self.game_loop_id = None    # int, game_loop ID
        self.pause = False          # bool, pause
        # used to check if game is running
        self.game_spawned = False   # bool, game ran for the first time
        self.game_running = True    # bool
        self.entry_focused = False  # text field focused in on
        # score for current run
        self.score = 0              # int, run score
        self.STARTING_SCROLL_SPEED = 6  # int, CONSTANT
        self.PLAYER_SIZE = 25  # int, CONSTANT
        self.NORMAL_JUMP = -22  # int, CONSTANT
        self.SUPER_JUMP = -30  # int, CONSTANT

        # hold boss key window instance
        self.boss_key_window = None
        # player name entered into the entry field in main menu
        self.player_name = None
        # last global stored saves array from
        # binary file containing player saves
        self.current_Player_saves = []
        # text entry variable
        self.entry_var = None
        # platform variables
        self.platform1 = None  # Class Platform
        self.platform2 = None  # ^
        self.platform3 = None  # ^
        # [platform1, platform2, platform3] when
        # the platforms are initialized
        self.all_platforms = None  # list[Class Platform]
        # bird related CONSTANTS
        self.NUM_OF_BIRDS = 3  # int, CONSTANT
        self.BIRD_SPEED = 4  # int, CONSTANT
        # bird related variables
        self.start_bird_pos = 2000  # int
        self.birds_array = None
        # key binds
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        # auto_save is set to run when window is to be destroyed
        self.root.protocol("WM_DELETE_WINDOW", self.auto_save)
        # setting up default state of game when opened
        self.load_Menu()
        self.root.mainloop()

    #############################
    # miscallaneous function
    #############################

    def auto_save(self) -> None:
        """method that saves the player's state if window is closed using the top right close window
        button
        """

        try:  # saves player run data when they try to destroy window
            # passes neccessary data to save player game into
            save_game(self.player_name, self.score, (self.p1.x, self.p1.y), self.p1.vel,
                      [[platform.get_platform_x(), platform.get_platform_height()]
                       for platform in self.all_platforms],
                      [self.background1.x, self.background1.y],
                      [self.background2.x, self.background2.y],
                      [self.background_upper1.x, self.background_upper1.y], [
                          self.background_upper2.x, self.background_upper2.y],
                      self.platform1.scroll_speed,
                      [[self.birds_array[i].image_x, self.birds_array[i].image_y, self.birds_array[i].scroll_speed, self.birds_array[i].tag] for i in range(len(self.birds_array))])

            self.set_score(0)
            self.clear_canvas()
            self.root.after_cancel(self.game_loop_id)
            # game states set to implied game running state has been exited
            self.game_running = False
            self.pause = True
            self.root.destroy()
        except:  # root is just destroyed if there is not
            self.root.destroy()

    # simply removes all polygons, images, and components from canvas
    def clear_canvas(self) -> None:
        self.canvas.delete("all")

    def set_score(self, n: int) -> None:
        """sets score to n and updates the score text

        Args:
            n (int): new value of the player's current run score
        """
        self.score = n
        self.score_text.config(text="Score: "+str(n))

    def platform_offset(self) -> int:
        """returns a random integer used for offseting adjacent platform heights

        Returns:
            int: integer ranges from 0 to 88
        """
        return randint(0, int(150//1.7))
        # return 150

    ##########################
    # main menu functions
    ##########################

    def start_new_game(self) -> None:
        """method called when start new game button clicked
        also ensures the player name is not empty of the default name thus meaning the entered
        player name is valid
        """
        self.root.focus_set()
        # ensures player name is valid (not empty or the default name)
        if self.player_name != "Player Name" or self.player_name.strip() == "":
            # game state managemnet variabels set to imply game running
            self.load_game(True)
            self.game_running = True
            self.pause = False

    def load_game(self, new: bool) -> None:

        self.root.focus_set()

        # if the player name has a save, player data is extracted from save file
        # this data is used to load the previous state of the game
        player_details_arr = False
        for p in read_saves_binary_file():
            if p["player_name"] == self.player_name:
                player_details_arr = list(p.values())
                break
        # else if the player name has no associated save data default data is used to start game instead
        if player_details_arr == False or new == True:
            n2 = min(500 + int(self.platform_offset()), 700) if randint(1,  # platform 2 height
                                                                        2) == 1 else max(500 - int(self.platform_offset()), 400)
            n3 = min(n2 + int(self.platform_offset()), 700) if randint(1,  # platform 3 height
                                                                       2) == 1 else max(n2 - int(self.platform_offset()), 400)
            # default set of save data values
            player_details_arr = [
                self.player_name, 0, [200, 400],
                0, [[0, 500], [1000, n2], [2000, n3],],
                [0, 0], [1366, 0], [0, 0], [1366, 0],
                self.STARTING_SCROLL_SPEED, [[self.start_bird_pos+1000*i, randint(
                    400, 600), self.BIRD_SPEED, "bird "+str(i)]for i in range(self.NUM_OF_BIRDS)]
            ]
        """player_details_arr = [player name, score, player starting position,
                                 player starting velocity vertically,
                                 positions of platforms,
                                 stars image 1 position,
                                 stars image 2 position,
                                 clouds image 1 position,
                                 clouds image 2 position,
                                 birds [x position, y position, speed of translation, tag] ]
        """
        self.clear_canvas()
        self.game_spawned = True
        # background initializations
        self.background_upper1 = GameBackground(
            player_details_arr[7][0], player_details_arr[7][1], "gameassets/clouds.png", "background_upper1", self.canvas, 3)
        self.background_upper2 = GameBackground(
            player_details_arr[8][0], player_details_arr[8][1], "gameassets/clouds.png", "background_upper2", self.canvas, 3)

        self.background1 = GameBackground(
            player_details_arr[5][0], player_details_arr[5][1], "gameassets/stars.png", "background1", self.canvas, 1)

        self.background2 = GameBackground(
            player_details_arr[6][0], player_details_arr[6][1], "gameassets/stars.png", "background2", self.canvas, 1)
        # starting score setting with score label
        self.score = player_details_arr[1]
        self.score_text = Label(self.root, bg="black", fg="white", font=(
            "Nimbus Mono PS", 12), text="Score: " + str(self.score))
        self.canvas.create_window(self.WIDTH // 2, self.HEIGHT // 2 - 300,
                                  anchor=CENTER, window=self.score_text)
        # creating pause/menu button
        self.playing_in_game_menu_button()

        # initilaize player at set their velocity
        self.p1 = Player(player_details_arr[2][0],
                         player_details_arr[2][1], self.PLAYER_SIZE, self.canvas)
        self.p1.vel = player_details_arr[3]

        # creating platforms with correct initial positions
        self.platform1 = Platforms(
            player_details_arr[4][0][0], player_details_arr[4][0][1], player_details_arr[9], self.canvas)
        self.platform2 = Platforms(
            player_details_arr[4][1][0], player_details_arr[4][1][1], player_details_arr[9], self.canvas)
        self.platform3 = Platforms(
            player_details_arr[4][2][0], player_details_arr[4][2][1], player_details_arr[9], self.canvas)

        # Update all_platforms with the new platform instances
        self.all_platforms = [self.platform1, self.platform2, self.platform3]

        self.birds_array = [Crow(player_details_arr[10][i][0],
                            player_details_arr[10][i][1],
                            player_details_arr[10][i][2],
                            f"gameassets/crows/crow-size-64-{str(1)}.png",
                                 player_details_arr[10][i][3],
                                 self.canvas) for i in range(len(player_details_arr[10]))]
        # set game state variables to imply the game is currently running
        self.pause = False
        self.game_running = True
        self.game_loop()  # starting main gameloop

    def leaderboard(self) -> None:
        """method used to create leaderboard page
        including creating the table
        and reading the rankings
        """
        self.root.focus_set()
        self.clear_canvas()
        # when function called, leaderboard page -> home/main menu page

        def go_back() -> None:
            self.clear_canvas()
            self.load_Menu()

        # obtaining top 5 or as many recordings saved
        rankings = read_leaderboard_binary_file()
        places = len(rankings)
        i = 0

        # Leaderboard title creation
        self.label_title = Label(self.root, text="LEADERBOARD", font=(
            "Nimbus Mono PS", 30), bg="black", fg="white")
        label_title_window = self.canvas.create_window(
            self.WIDTH // 2, 100, anchor=CENTER, window=self.label_title)

        # creating rows of the score
        # `player_name`: `score`
        while i != places:
            label1 = Label(self.root, text=rankings[i]["player_name"], font=(
                "Nimbus Mono PS", 12), bg="black", fg="white")
            label1_window = self.canvas.create_window(
                self.WIDTH // 2 - 50, self.HEIGHT // 2 - 200 + 100*i,
                anchor=CENTER, window=label1)

            label2 = Label(self.root, text=rankings[i]["score"], font=(
                "Nimbus Mono PS", 12), bg="black", fg="white")
            label2_window = self.canvas.create_window(
                self.WIDTH // 2 + 50, self.HEIGHT // 2 - 200+100*i,
                anchor=CENTER, window=label2)
            i += 1
        # back button creation that calls go_back when clicked
        back_button = Button(self.root, text="Back", font=("Nimbus Mono PS", 12),
                             bg="black", fg="white",
                             bd=3, relief=RAISED, padx=10, pady=5,
                             width=10, height=2, command=go_back)
        self.canvas.create_window(self.WIDTH // 2, self.HEIGHT // 2 + 300,
                                  anchor=CENTER, window=back_button)

    def settings(self):
        """settings page
        where key bindings can be changed
        """
        self.root.focus_set()
        self.clear_canvas()
        # settings page -> home/main menu page

        def go_back() -> None:
            self.clear_canvas()
            self.load_Menu()
        # function that controls which buttons in the settings page is on or off
        # bassed on the current jump binding

        def set_bind_jump(new_jump_bind: str) -> None:

            if new_jump_bind == "space":
                # new bind jump set
                self.binded_jump = new_jump_bind
                # bind jump to space deactivated
                bind_jump_button2.config(state="disabled")
                # bind jump to up activated
                bind_jump_button.config(state="normal")
            else:  # if new_bind_jump == "Up"
                # new bind jump set
                self.binded_jump = new_jump_bind
                # bind jump to space activated
                bind_jump_button2.config(state="normal")
                # bind jump to up deactivated
                bind_jump_button.config(state="disabled")

        binded_jump_label = Label(self.root, text=f"Binded Jump: {self.binded_jump}",
                                  font=("Nimbus Mono PS", 12), bg="black", fg="white")
        binded_jump_label_window = self.canvas.create_window(
            self.WIDTH // 2, self.HEIGHT // 2-100, anchor=CENTER,
            window=binded_jump_label)
        # binds jump to `Up` arrow
        bind_jump_button = Button(self.root, text="Up Arrow", font=("Nimbus Mono PS", 12),
                                  bg="black", fg="white", bd=3,
                                  relief=RAISED, padx=10, pady=5, width=12, height=2,
                                  command=lambda: set_bind_jump("Up"))
        bind_jump_button_window = self.canvas.create_window(self.WIDTH // 2 - 150,
                                                            self.HEIGHT // 2 - 20,
                                                            anchor=CENTER,
                                                            window=bind_jump_button)
        # binds jump to `space` bar
        bind_jump_button2 = Button(self.root, text="space", font=("Nimbus Mono PS", 12),
                                   bg="black", fg="white", bd=3,
                                   relief=RAISED, padx=10, pady=5, width=12,
                                   height=2, command=lambda: set_bind_jump("space"))
        bind_jump_button2_window = self.canvas.create_window(self.WIDTH // 2 + 150,
                                                             self.HEIGHT // 2 - 20,
                                                             anchor=CENTER,
                                                             window=bind_jump_button2)

        set_bind_jump(self.binded_jump)
        # back button creation
        back_button = Button(self.root, text="Back", font=("Nimbus Mono PS", 12),
                             bg="black", fg="white", bd=3,
                             relief=RAISED, padx=10, pady=5, width=10,
                             height=2, command=go_back)
        back_button_window = self.canvas.create_window(
            self.WIDTH // 2, self.HEIGHT // 2 + 100, anchor=CENTER, window=back_button)

    def load_Menu(self):
        """home/main menu page
        default state/ page when the player opens the game
        this contains the player name entry field, and buttons to
        settings page, leaderboard page, new game, load game save
        """
        label_title = Label(self.root, text="NIGHT CRAWLER", font=(
            "C059", 40), bg="black", fg="dark red")
        label_title_window = self.canvas.create_window(
            self.WIDTH // 2, 100, anchor=CENTER, window=label_title)

        placeholder = "Player Name"
        # when something is typed into the entry

        def on_entry_change(event, running: bool) -> None:
            if running:
                self.root.after(1, update_change)

        def update_change() -> None:
            name = self.entry.get()
            self.player_name = name
            found = False
            # checks to see if playername matches a save
            for d in current_Player_saves:
                if d["player_name"] == name:
                    load_game_button.config(state="normal")
                    start_new_game_button.config(state="normal")
                    found = True
                    break
            if name == placeholder or name.strip() == "":
                load_game_button.config(state="disabled")
                start_new_game_button.config(state="disabled")
            elif not found:
                load_game_button.config(state="disabled")
                start_new_game_button.config(state="normal")
        # creating entry field
        self.entry = Entry(self.root, width=20)
        self.entry.insert(0, placeholder)
        entry_window = self.canvas.create_window(
            self.WIDTH//2, self.HEIGHT//2-200, anchor=CENTER, window=self.entry)
        # Bind the <Key> event to the entry field
        self.entry.bind('<Key>', lambda x: on_entry_change(
            x, self.game_running or self.game_spawned))

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
        # start new game button creation
        start_new_game_button = Button(self.root, text="New Game", font=("Nimbus Mono PS", 12), bg="black",
                                       fg="white", bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=self.start_new_game, state="disabled")
        # load game button creation
        load_game_button = Button(self.root, text="Load Game", font=("Nimbus Mono PS", 12), bg="black",
                                  fg="white", bd=3, relief=RAISED, padx=10, pady=5, width=16, height=2, command=lambda: self.load_game(False), state="disabled")
        # leader board button creation
        leaderboard_button = Button(self.root, text="Leaderboard", font=("Nimbus Mono PS", 12), bg="black",
                                    fg="white", bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=self.leaderboard)
        # settings button creation
        settingsButton = Button(self.root, text="Settings", font=("Nimbus Mono PS", 12), bg="black",
                                fg="white", bd=3, relief=RAISED, padx=10, pady=5, width=15, height=2, command=self.settings)
        # placing all these buttons on to the canvas
        self.canvas.create_window(self.WIDTH//2, self.HEIGHT//2-100,
                                  anchor=CENTER, window=start_new_game_button)
        self.canvas.create_window(self.WIDTH//2, self.HEIGHT//2,
                                  anchor=CENTER, window=load_game_button)
        self.canvas.create_window(self.WIDTH//2, self.HEIGHT//2+100,
                                  anchor=CENTER, window=leaderboard_button)
        self.canvas.create_window(self.WIDTH//2, self.HEIGHT//2+200,
                                  anchor=CENTER, window=settingsButton)

    #############################################
    # In Game Mangement Functions
    #############################################

    def in_game_pause_menu(self) -> None:
        """the in game pause menu button
        also this functions handles
        resume button -> unpause game state
        cheat code button -> cheat code menu
        in game save and exit -> save game state and main menu
        """
        self.pause = True
        # in game buttons for resume, cheats, save and exit after pause
        # menu clicked during game running
        pause_resume = Button(self.root, text="resume",
                              font=("Nimbus Mono PS", 12), bg="black", fg="white",
                              bd=3, relief=RAISED, padx=10,
                              pady=5, width=16, height=2, command=self.resume_game)

        pause_cheats = Button(self.root, text="cheats",
                              font=("Nimbus Mono PS", 12), bg="black", fg="white",
                              bd=3, relief=RAISED, padx=10, pady=5, width=15,
                              height=2, command=self.cheat_code_entry)

        pause_exit = Button(self.root, text="Save and Exit",
                            font=("Nimbus Mono PS", 12), bg="black", fg="white",
                            bd=3, relief=RAISED, padx=10, pady=5,
                            width=15, height=2, command=self.in_game_exit)

        self.btn_pause_resume = pause_resume
        self.btn_pause_cheats = pause_cheats
        self.btn_pause_exit = pause_exit
        # placing buttons for resume, cheats, save and exit
        self.canvas.create_window(self.WIDTH//2, self.HEIGHT//2-100,
                                  anchor=CENTER, window=self.btn_pause_resume)
        self.canvas.create_window(self.WIDTH//2, self.HEIGHT//2,
                                  anchor=CENTER, window=self.btn_pause_cheats)
        self.canvas.create_window(self.WIDTH//2, self.HEIGHT//2+100,
                                  anchor=CENTER, window=self.btn_pause_exit)
        # destroying the pause menu button
        self.btn_MenuToPause.destroy()

    def playing_in_game_menu_button(self) -> None:
        # in game pause menu button creation and placement

        self.menu_to_pause = Button(self.root, text="Menu",
                                    font=("Nimbus Mono PS", 12),
                                    bg="black", fg="white",
                                    bd=3, relief=RAISED, padx=10,
                                    pady=5, width=15, height=2,
                                    command=self.in_game_pause_menu)
        self.btn_MenuToPause = self.menu_to_pause
        self.in_game_menu_id = self.canvas.create_window(
            150, 50, anchor=CENTER, window=self.menu_to_pause)
        self.pause = False

    def in_game_exit(self) -> None:
        # handles saving game state and game state -> main menu
        save_game(self.player_name, self.score, (self.p1.x, self.p1.y), self.p1.vel,
                  [[platform.get_platform_x(), platform.get_platform_height()]
                   for platform in self.all_platforms],
                  [self.background1.x, self.background1.y],
                  [self.background2.x, self.background2.y],
                  [self.background_upper1.x, self.background_upper1.y], [
            self.background_upper2.x, self.background_upper2.y],
            self.platform1.scroll_speed,
            [[self.birds_array[i].image_x,
              self.birds_array[i].image_y,
              self.birds_array[i].scroll_speed,
              self.birds_array[i].tag] for i in range(len(self.birds_array))])

        """save_game(player name, score, player starting position,
                     player starting velocity vertically,
                     positions of platforms,
                     stars image 1 position,
                     stars image 2 position,
                     clouds image 1 position,
                     clouds image 2 position,
                     for all birds : [x position, y position, speed of translation, tag] )
        """
        # resets score, gameloop, game running status variables and the canvas
        self.set_score(0)
        self.clear_canvas()
        self.root.after_cancel(self.game_loop_id)
        self.game_running = False  # Stop the game loop
        self.pause = True
        self.load_Menu()

    def resume_game(self) -> None:
        # deletes all buttons on the screen and resumes gameloop
        self.pause = False
        arr = [self.btn_pause_resume,
               self.btn_pause_cheats, self.btn_pause_exit]
        for i in range(len(arr)):
            arr[i].destroy()
        self.playing_in_game_menu_button()
        self.game_loop()

    def cheat_code_entry(self) -> None:
        """cheat code page
        allows toggling of triple point
        contains back button for cheat code page -> ingame pause menu
        """
        arr = [self.btn_pause_resume,
               self.btn_pause_cheats, self.btn_pause_exit]
        for i in range(len(arr)):
            arr[i].destroy()
        # turns off and on the apprpriate buttons depending on
        # if triple points is activated

        def set_triple_points(choice: bool) -> None:
            if choice:
                text_button_1.config(state="disabled")
                text_button_2.config(state="normal")
                self.cheat_codes_actived["triple_points"] = True
            else:
                text_button_2.config(state="disabled")
                text_button_1.config(state="normal")
                self.cheat_codes_actived["triple_points"] = False
        # function that destroys all buttons on screen then leads back
        # into in game menu pause state

        def go_back() -> None:
            text_button_1.destroy()
            text_button_2.destroy()
            self.canvas.delete(text_button_window_1)
            self.canvas.delete(text_button_window_2)
            self.canvas.delete(back_button_window)
            back_button.destroy()
            self.in_game_pause_menu()
        # activate and deactivate triple point buttons respectively
        text_button_1 = Button(self.root, bg="black", fg="white", font=(
            "Nimbus Mono PS", 12), text="Activate triple points",
            command=lambda: set_triple_points(True))
        text_button_window_1 = self.canvas.create_window(
            self.WIDTH//2-150, self.HEIGHT//2-100, anchor=CENTER, window=text_button_1)

        text_button_2 = Button(self.root, bg="black", fg="white", font=(
            "Nimbus Mono PS", 12), text="Deactivate triple points",
            command=lambda: set_triple_points(False))
        text_button_window_2 = self.canvas.create_window(
            self.WIDTH//2+150, self.HEIGHT//2-100, anchor=CENTER, window=text_button_2)

        set_triple_points(self.cheat_codes_actived["triple_points"])

        # placing back button
        back_button = Button(self.root, bg="black", fg="white", font=(
            "Nimbus Mono PS", 12), text="Back", command=go_back)
        back_button_window = self.canvas.create_window(
            self.WIDTH//2, self.HEIGHT//2+100, anchor=CENTER, window=back_button)

    #########################
    # key event management
    #########################
    def key_press(self, event) -> None:

        try:  # checks for jump press
            if event.keysym == self.binded_jump:
                self.p1.jump()
        except:
            pass
        # checks for player boss key press
        if event.keysym == "b" and self.root.focus_get() != self.entry:
            Bk.boss_key_create()
        # checks for triple point cheat code activation/deactivation
        if event.keysym == "t" and self.root.focus_get() != self.entry:
            self.cheat_codes_actived["triple_points"] = not self.cheat_codes_actived["triple_points"]
        # checks for super jump cheat code activation
        if event.keysym == "o" and self.root.focus_get() != self.entry:
            self.super_jump_keys["o"] = True
            self.cheat_codes_actived["super_jump"] = self.super_jump_keys["o"] and self.super_jump_keys["p"]
            if self.cheat_codes_actived["super_jump"]:
                try:
                    self.p1.jump_force = self.SUPER_JUMP
                except:
                    pass
        # checks for super jump cheat code activation
        if event.keysym == "p" and self.root.focus_get() != self.entry:
            self.super_jump_keys["p"] = True
            self.cheat_codes_actived["super_jump"] = self.super_jump_keys["o"] and self.super_jump_keys["p"]
            if self.cheat_codes_actived["super_jump"]:
                try:  # only works if player has been created
                    self.p1.jump_force = self.SUPER_JUMP
                except:
                    pass

    def key_release(self, event) -> None:
        try:  # checks for jump button let go to stop jumping
            if event.keysym == self.binded_jump:
                self.p1.stop_jump()
        except:
            pass
        # checks for super jump deactivation
        if event.keysym == "o" and self.root.focus_get() != self.entry:
            self.super_jump_keys["o"] = False
            self.cheat_codes_actived["super_jump"] = False
            try:
                self.p1.jump_force = self.NORMAL_JUMP
            except:
                pass
        # checks for super jump deactivation
        if event.keysym == "p" and self.root.focus_get() != self.entry:
            self.super_jump_keys["p"] = False
            self.cheat_codes_actived["super_jump"] = False
            try:
                self.p1.jump_force = self.NORMAL_JUMP
            except:
                pass

    ##########################
    # game cycle management
    ##########################

    def game_loop(self) -> None:

        if self.game_running and not self.pause:  # checking if game is unpaused
            self.set_score(  # updating score label to display correct score
                self.score+(3 if self.cheat_codes_actived["triple_points"] else 1))
            # if again is set to True then player has not collided with platform after update
            # thus backgrounds, crows, platforms are updated
            again = self.p1.update_player(
                self.all_platforms, self.restart_game)
            if again:
                # backgrounds translated
                self.background1.update_background()
                self.background2.update_background()
                self.background_upper2.update_background()
                self.background_upper1.update_background()
                # max height player is expected to jump between platforms
                max_jump_height = self.p1.max_jump_height()
                # checks for bird and player collision
                for b in self.birds_array:
                    again2 = b.update_crow(
                        [self.p1.x, self.p1.y, self.p1.x+self.p1.size, self.p1.y+self.p1.size], self.restart_game)
                    if not again2:
                        break
                # platform updated and floor for player set
                last_platform = self.platform1
                for p in self.all_platforms:
                    if p.get_platform_x() > last_platform.get_platform_x():
                        last_platform = p
                for platform in self.all_platforms:
                    platform.update_platform(height_of_last_platform=last_platform.get_platform_height(
                    ), x_of_last_platform=last_platform.get_platform_x(), max_player_height=max_jump_height)
                    platform.change_scroll_speed(
                        self.STARTING_SCROLL_SPEED, self.score)
            # if player has not collided with a platform or bird game continues
            # else game restarts (restart function passed into player)
            if again and again2:
                self.game_loop_id = self.root.after(20, self.game_loop)

    def restart_game(self) -> None:
        # count down display routine
        def count_down_display(n: int) -> None:
            self.count = PhotoImage(file="gameassets/count"+str(n)+".png")
            countdown_label_id = self.canvas.create_image(self.WIDTH//2,
                                                          self.HEIGHT//2, anchor=CENTER, image=self.count)
            self.root.after(
                800, lambda: delete_countdown_label(countdown_label_id))

        def delete_countdown_label(id: int) -> None:
            self.canvas.delete(id)
        # checking if a game has actually been played before attempting game restart
        if self.game_loop_id:
            # updating leaderboard neccessarily at end of game
            self.game_running = True
            update_Leaderboard(self.player_name, self.score)
            # resetting platforms whilst giving them random start heights
            self.p1.reset_position()
            self.platform1.reset_pos(0, 500)
            if randint(1, 2) == 1:
                self.platform2.reset_pos(
                    1000, max(self.platform1.get_platform_height()-int(self.platform_offset()), 400))
            else:
                self.platform2.reset_pos(
                    1000, min(700, self.platform1.get_platform_height()+int(self.platform_offset())))
            if randint(1, 2) == 1:
                self.platform3.reset_pos(
                    2000, max(400, self. platform2.get_platform_height()-int(self.platform_offset())))
            else:
                self.platform3.reset_pos(
                    2000, min(700, self.platform2.get_platform_height()+int(self.platform_offset())))

            self.set_score(0)  # score zeroed
            # birds all start off-screen
            for bird in range(len(self.birds_array)):
                self.birds_array[bird].reset_pos(bird, self.start_bird_pos)
            # deleting paus button in preperation of countdown
            self.canvas.delete(self.in_game_menu_id)
            count_down_display(3)  # countdown initiated

            self.root.after(1000, lambda: count_down_display(2))
            self.root.after(2000, lambda: count_down_display(1))

            self.root.after(3000, lambda: (  # after count down menu pause button reloaded
                self.game_loop(), self.playing_in_game_menu_button()))


Game = GameStateManager()
