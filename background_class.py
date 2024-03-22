from tkinter import PhotoImage, NW, Canvas


class GameBackground:
    def __init__(self, x: int, y: int, file_path: str, tag: str, canvas: Canvas, scroll_speed: int) -> None:
        """initilizing parameters and create image to put on to main game canvas

        Args:
            x (int): top left x position of image
            y (int): top left corner y position of image
            file_path (str): relative file path of image
            tag (str): image tag
            canvas (tkinter.Canvas): main game canvas
            scroll_speed (int): speed of horizontal canvas translation
        """
        # corrdinates of image
        self.initial_x = x
        self.initial_y = y
        self.x = x
        self.y = y
        # file path for background image
        self.file_path = file_path
        self.tag = tag
        # creating image object
        self.image = PhotoImage(file=file_path)
        self.image_object = canvas.create_image(
            x, y, anchor=NW, image=self.image, tags=tag)  # put image object onto a window on the canvas
        self.canvas = canvas
        # push image to bottom layer
        self.canvas.tag_lower(tag)
        # rate of image horizontal translation
        self.scroll_speed = scroll_speed
        self.width = self.image.width()

    def update_background(self) -> None:
        if self.x - self.scroll_speed <= -1366:  # if by translation the image is fully off-screen
            self.x = 1366-(self.scroll_speed-(1366+self.x))
            # loop image around to other side of screen
            self.canvas.coords(self.image_object, self.x, 0)
        else:
            # otherwise just translate image horizontally
            self.canvas.move(self.image_object, -self.scroll_speed, 0)
            self.x -= self.scroll_speed
