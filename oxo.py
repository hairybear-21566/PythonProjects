from tkinter import Button, Tk, PhotoImage, Label

GameGrid = [[None, None, None] for i in range(3)]
NGrid = [[0, 0, 0] for i in range(3)]
root = Tk()
root.title("xox")
root.geometry("300x300")
player1Turn = True
counter=0


def square_taken():
    # Display label
    label = Label(root, text="This tile is taken", font=("Arial", 12))
    label.place(x=150, y=150)
    root.after(3000, label.destroy)  # Remove label after 3000 milliseconds

def checkWin()-> int:
    for i in range(3):
        if NGrid[i][0]==NGrid[i][1]==NGrid[i][2] and NGrid[i][0]!=0:
            return NGrid[i][0]
        if NGrid[0][i]==NGrid[1][i]==NGrid[2][i] and NGrid[0][i]!=0:
            return NGrid[0][i]
        
    if (NGrid[0][0]==NGrid[1][1]==NGrid[2][2] or NGrid[0][2]==NGrid[1][1]==NGrid[2][0]) and NGrid[1][1]!=0:
        return NGrid[1][1]
    
    
    return 0

def handle_button_click(butNum):
    global player1Turn
    global counter
    
    counter+=1
    button = GameGrid[butNum // 3][butNum % 3]
    button.configure(image=P1ButtonIMG if player1Turn else P2ButtonIMG,command=square_taken)
    
    button.image = P1ButtonIMG if player1Turn else P2ButtonIMG
    NGrid[butNum // 3][butNum % 3] = 1 if player1Turn else 2
    n=checkWin()

    if n!=0:
        label = Label(root, text="Player"+str(n)+"wins", font=("Arial", 12))
        label.place(x=150, y=150)
        root.after(3000, label.destroy)
        for j in range(3):
            for k in range(3):
                GameGrid[j][k].config(state="disabled",relief="sunken", bd=2)
    elif counter==9:
        label = Label(root, text="draw", font=("Arial", 12))
        label.place(x=150, y=150)
        root.after(3000, label.destroy)
        for j in range(3):
            for k in range(3):
                GameGrid[j][k].config(state="disabled",relief="sunken", bd=2)
    player1Turn = not player1Turn

def create_buttons():
    for i in range(9):
        myButton = Button(
            root,
            image=regularButtonIMG,
            width=100,
            height=100,
            command=lambda i=i: handle_button_click(i)
        )
        myButton.place(x=(i % 3) * 100, y=(i // 3) * 100)
        GameGrid[i // 3][i % 3] = myButton

regularButtonIMG = PhotoImage(file="images/myButton.png")
P1ButtonIMG = PhotoImage(file="images/myButtonP1.png")
P2ButtonIMG = PhotoImage(file="images/myButtonP2.png")
winnerIMG = PhotoImage(file="images/winner.png")

# Adjust the image sizes as needed
relsize=regularButtonIMG.width()
image_size = 100
regularButtonIMG = regularButtonIMG.zoom(image_size)
regularButtonIMG = regularButtonIMG.subsample(relsize)

P1ButtonIMG = P1ButtonIMG.zoom(image_size)
P1ButtonIMG = P1ButtonIMG.subsample(relsize)

P2ButtonIMG = P2ButtonIMG.zoom(image_size)
P2ButtonIMG = P2ButtonIMG.subsample(relsize)

winnerIMG = winnerIMG.zoom(image_size)
winnerIMG = winnerIMG.subsample(relsize)

create_buttons()
root.mainloop()
