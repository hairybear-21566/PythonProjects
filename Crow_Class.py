
from tkinter import Canvas, PhotoImage,NW 
from random import randint

class Crow:

    def __init__(self,x:int,y:int,scrollSpeed:int,filepath:str,tag_id:str,canvas:Canvas)->None:
        #             100,100,10,f"GameTests/crow-size-32/crow-size-32-{str(1)}.png", 400, "bird 1", canvas

        self.image_x = x
        self.image_y = y
        self.hitbox = [self.image_x+10,self.image_y+10,self.image_x+54,self.image_y+54] # 64 x 64 is the dimensions of the image but the hitbox is 44 x 44
        self.scroll_speed =scrollSpeed
        self.frame = 1
        
        self.filepath = f"GameTests/crow-size-32/crow-size-32-{str(1)}.png"

        self.size = 64
        
        self.canvas = canvas
        self.tag =tag_id

        self.image = PhotoImage(file = filepath,).subsample(8,8)
        
        self.image_object = canvas.create_image(x,y,anchor = NW, image = self.image,tags=tag_id)
        self.canvas.tag_raise(self)
        
        self.rect = canvas.create_rectangle(x+10,y+10,x + 54,y + 54, outline = "red" )

        self.frame = 1
        self.count = 0 

    def update_crow(self,player,restart_game)->bool:
        
        self.frame_update()
        self.move()
        self.animate()
        if self.collision(player,self.hitbox):
            restart_game()
            return False
        return True
        

    def animate(self)->None:
        
        self.filepath = f"GameTests/crow-size-32/crow-size-32-{str(self.frame)}.png"
        self.image.config(file=self.filepath)
        self.image = self.image.subsample(8,8)
        self.canvas.itemconfig(self.image_object, image=self.image)
        

    def move(self)->None:
        # check if crow off screen, if so then push crow to the end otherwise shift to side
        if self.image_x + self.size - self.scroll_speed <= 0:
            self.floor = self.get_min_height()-randint(25,100)-64
            self.image_y = self.floor
            self.image_x = 1366-(self.scroll_speed-(self.size+self.image_x)) 

        else:
            #self.floor = self.get_min_height(platforms)+randint(25,100)+64
            #self.image_y = self.floor
            self.image_x -= self.scroll_speed 
        self.canvas.coords(self.image_object,self.image_x,self.image_y)
        self.hitbox = [self.image_x+10,self.image_y+10,self.image_x+54,self.image_y+54]
        self.canvas.coords(self.rect,self.hitbox[0],self.hitbox[1],self.hitbox[2],self.hitbox[3])

    def get_min_height(self)->int:
        # loops through all the platforms and finds the greatest height of each platform
        return randint(450,650)
    
    def collision(self,arr1:list[int],arr2:list[int])->bool:
        # arr[1], arr[2] : [x,y,x+w,y+h]
        if arr1[0] < arr2[2] and arr1[2] > arr2[0] and arr1[1] < arr2[3] and arr1[3] > arr2[1]: 
            return True
        return False
    
    def reset_pos(self,i:int,start_bird_pos:int)->None:
        self.image_x = start_bird_pos+i*1000
        self.image_y = randint(450,650)
        self.canvas.coords(self.image_object,self.image_x,self.image_y)
        self.hitbox = [self.image_x+10,self.image_y+10,self.image_x+54,self.image_y+54]
        self.canvas.coords(self.rect,self.hitbox[0],self.hitbox[1],self.hitbox[2],self.hitbox[3])

    def frame_update(self)->None:
        self.count = self.count + 1 if self.count!=5 else 1
        if self.count == 5:
            self.frame = self.frame + 1 if self.frame!=6 else 1