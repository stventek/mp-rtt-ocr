import sys
import tkinter as tk
import main_tk
from toplevel_tks.borderless_window import BorderlessWindow
from utils.draw_corners import draw_corners

class MagicWindow():

    def __init__(self, mainTk: main_tk.MainTKWrapper):
        self.mainTk = mainTk
        self.borderlessW = BorderlessWindow(self.mainTk.app, name="magic_window")
        self.width = 800
        self.height = 200
        self.resizing = None
        self.frame_size = 5
        self.hover = False
        self.unframe = False
        self.borderlessW.app.title("magic window")
        self.borderlessW.app.geometry(f"{self.width}x{self.height}")
        if sys.platform == 'linux' or sys.platform == 'darwin':
            self.borderlessW.app.wait_visibility(self.borderlessW.app)
        else:
            self.borderlessW.app.wm_attributes('-transparentcolor', 'black')
        self.borderlessW.app.attributes("-alpha", 0.5)
        self.borderlessW.app.wm_attributes('-topmost', True)
        self.frame = tk.Frame(self.borderlessW.app, bg="black")
        self.frame.pack(fill='both', expand=True)
        self.canvas = tk.Canvas(self.frame, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.grid_columnconfigure(0, weight=1)
        self.canvas.grid_rowconfigure(0, weight=1)
        self.grip = tk.Frame(self.canvas, bg='white', width=self.frame_size, height=self.frame_size)
        self.grip.configure(cursor='sizing')
        self.grip.grid(column=0, row=0, sticky='se')
        self.grip.bind('<ButtonPress-1>', self.start_resize)
        draw_corners(self.canvas, 0, 0, self.width, self.height, tags='lines', width=self.frame_size)
        if sys.platform != 'linux' and sys.platform != 'darwin':
            self.borderlessW.app.after(100, self.check_hover)
        self.borderlessW.app.bind('<Configure>', self.update_win_info)

    def update_win_info(self, event):
        wx, wy = self.borderlessW.app.winfo_x(), self.borderlessW.app.winfo_y()
        w, h = self.borderlessW.app.winfo_width(), self.borderlessW.app.winfo_height()
        self.window_square = (wx + self.frame_size ,wy + self.frame_size, w - self.frame_size, h - self.frame_size,)
        
    def unframe_window(self):
        self.unframe = not self.unframe
        if self.unframe:
            self.canvas.pack_forget()
        else:
            self.canvas.pack(fill='both', expand=True)

    def resize(self, event):
        x = self.borderlessW.app.winfo_rootx() 
        y = self.borderlessW.app.winfo_rooty()  
        w = event.x_root - x  
        h = event.y_root - y  
        if w > 0 and h > 0:
            self.canvas.delete('lines')
            draw_corners(self.canvas, 0, 0, w, h, tags='lines', width=self.frame_size)
            self.borderlessW.app.geometry(f"{w}x{h}")

    def stop_resize(self, event):
        self.resizing = False
        self.borderlessW.app.unbind('<B1-Motion>')
        self.borderlessW.app.unbind('<ButtonRelease-1>')
        self.borderlessW.app.bind("<ButtonRelease-1>", self.borderlessW.stop_move)
        self.borderlessW.app.bind("<B1-Motion>", self.borderlessW.do_move)
        
    def start_resize(self, event):
        self.resizing = True
        self.grip.configure(cursor='sizing')
        self.borderlessW.app.bind('<B1-Motion>', self.resize)
        self.borderlessW.app.bind('<ButtonRelease-1>', self.stop_resize)

    def check_hover(self):
        if not self.resizing:
            x,y = self.borderlessW.app.winfo_pointerxy()
            wx, wy = self.borderlessW.app.winfo_x(), self.borderlessW.app.winfo_y()
            w, h = self.borderlessW.app.winfo_width(), self.borderlessW.app.winfo_height()
            endx, endy = wx + w, wy + h

            if x > wx and y > wy and x < endx and y < endy:
                if not self.hover:
                    # in
                    self.borderlessW.app.wm_attributes('-transparentcolor', '#3d0d01')
                self.hover = True
            else:
                if self.hover:
                    # out
                    self.borderlessW.app.wm_attributes('-transparentcolor', 'black')
                self.hover = False
        self.borderlessW.app.after(100, self.check_hover)

    def destroy(self):
        self.borderlessW.app.destroy()