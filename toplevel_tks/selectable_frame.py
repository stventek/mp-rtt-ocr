import sys
import tkinter as tk
import main_tk

class SelectableFrame():

    def __init__(self, mainTk: main_tk.MainTKWrapper):
        self.c1 = None
        self.c2 = None
        self.p1 = None
        self.p2 = None
        self.mainTk = mainTk
        self.selectable_window = tk.Toplevel(self.mainTk.app)
        geometry_string = "{width}x{height}{sign}{left}{sign}{top}".format(
            width=self.mainTk.state.display["width"],
            height=self.mainTk.state.display["height"],
            sign="" if self.mainTk.state.display["left"] >= 0 else "-",
            left=abs(self.mainTk.state.display["left"]),
            top=self.mainTk.state.display["top"]
        )
        self.selectable_window.geometry(geometry_string)
        self.selectable_window.configure(bg='black')
        self.selectable_window.wm_attributes('-topmost', True)
        self.selectable_window.overrideredirect(True)
        self.canvas = tk.Canvas(self.selectable_window, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.selectable_window.bind("<Motion>", self.OnMouseMove)
        self.selectable_window.bind("<Button-1>", self.OnMouseDown)
        self.selectable_window.bind("<ButtonRelease-1>", self.OnMouseUp)
        self.selectable_window.focus_force()
        if sys.platform == "linux" or sys.platform == 'darwin':
            self.selectable_window.wait_visibility(self.selectable_window)
        self.selectable_window.attributes("-alpha", 0.7)

    def OnMouseMove(self, event):
        if self.c1 is None or event.state == 0: return
        self.c2 = event.x, event.y
        self.p2 = event.x_root, event.y_root
        self.canvas.delete("selection")
        self.canvas.create_rectangle(self.c1, self.c2, outline="red", tags="selection")

    def OnMouseDown(self, event):
        self.c1 = event.x, event.y
        self.p1 = event.x_root, event.y_root

    def OnMouseUp(self, event):
        self.mainTk.state.x1, self.mainTk.state.y1 = self.p1
        self.mainTk.state.x2, self.mainTk.state.y2 = self.p2
        self.mainTk.state.saveState()
        self.mainTk.bring_child_windows()
        self.mainTk.app.deiconify()
        self.selectable_window.destroy()
