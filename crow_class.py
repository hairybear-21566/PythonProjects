
from tkinter import Canvas, PhotoImage, NW
from random import randint


class Crow:

    def __init__(self, x: int, y: int, scroll_speed: int, file_path: str, tag_id: str, canvas: Canvas) -> None:
        """initiliazing crow instance

        Args:
            x (int): top left corner x position for crow
            y (int): top left corner y position for crow
            scroll_speed (int): translation speed of crow
            file_path (str): relative file path for crow sprite image
            tag_id (str): tag for image
            canvas (Canvas): canvas to play game on
        """

        self.image_x = x
        self.image_y = y
        # 64 x 64 is the dimensions of the image but the hitbox is 44 x 44
        self.hitbox = [self.image_x+10, self.image_y +
                       10, self.image_x+54, self.image_y+54]
        self.scroll_speed = scroll_speed
        self.frame = 1
        self.file_path = file_path
        self.size = 64
        self.canvas = canvas
        self.tag = tag_id
        self.image = PhotoImage(file=file_path)
        self.image_object = canvas.create_image(
            x, y, anchor=NW, image=self.image, tags=tag_id)
        self.canvas.tag_raise(self.tag)
        self.frame = 1
        self.count = 0

    def update_crow(self, player, restart_game) -> bool:
        # crow translated
        self.move()
        # animated
        self.animate(self.frame_update())
        # checks for collision with player
        if self.collision(player, self.hitbox):
            restart_game()
            return False
        return True

    def animate(self, f_path: str) -> None:
        self.file_path = f_path
        self.image.config(file=f_path)
        self.canvas.itemconfig(self.image_object, image=self.image)

    def move(self) -> None:
        # check if crow off screen, if so then push crow to the end otherwise shift to side
        if self.image_x + self.size - self.scroll_speed <= 0:
            self.image_y = self.get_min_height()-randint(25, 100)-64
            self.image_x = 1366-(self.scroll_speed-(self.size+self.image_x))
            self.scroll_speed = randint(4, 10)
        else:
            self.image_x -= self.scroll_speed
        self.canvas.coords(self.image_object, self.image_x, self.image_y)
        self.hitbox = [self.image_x+10, self.image_y +
                       10, self.image_x+54, self.image_y+54]

    def get_min_height(self) -> int:
        return randint(400, 625)

    def collision(self, arr1: list, arr2: list) -> bool:
        """AABB collision detection betweeen player and crow

        Args:
            arr1 (list[int]): player hit box
            arr2 (list[int]): crow hit box

        Returns:
            bool: True if collison detect else False
        """
        # arr[1], arr[2] : [x,y,x+w,y+h]
        if arr1[0] < arr2[2] and arr1[2] > arr2[0] and arr1[1] < arr2[3] and arr1[3] > arr2[1]:
            return True
        return False

    def reset_pos(self, i: int, start_bird_pos: int) -> None:
        """resets the positon of the birds to appropriate starting postions

        Args:
            i (int): number related to sequence bird is introduced to player run
            start_bird_pos (int): the default starting position of a bird
        """
        self.image_x = start_bird_pos+i*1000
        self.image_y = randint(450, 650)
        self.canvas.coords(self.image_object, self.image_x, self.image_y)
        self.hitbox = [self.image_x+10, self.image_y +
                       10, self.image_x+54, self.image_y+54]
        # self.canvas.coords(self.rect,self.hitbox[0],self.hitbox[1],self.hitbox[2],self.hitbox[3])

    def frame_update(self) -> str:
        """function that ensures 5 frames have passed before next crow sprite loaded
        then returns the appropriate bird sprite

        Returns:
            str: relative path of imange png of crow sprite
        """
        self.count = self.count + 1 if self.count != 5 else 1
        if self.count == 5:
            self.frame = self.frame + 1 if self.frame != 6 else 1
        return f"gameassets/crows/crow-size-64-{str(self.frame)}.png"
