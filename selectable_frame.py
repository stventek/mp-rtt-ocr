
import json
import tkinter as tk
import main_tk

class SelectableFrame():

    c1 = None
    c2 = None
    
    def __init__(self, mainTk: main_tk.MainTK):
        self.mainTk = mainTk
        self.selectable_window = tk.Toplevel(self.mainTk.app)
        self.selectable_window.attributes("-fullscreen", True)
        self.selectable_window.attributes("-alpha", 0.7)
        self.canvas = tk.Canvas(self.selectable_window, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.selectable_window.bind("<Motion>", self.OnMouseMove)
        self.selectable_window.bind("<Button-1>", self.OnMouseDown)
        self.selectable_window.bind("<ButtonRelease-1>", self.OnMouseUp)


    def OnMouseMove(self, event):
        if self.c1 is None or event.state == 0: return
        self.c2 = event.x, event.y
        self.canvas.delete("selection")
        self.canvas.create_rectangle(self.c1, self.c2, outline="red", tags="selection")

    def OnMouseDown(self, event):
        self.c1 = event.x, event.y

    def OnMouseUp(self, event):
        self.mainTk.state.x1, self.mainTk.state.y1 = self.c1
        self.mainTk.state.x2, self.mainTk.state.y2 = self.c2
        self.mainTk.state.saveState()
        self.mainTk.bring_child_windows()
        self.mainTk.app.deiconify()
        if self.mainTk.translate_window is None:
            self.mainTk.open_translate_window()
        self.selectable_window.destroy()
