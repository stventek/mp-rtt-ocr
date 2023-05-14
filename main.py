import os
import tkinter as tk
from real_time_translate import RealTimeTranslate
from selectable_frame import SelectableFrame

root = tk.Tk()

def open_window(window_class):
    return window_class(root)

if __name__ == "__main__":
    window_class = RealTimeTranslate if os.path.exists('data.json') else SelectableFrame
    window_app = open_window(window_class)
    root.mainloop()