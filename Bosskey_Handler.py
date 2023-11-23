from tkinter import Tk

root2 = None


def bossKeyCreate(rootBoss: Tk = None) -> Tk:
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
        # root2.protocol("WM_DELETE_WINDOW", lambda: bossKeyDestroy(rootBoss))
        root2.bind("<KeyPress>", key_press)
        root2.mainloop()
    else:
        bossKeyDestroy(rootBoss)
    return rootBoss


def bossKeyDestroy(rootBoss: Tk) -> None:
    rootBoss.destroy()


def key_press(event) -> None:
    global root2
    if root2 != None:
        root2.destroy()
        root2 = None
    pass
