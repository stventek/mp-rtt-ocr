import pygame
import tkinter as tk
from tkinter import ttk

def play_song():
    pygame.mixer.music.load("s.mp3")
    pygame.mixer.music.play()

def stop_song():
    pygame.mixer.music.stop()

def change_volume(volume):
    pygame.mixer.music.set_volume(float(volume) / 100)

# Initialize Pygame Mixer
pygame.mixer.init()

# Create the Tkinter app
app = tk.Tk()
app.title("Music Player")

# Create volume slider
volume_label = ttk.Label(app, text="Volume:")
volume_label.pack()

volume_slider = ttk.Scale(app, from_=0, to=100, orient="horizontal", command=change_volume)
volume_slider.set(50)  # Set initial volume to 50
volume_slider.pack()

# Create buttons
play_button = ttk.Button(app, text="Play", command=play_song)
play_button.pack()

stop_button = ttk.Button(app, text="Stop", command=stop_song)
stop_button.pack()

# Run the app
app.mainloop()
