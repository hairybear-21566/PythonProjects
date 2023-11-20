import tkinter as tk
from tkinter import ttk, simpledialog
import subprocess

class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")

        # Create buttons
        play_button = ttk.Button(root, text="Play Music", command=self.play_music)
        stop_button = ttk.Button(root, text="Stop Music", command=self.stop_music)
        choose_button = ttk.Button(root, text="Choose Music", command=self.choose_music)

        play_button.pack(pady=20)
        stop_button.pack(pady=20)
        choose_button.pack(pady=20)

        self.music_file = ""

    def play_music(self):
        if self.music_file:
            subprocess.run(["vlc", self.music_file])

    def stop_music(self):
        subprocess.run(["pkill", "-9", "vlc"])

    def choose_music(self):
        self.music_file = simpledialog.askstring("Choose Music", "Enter the path to the music file")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()
