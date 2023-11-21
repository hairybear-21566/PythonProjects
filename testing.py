from tkinter import CENTER, Tk, Canvas, Button, RAISED, PhotoImage, NW, Entry, CENTER, Label

#from testing2 import Crow
from random import randint

# testing looping
class Crow:

    def __init__(self,x:int,y:int,scrollSpeed:int,filepath:str,floor:int,tag_id:str,canvas:Canvas):
        #             100,100,10,f"GameTests/crow-size-32/crow-size-32-{str(1)}.png", 400, "bird 1", canvas

        self.image_x = x
        self.image_y = y
        self.hitbox = [self.image_x+10,self.image_y+10,self.image_x+54,self.image_y+54] # 64 x 64 is the dimensions of the image but the hitbox is 44 x 44
        self.scroll_speed =scrollSpeed
        self.frame = 1
        self.floor = floor
        self.filepath = f"GameTests/crow-size-32/crow-size-32-{str(1)}.png"

        self.size = 64
        
        self.canvas = canvas
        self.tag =tag_id

        self.image = PhotoImage(file = filepath,).subsample(8,8)
        
        self.image_object = canvas.create_image(x,y,anchor = NW, image = self.image,tags=tag_id)
        self.canvas.tag_raise(self)
        
        self.rect = canvas.create_rectangle(x+10,y+10,x + 54,y + 54, outline = "red" )

    def update_crow(self,platforms,frame):
         # move
        self.move(platforms)
        # then check for collision
        # self.collision(self.hitbox,arr)
        # if no collision animate else restart game
        self.animate(frame)
        pass
        

    def animate(self,frame):
        if self.frame != frame:
            self.filepath = f"GameTests/crow-size-32/crow-size-32-{str(frame)}.png"
            #self.image = PhotoImage(file=self.filepath).subsample(4, 4)
            self.image.config(file=self.filepath)
            self.image = self.image.subsample(8,8)
            self.canvas.itemconfig(self.image_object, image=self.image)
            self.frame = frame  # Update the frame attribute

    def move(self, platforms):
        # check if crow off screen, if so then push crow to the end otherwise shift to side
        if self.image_x + self.size - self.scroll_speed <= 0:
            self.floor = self.get_min_height(platforms)+randint(25,100)+64
            self.image_y = self.floor
            self.image_x = 1366-(self.scroll_speed-(self.size+self.image_x)) 

        else:
            #self.floor = self.get_min_height(platforms)+randint(25,100)+64
            #self.image_y = self.floor
            self.image_x -= self.scroll_speed 
        self.canvas.coords(self.image_object,self.image_x,self.image_y)
        self.hitbox = [self.image_x+10,self.image_y+10,self.image_x+54,self.image_y+54]
        self.canvas.coords(self.rect,self.hitbox[0],self.hitbox[1],self.hitbox[2],self.hitbox[3])

    def get_min_height(self,platforms):
        # loops through all the platforms and finds the greatest height of each platform
        return 500
    
    def collision(self,arr1,arr2):
        # arr[1], arr[2] : [x,y,x+w,y+h]
        if arr1[0] < arr2[2] and arr1[2] > arr2[0] and arr1[1] < arr2[3] and arr1[3] > arr2[1]: 
            return True
        return False


    
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

bird = Crow(100,100,5,f"GameTests/crow-size-32/crow-size-32-{str(1)}.png", 400, "bird 1", canvas)
ting = Thing(canvas)

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
    bird.update_crow(500,frame)
    
    
    if not bird.collision([ting.x,ting.y,ting.x+15,ting.y+15],bird.hitbox):
        #pass
        root.after(5,gameloop)
    else:
        root.destroy()
    

def key_press(event):
    
    if event.keysym == "w":
        movement[0]=True
    if event.keysym == "a":
        movement[1]=True
    if event.keysym == "s":
        movement[2]=True
    if event.keysym == "d":
        movement[3]=True
    


        

   

# Function to clear the flag when the up key is released


def key_release(event):
    if event.keysym == "w":
        movement[0]=False
    if event.keysym == "a":
        movement[1]=False
    if event.keysym == "s":
        movement[2]=False
    if event.keysym == "d":
        movement[3]=False
    
    

# Bind the key press and release events
root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

gameloop()
root.mainloop()