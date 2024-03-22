from tkinter import Tk, Label, PhotoImage
# import os

root2 = None

def boss_key_create():
    """function responsible for creating boss key window 
    and also listening to see if boss key is to be destroyed by pressing b
    """
    global root2
    if root2 is None:
        root2 = Tk()
        width = 1366
        height = 768
        screen_width = root2.winfo_screenwidth()
        screen_height = root2.winfo_screenheight()
        x1 = (screen_width - width) // 2
        y1 = (screen_height - height) // 2
        root2.geometry(f"{width}x{height}+{x1}+{y1}")
        root2.config(bg="#444444")

        # print("my current directory:",os.getcwd())
        # script_dir = os.path.dirname(os.path.abspath(__file__))
        # image_path = os.path.join(script_dir, "gameassets", "stars.png")

        # Create a PhotoImage and set it as the background
        # IMPORTANT: master set to this second root/window as
        # If you do not define a master then this image uses the first Tk() which 
        # is created and if that Tk is deleted there is no image to display.
        background_image = PhotoImage(master=root2, file="gameassets/work.png")
        background_label = Label(root2, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # root2.protocol("WM_DELETE_WINDOW", lambda: boss_key_destroyroot_boss))
        root2.bind("<KeyPress>", key_press)
        root2.mainloop()   

# if b is pressed then window is destoyed
def key_press(event) -> None:
    global root2
    if event.keysym == "b":
        if root2 != None:
            root2.destroy()
            root2 = None
