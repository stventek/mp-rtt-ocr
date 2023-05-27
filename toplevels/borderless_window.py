import tkinter as tk

class BorderlessWindow:

    def __init__(self, *args, **kwargs):
        self.app = tk.Toplevel(*args, **kwargs)
        self.app.overrideredirect(True)
        self.app.bind("<ButtonPress-1>", self.start_move)
        self.app.bind("<ButtonRelease-1>", self.stop_move)
        self.app.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y
        self.app.event_generate('<<StartMove>>')

    def stop_move(self, event):
        self.x = None
        self.y = None
        self.app.event_generate('<<OnStopMove>>')

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.app.winfo_x() + deltax
        y = self.app.winfo_y() + deltay
        self.app.geometry(f"+{x}+{y}")
        self.app.event_generate('<<OnMove>>')