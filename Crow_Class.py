
from tkinter import Canvas, PhotoImage,NW 
from random import randint

class Crow:

    def __init__(self,x:int,y:int,scrollSpeed:int,filepath:str,tag_id:str,canvas:Canvas)->None:

        self.image_x = x
        self.image_y = y
        self.hitbox = [self.image_x+10,self.image_y+10,self.image_x+54,self.image_y+54] # 64 x 64 is the dimensions of the image but the hitbox is 44 x 44
        self.scroll_speed =scrollSpeed
        self.frame = 1
        self.filepath = filepath
        self.size = 64
        self.canvas = canvas
        self.tag =tag_id
        self.image = PhotoImage(file = filepath)
        self.image_object = canvas.create_image(x,y,anchor = NW, image = self.image,tags=tag_id)
        self.canvas.tag_raise(self.tag)
        self.frame = 1
        self.count = 0 

    def update_crow(self,player,restart_game)->bool:
        
        
        self.move()
        self.animate(self.frame_update())
        if self.collision(player,self.hitbox):
            restart_game()
            return False
        return True
        

    def animate(self,f_path:str)->None:
        self.filepath = f_path
        self.image.config(file=f_path)
        # self.image = self.image.subsample(8,8)
        self.canvas.itemconfig(self.image_object, image=self.image)
        

    def move(self)->None:
        # check if crow off screen, if so then push crow to the end otherwise shift to side
        if self.image_x + self.size - self.scroll_speed <= 0:   
            self.image_y = self.get_min_height()-randint(25,100)-64
            self.image_x = 1366-(self.scroll_speed-(self.size+self.image_x))
            self.scroll_speed=randint(4,10) 
        else:
            self.image_x -= self.scroll_speed 
        self.canvas.coords(self.image_object,self.image_x,self.image_y)
        self.hitbox = [self.image_x+10,self.image_y+10,self.image_x+54,self.image_y+54]
        

    def get_min_height(self)->int:
        return randint(400,625)
    
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
        #self.canvas.coords(self.rect,self.hitbox[0],self.hitbox[1],self.hitbox[2],self.hitbox[3])

    def frame_update(self)->int:
        self.count = self.count + 1 if self.count!=5 else 1
        if self.count == 5:
            self.frame = self.frame + 1 if self.frame!=6 else 1
        return f"gameassets/crows-64/crow-size-64-{str(self.frame)}.png"