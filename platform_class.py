from random import randint
from tkinter import Canvas

# restartGame IN updatPlayer
# allPlatforms IN updatePlayer->setNewFloor

class Platforms:
    width = 850  # Added class attribute for width thus the gap betweeen the platforms is 1000px - width in px)
    screen_height = 1366

    def __init__(self, x: int, y: int, scroll_speed: int, game_canvas: Canvas)->None:
        """initializing the platform position and create & drawing the platform
        using tkinter.Canvas.create_rectangle

        Args:
            x (int): top left position of platform
            y (int): top left vertical position of platform
            scroll_speed (int): platform starting west translation speed
            game_canvas (Canvas): the main game canvas that all polygons and images are drawn onto
        """
        self.initial_x = x
        self.initial_y = y
        self.x = x
        self.y = y
        self.initial_scroll_speed = scroll_speed
        self.scroll_speed = scroll_speed
        # Create the platform with the class attribute width
        self.platform_id = game_canvas.create_rectangle(
            x, y, x + Platforms.width, Platforms.screen_height, fill="black")
        self.game_canvas = game_canvas
        
        

    def update_platform(self, height_of_last_platform: int = 0, x_of_last_platform: int = 0, max_player_height: int = 0)->None:
        """choosing how to translate platform position

        Args:
            height_of_last_platorm (int, optional): height of platform furthest to the right. Defaults to 0.
            x_of_last_platform (int, optional): the x coordinate of the last platform . Defaults to 0.
            max_player_height (int, optional): the max height a player is expected to jump. Defaults to 0.
        """
        if self.x+self.width < 0:
            self.new_platform(height_of_last_platform, x_of_last_platform)
        else:
            self.scroll_platform()

    def change_scroll_speed(self, start: int, score: int)->None:
        """change horizontal translation rate of platform

        Args:
            start (int): _description_
            score (int): _description_
        """
        self.scroll_speed = min(score//200 + start, 13)

    def scroll_platform(self)->None:
        self.game_canvas.move(self.platform_id, -self.scroll_speed, 0)
        self.x -= self.scroll_speed
        

    def new_platform(self, previous_height: int, x_of_last_platform: int)->None:
        self.x = x_of_last_platform + 1000  # Use class attribute width
        if randint(1, 2) == 1:
            self.y = min(previous_height + randint(0, int(150//1.7)), 700)
        else:
            self.y = max(previous_height - randint(0, int(150//1.7)), 400)
        # Update the platform coordinates using class attribute width
        self.game_canvas.coords(self.platform_id, self.x, self.y,
                               self.x + Platforms.width, Platforms.screen_height)
        

    def get_platform_height(self) -> int:
        return self.y

    def get_platform_x(self) -> int:
        return self.x

    def reset_scroll_speed(self)->None:
        self.scroll_speed = self.initial_scroll_speed

    def reset_pos(self, x: int, y: int)->None:
        self.game_canvas.coords(self.platform_id, x, y, x+self.width, 768)
        self.x = x
        self.y = y
        self.reset_scroll_speed()
     
