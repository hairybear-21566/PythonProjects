from tkinter import Canvas, Tk, Label, messagebox
import random

def set_window_dimensions(w, h):
    root = Tk()
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - w) // 2
    y = (screen_height - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")
    
    return root

def exit_fullscreen(event):
    window.attributes('-fullscreen', False)

def leftKey(event):
    global direction
    if direction!="right":
        direction="left"

def upKey(event):
    global direction
    if direction!="down":
        direction="up"

def downKey(event):
    global direction
    if direction!="up":
        direction="down"

def rightKey(event):
    global direction
    if direction!="left":
        direction="right"

def create_text() -> str:
    return f"Score: {score}"

def placeFood():
    global food,food_x,food_y
    food_x = random.randint(0,width-snake_size)
    food_y = random.randint(0,height-snake_size)
    food = GameCanvas.create_rectangle(food_x,food_y,food_x+snake_size,food_y+snake_size,fill="steel blue")

def move_food():
    global food,food_x,food_y
    GameCanvas.move(food,food_x*-1,food_y*-1)
    GameCanvas.delete(food)
    placeFood()

def move_snake_body():
    global snake
    for part in range(len(snake)-1,0, -1):
        X1,Y1,X2,Y2 = GameCanvas.coords(snake[part-1])
        GameCanvas.coords(snake[part],X1,Y1,X2,Y2)

def grow_snake(px1,py1,px2,py2):
    global snake,step_size,direction,snake_size
    diff = snake_size-step_size
    if direction=="left":
        snake.append(GameCanvas.create_rectangle(px1+diff,py1,px2+diff,py2,fill="green"))
    elif direction=="right":
        snake.append(GameCanvas.create_rectangle(px1-diff,py1,px2-diff,py2,fill="green"))
    elif direction=="up":
        snake.append(GameCanvas.create_rectangle(px1,py1+diff,px2,py2+diff,fill="green"))
    else:
        snake.append(GameCanvas.create_rectangle(px1,py1-diff,px2,py2-diff,fill="green"))

def overlapping(a:int,b:int):
    if a[0]<b[2] and a[2]>b[0] and a[1]<b[3] and a[3]>b[1]:
        return True
    return False

def crumple():
    for a in range(1,len(snake)):
        if overlapping(GameCanvas.coords(head),GameCanvas.coords(snake[a])):
            return True
    return False

def game_over():
    global window, ScoreMessage
    label = Label(window, text="Game Over", font=("Arial", 24))
    label.place(relx=0.5, rely=0.5, anchor="center")
    window.update()
    messagebox.showinfo("Game Over", "Your score: " + str(score))
    label.destroy()
    reset_game()

def reset_game():
    global snake, score, ScoreMessage, head

    # Clear the canvas
    GameCanvas.delete("all")

    # Initialize snake and other variables
    snake = []
    snake_size = 15

    head = GameCanvas.create_rectangle(100,100,snake_size+100,100+snake_size,fill="green")
    snake.append(head)

    score = 0
    score_text = create_text()

    ScoreMessage = GameCanvas.create_text(10, 10, text=score_text, fill="white", anchor="nw")

    # Set up initial conditions
    placeFood()
    move_snake()
def move_snake():
    global width, height, score, step_size, ScoreMessage

    positions = []
    
    TLx, TLy, BRx, BRy = GameCanvas.coords(head)
    px1, py1, px2, py2 = GameCanvas.coords(snake[len(snake)-1])
    positions.append([TLx, TLy, BRx, BRy])
    
    step_size = snake_size

    if positions[0][0] < 0:
        GameCanvas.coords(snake[0],width,positions[0][1],width-step_size,positions[0][3])
    elif positions[0][1] < 0:
        GameCanvas.coords(snake[0],positions[0][0],height,positions[0][2],height-step_size)
    elif positions[0][2] > width:
        GameCanvas.coords(snake[0],0-step_size,positions[0][1],0,positions[0][3])
    elif positions[0][3] > height:
        GameCanvas.coords(snake[0],positions[0][0],0-step_size,positions[0][2],0)
    
    positions.clear()

    TLx, TLy, BRx, BRy= GameCanvas.coords(head)
    positions.append([TLx, TLy, BRx, BRy])

    game_over_flag = crumple()
    move_snake_body()

    if direction=="left":
        GameCanvas.move(snake[0],-step_size,0)
    elif direction=="right":
        GameCanvas.move(snake[0],step_size,0)
    elif direction=="up":
        GameCanvas.move(snake[0],0,-step_size)
    elif direction=="down":
        GameCanvas.move(snake[0],0,step_size)
    
    if overlapping([TLx, TLy, BRx, BRy], GameCanvas.coords(food)):
        score += 1
        score_text = create_text()
        GameCanvas.delete(ScoreMessage)
        ScoreMessage = GameCanvas.create_text(10, 10, text=score_text, fill="white", anchor="nw")
        move_food()
        grow_snake(px1, py1, px2, py2)

    if not game_over_flag:
        window.after(10, move_snake)
    else:
        game_over()

# Set the dimensions of the window
width = 1366
height = 768

# Create the main window
window = set_window_dimensions(width, height)

# Create the canvas
GameCanvas = Canvas(window, bg="black", height=height, width=width)
GameCanvas.pack(expand=True)

# Initialize snake and other variables
snake = []
snake_size = 15

head = GameCanvas.create_rectangle(100,100,snake_size+100,100+snake_size,fill="green")
snake.append(head)

score = 0
score_text = create_text()

ScoreMessage = GameCanvas.create_text(10, 10, text=score_text, fill="white", anchor="nw")

# Set up key bindings
GameCanvas.bind("<Left>", leftKey)
GameCanvas.bind("<Right>", rightKey)
GameCanvas.bind("<Up>", upKey)
GameCanvas.bind("<Down>", downKey)
window.bind('<Escape>', exit_fullscreen)
GameCanvas.focus_set()

# Set initial direction
direction = "right"

# Set up initial conditions
placeFood()
move_snake()

# Start the Tkinter event loop
window.mainloop()
