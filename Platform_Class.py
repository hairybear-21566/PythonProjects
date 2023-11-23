from random import randint
from tkinter import Canvas
# restartGame IN updatPlayer
# allPlatforms IN updatePlayer->setNewFloor


class Platforms:
    width = 850  # Added class attribute for width thus the gap betweeen the platforms is 1000px - width in px)
    screen_height = 1366

    def __init__(self, x: int, y: int, scrollSpeed: int, GameCanvas: Canvas):
        self.initialX = x
        self.initialY = y
        self.x = x
        self.y = y
        self.initial_scroll_speed = scrollSpeed
        self.scrollSpeed = scrollSpeed
        # Create the platform with the class attribute width
        self.platformInt = GameCanvas.create_rectangle(
            x, y, x + Platforms.width, Platforms.screen_height, fill="black")
        self.GameCanvas = GameCanvas

    def updatePlatform(self, heightOfLastPlatform: int = 0, xOfLastPlatform: int = 0, maxPlayerJumpHeight: int = 0):
        if self.x+self.width < 0:
            self.newPlatform(heightOfLastPlatform, xOfLastPlatform)
        else:
            self.scrollPlatform()

    def changeScrollSpeed(self, start: int, score: int):
        self.scrollSpeed = min(score//200 + start, 15)

    def scrollPlatform(self):
        self.GameCanvas.move(self.platformInt, -self.scrollSpeed, 0)
        self.x -= self.scrollSpeed

    def newPlatform(self, prevHeight: int, xOfLastPlatform: int):
        self.x = xOfLastPlatform + 1000  # Use class attribute width
        if randint(1, 2) == 1:
            self.y = min(prevHeight + randint(0, int(150//1.7)), 700)
        else:
            self.y = max(prevHeight - randint(0, int(150//1.7)), 400)
        # Update the platform coordinates using class attribute width
        self.GameCanvas.coords(self.platformInt, self.x, self.y,
                               self.x + Platforms.width, Platforms.screen_height)

    def getPlatformHeight(self) -> int:
        return self.y

    def getPlatformX(self) -> int:
        return self.x

    def resetScrollSpeed(self):
        self.scrollSpeed = self.initial_scroll_speed

    def resetPos(self, x: int, y: int):
        self.GameCanvas.coords(self.platformInt, x, y, x+self.width, 768)
        self.x = x
        self.y = y
        self.resetScrollSpeed()
