from tkinter import CENTER, Tk, Canvas, Button, RAISED, PhotoImage, NW, Entry, CENTER, Label

#from testing2 import Crow
from random import randint
from testing2 import Player



class Platform:

    def __init__(self,x,y,width):
        self.x = x
        self.y = y
        self.width = width
    
    def getPlatformX(self):
        return self.x
    
    def getPlatformHeight(self):
        return self.y
    
class Thing:
    def __init__(self,canvas: Canvas):
        self.x = 500
        self.y = 100
        self.canvas = canvas
        self.obj=canvas.create_rectangle(self.x,self.y,self.x+15,self.y+15, fill = "blue")

    def move(self,movement):
        if movement[0]==True:
            self.y-=5
        if movement[1]==True:
            self.x-=5
        if movement[2]==True:
            self.y+=5
        if movement[3]==True:
            self.x+=5

        self.update_player()
    def update_player(self):
        self.canvas.coords(self.obj,self.x,self.y,self.x+15,self.y+15)
    




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


ting = Thing(canvas)
p1 = Player(500,400,25,canvas)
bindedJump = "Up"
platforms = [Platform(0,500,1366)]

frame = 1
count = 0 
#             w      a      s      d
movement = [False, False, False, False]

def gameloop():
    global count, frame

    count = count + 1 if count!=5 else 1
    if count == 5:
        frame = frame + 1 if frame!=6 else 1
    ting.move(movement)
    p1.updatePlayer(platforms,lambda:print("restart"))
    
    
    
    if True:
        #pass
        root.after(20,gameloop)
    else:
        root.destroy()
    


    

def key_press(event)->None:
        
    try:
        if event.keysym == bindedJump:
            p1.jump()

    except:
        pass
       

def key_release(event)->None:
    try:
        if event.keysym == bindedJump:
            p1.stopJump()
    except:
        pass


        

   

# Function to clear the flag when the up key is released


    

# Bind the key press and release events
root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

gameloop()
root.mainloop()