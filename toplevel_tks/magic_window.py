import tkinter as tk
import customtkinter as ck
import main_tk
import tkinter.ttk as ttk
from utils.draw_corners import draw_corners

class MagicWindow():

    def __init__(self, mainTk: main_tk.MainTKWrapper):
        self.mainTk = mainTk
        self.app = tk.Toplevel(self.mainTk.app, name="magic_window")
        self.width = 600
        self.height = 200
        self.resizing = None
        self.app.overrideredirect(True)
        self.app.title("magic window")
        self.app.geometry(f"{self.width}x{self.height}+{800}+{500}")
        self.app.wm_attributes('-transparentcolor', 'black')
        self.app.attributes("-alpha", 0.6)
        self.app.wm_attributes('-topmost', True)
        self.app.bind("<ButtonPress-1>", self.start_move)
        self.app.bind("<ButtonRelease-1>", self.stop_move)
        self.app.bind("<B1-Motion>", self.do_move)
        self.frame = tk.Frame(self.app, bg="black")
        self.frame.pack(fill='both', expand=True)
        self.canvas = tk.Canvas(self.frame, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.unframe = False
        self.canvas.grid_columnconfigure(0, weight=1)
        self.canvas.grid_rowconfigure(0, weight=1)
        self.frame_size = 5
        self.grip = tk.Frame(self.canvas, bg='white', width=self.frame_size, height=self.frame_size)
        self.grip.configure(cursor='sizing')
        self.grip.grid(column=0, row=0, sticky='se')
        self.grip.bind('<ButtonPress-1>', self.start_resize)

        draw_corners(self.canvas, 0, 0, self.width, self.height, tags='lines', width=self.frame_size)
        self.app.after(100, self.check_hover)
        self.hover = False


    def unframe_window(self):
        self.unframe = not self.unframe
        if self.unframe:
            self.canvas.pack_forget()
        else:
            self.canvas.pack(fill='both', expand=True)

    def resize(self, event):
        x = self.app.winfo_rootx()  # Get the root window's x-coordinate
        y = self.app.winfo_rooty()  # Get the root window's y-coordinate
        w = event.x_root - x  # Calculate the new width relative to the root window
        h = event.y_root - y  # Calculate the new height relative to the root window
        if w > 0 and h > 0:
            self.canvas.delete('lines')
            draw_corners(self.canvas, 0, 0, w, h, tags='lines', width=self.frame_size)
            self.app.geometry(f"{w}x{h}")

    def stop_resize(self, event):
        self.resizing = False
        self.app.unbind('<B1-Motion>')
        self.app.unbind('<ButtonRelease-1>')
        self.app.bind("<ButtonRelease-1>", self.stop_move)
        self.app.bind("<B1-Motion>", self.do_move)

    def start_resize(self, event):
        self.resizing = True
        self.grip.configure(cursor='sizing')
        self.app.bind('<B1-Motion>', self.resize)
        self.app.bind('<ButtonRelease-1>', self.stop_resize)

    def check_hover(self):
        if not self.resizing:
            x,y = self.app.winfo_pointerxy()
            wx, wy = self.app.winfo_x(), self.app.winfo_y()
            w, h = self.app.winfo_width(), self.app.winfo_height()
            endx, endy = wx + w, wy + h
            self.window_square = (wx + self.frame_size ,wy + self.frame_size, w - self.frame_size, h - self.frame_size,)

            if x > wx and y > wy and x < endx and y < endy:
                if not self.hover:
                    # in
                    self.app.wm_attributes('-transparentcolor', '#3d0d01')
                self.hover = True
            else:
                if self.hover:
                    # out
                    self.app.wm_attributes('-transparentcolor', 'black')
                self.hover = False
        self.app.after(100, self.check_hover)

    def start_move(self, event):
        if not self.resizing:
            self.x = event.x
            self.y = event.y

    def stop_move(self, event):
        if not self.resizing:
            self.x = None
            self.y = None

    def do_move(self, event):
        if not self.resizing:
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.app.winfo_x() + deltax
            y = self.app.winfo_y() + deltay
            self.app.geometry(f"+{x}+{y}")

    def destroy(self):
        self.app.destroy()