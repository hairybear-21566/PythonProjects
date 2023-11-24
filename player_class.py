from tkinter import Canvas, NW, PhotoImage
from random import randint


class Player:

    def __init__(self, x: int, y: int, size: int, game_canvas: Canvas):
        """PROCEDURE, instatiating player square properties
        Args:
            x (int): player position on x axis
            y (int): player position on y axis
            size (int): player square dimesions
            game_canvas (tkinter.Canvas): canvas everything for the game is drawn on including the player
        """
        self.initial_x = x
        self.initial_y = y
        self.size = size
        self.x = x
        self.y = y
        self.canvas = game_canvas
        # player id on canvas
        # self.playerInt = self.canvas.create_rectangle(x,y,size+x,y+size,outline="green")
        # values related to movement
        self.vel = 0
        self.conseq_jump_frames = 0
        self.max_conseq_jump_frames = 5
        self.gravity = 1.5
        self.jump_force = -22
        self.on_ground = True
        self.holding_jump = False
        self.jump_available = False
        self.floor = self.y
        # animations
        self.run_frame = 0  # frames range from 0 to 7
        self.jump_frame = 2  # frames range from 0 to 2
        self.land_frame = 0  # frames range from 0 to 8
        self.image = PhotoImage(
            f"gameassets/player-jumping/tile00{self.jump_frame}.png")
        self.diff = int((48 - self.size)//2)
        # self.image_object = self.canvas.create_image(x,y,anchor = NW, image = self.image,tags="player")
        self.image_object = self.canvas.create_image(
            self.x-self.diff, self.y-self.diff, anchor=NW, image=self.image, tags="player")
        self.canvas.tag_raise("player")
        self.landing = True
        self.still_animating_jump = True
        self.run_count = 0

    def update_player(self, platforms: list, game_restart):
        """moves players and updates animations OR restarts game
        restart game is triggered if player collides with platform

        Args:
            platforms (list): array of the 3 platforms that wrap around the screen to
            give the illusion of infinite platforms
            game_restart (function): restarts game by reseting the screen on player death
        """
        self.set_new_floor(platforms)
        self.set_on_ground()
# checking if gravity should kick in yet
        # if player not on ground
        if not self.on_ground:
            # if they are holdidig jump for less than 5 frames
            if self.conseq_jump_frames < self.max_conseq_jump_frames and self.holding_jump:
                # continue velocity, but then increment frame count by 1
                self.conseq_jump_frames += 1
                self.vel = self.jump_force  # just to make sure velocity is corect
            else:
                # add gravity to velocity to begin the fall
                self.vel += self.gravity
                # set jumpframes held to the max to begin the fall
                self.conseq_jump_frames = self.max_conseq_jump_frames
# if the player + vel still has them above their floor
        if self.y + self.vel + self.size < self.floor:
            # move player to new y = old y + vel
            self.move_player(0, self.vel)
# if player + velocity has them below the floor but player is above the floor
        elif self.y+self.vel+self.size >= self.floor and self.y+self.size < self.floor:
            # player attaches to ground
            self.move_player(0, self.floor - self.size - self.y)
            # velocity set to zero
            self.vel = 0
            # reset conseqative jump frames
            self.conseq_jump_frames = 0
        # if player on the floor just reset consequetive jump frames
        elif self.y + self.size == self.floor:
            self.conseq_jump_frames = 0
        elif self.y+self.size > 700:
            self.reset_frames()
            game_restart()
            return False
        # if player below the floor
        else:
            self.reset_frames()
            game_restart()
            return False
        self.animate()
        return True

    def animate(self):
        pass
        # if not on the ground use jump animations
        # if jump_frame != 2 then (jump_frame = jump_frame + 1 AND landing = True 
        # AND self.run_frame = 0 AND self.land_frame = 0)
        # else if player on ground
        # if player landing and land_frame<9 THEN load land_frame THEN land_frame+=1
        # else player landing = False THEN load player running 
        # THEN run_frame += 1 if run_frame<7 else run_frame = 0

        # if not on the ground use jump animations
        if not self.on_ground:
            # if jump_frame != 2 then (jump_frame = jump_frame + 1 AND landing = True 
            # AND self.run_frame = 0 AND self.land_frame = 0)
            if self.jump_frame < 2:

                self.image.config(
                    file=f"gameassets/player-jumping/tile00{self.jump_frame}.png")
                self.canvas.itemconfig(self.image_object, image=self.image)
                self.jump_frame += 1
                self.run_frame = 0
                self.land_frame = 0
                self.landing = True
                self.run_count = 0
            elif self.still_animating_jump:
                self.still_animating_jump = False
                self.image.config(file="gameassets/player-jumping/tile002.png")
                self.canvas.itemconfig(self.image_object, image=self.image)

        # else if player on ground
        else:
            # if player landing and land_frame<9 THEN load land_frame 
            # THEN land_frame+=1 AND jump_frame = 0
            if self.landing and self.land_frame < 9:
                self.image.config(
                    file=f"gameassets/player-landing/tile00{self.land_frame}.png")
                self.canvas.itemconfig(self.image_object, image=self.image)
                self.land_frame += 1
                self.jump_frame = 0

            # else player landing = False THEN load player running THEN if run_count==4 
            # THEN(run_frame += 1 if run_frame<7 else run_frame = 0)
                # else run_count+=1
            else:
                self.landing = False
                self.image.config(
                    file=f"gameassets/player-running/tile00{self.run_frame}.png")
                self.canvas.itemconfig(self.image_object, image=self.image)
                if self.run_count == 4:
                    self.run_frame = self.run_frame+1 if self.run_frame < 7 else 0
                    self.run_count = 0
                else:
                    self.run_count += 1

    def reset_frames(self):
        self.run_frame = 0  # frames range from 0 to 7
        self.jump_frame = 2  # frames range from 0 to 2
        self.land_frame = 0  # frames range from 0 to 8
        self.image = PhotoImage(file="gameassets/player-jumping/tile002.png")
        self.diff = int((48 - self.size) // 2)
        self.canvas.itemconfig(self.image_object, image=self.image)
        self.landing = True
        self.still_animating_jump = True
        self.run_count = 0

    def move_player(self, dx: int, dy: int):
        # self.canvas.move(self.playerInt,dx,dy)
        self.y += dy
        self.x += dx
        # def move_image(self,dx:int,dy:int):
        self.canvas.move(self.image_object, dx, dy)

    def set_new_floor(self, platforms: list):
        # discovering which platform is directly under player 
        # if any then setting the players floor
        # to the height of the platform
        # else floor is set to a large number allowing player 
        # to fall to their death
        value = False
        for p in platforms:
            if p.get_platform_x() <= self.x+self.size and p.get_platform_x()+p.width >= self.x+self.size:
                self.floor = p.get_platform_height()
                value = True
                break
        if value == False:
            self.floor = 800

    def set_on_ground(self):
        if self.y+self.size == self.floor:
            self.on_ground = True
        else:
            self.on_ground = False

    def set_available_jump(self):
        if self.y+self.size == self.floor:
            self.jump_available = True
        else:
            self.jump_available = False

    def jump(self, event=None):
        """PROCEDURE, initiate jump

        Args:
            event (any, optional): may be used for jump nuance. Defaults to None.
        """
        if self.on_ground:
            self.vel = self.jump_force
            self.on_ground = False
            self.holding_jump = True

    def stop_jump(self):
        """PROCEDURE, stops jump
        """
        self.holding_jump = False

    def max_jump_height(self) -> int:
        """returns the max height of a jump

        Returns:
            int:max height of jump in pixels roughly, used for platform generation
        """
        return 150

    def reset_position(self):

        # reset player position to default point and thier 
        # animation to falling animation
        self.x = 200
        self.y = 400
        self.vel = 0
        self.reset_image()
        self.reset_frames()

    def reset_image(self):
        self.canvas.coords(self.image_object, self.x -
                           self.diff, self.y-self.diff)
