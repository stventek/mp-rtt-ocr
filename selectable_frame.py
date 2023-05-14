
import json
import tkinter as tk

from real_time_translate import RealTimeTranslate

class SelectableFrame():

    c1 = None
    c2 = None
    
    def __init__(self, root):
        self.root = root
        self.selectable_window = tk.Toplevel(self.root)
        self.selectable_window.title("")
        self.selectable_window.attributes("-fullscreen", True)

        self.canvas = tk.Canvas(self.selectable_window, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.menu = tk.Menu(self.selectable_window)
        self.menu.add_command(label="Transparency", command=self.OnTrans)
        self.selectable_window.config(menu=self.menu)

        self.selectable_window.bind("<Motion>", self.OnMouseMove)
        self.selectable_window.bind("<Button-1>", self.OnMouseDown)
        self.selectable_window.bind("<ButtonRelease-1>", self.OnMouseUp)

        self.transp = False
        self.selectable_window.after(250, self.OnTrans)

    def OnTrans(self, event=None):
        if self.transp == False:
            self.selectable_window.attributes("-alpha", 0.7)
            self.transp = True
        else:
            self.selectable_window.attributes("-alpha", 1.0)
            self.transp = False

    def OnMouseMove(self, event):
        if self.c1 is None or event.state == 0: return
        self.c2 = event.x, event.y
        self.canvas.delete("selection")
        self.canvas.create_rectangle(self.c1, self.c2, outline="red", tags="selection")

    def OnMouseDown(self, event):
        self.c1 = event.x, event.y

    def OnMouseUp(self, event):
        x1, y1 = self.c1
        x2, y2 = self.c2
        data = {
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2
        }
        with open('data.json', 'w') as f:
            json.dump(data, f)
        RealTimeTranslate()
        self.selectable_window.destroy()
