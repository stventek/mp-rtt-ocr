import tkinter as tk
from main_tk import MainTKWrapper
from toplevel_tks.borderless_window import BorderlessWindow

class CustomBorderlessWindow:

    def __init__(self, *args, **kwargs):
        self.app = tk.Toplevel(*args, **kwargs)
        self.app.overrideredirect(True)
        self.app.bind("<ButtonPress-1>", self.start_move)
        self.app.bind("<ButtonRelease-1>", self.stop_move)
        self.app.bind("<B1-Motion>", self.do_move)

    def start_move(self, event):
        if event.widget.widgetName != 'textArea' or event.widget.get(event.widget.index('current')) == '\n':
            self.x = event.x
            self.y = event.y
            self.app.event_generate('<<StartMove>>')

    def stop_move(self, event):
        if event.widget.widgetName != 'textArea' or event.widget.get(event.widget.index('current')) == '\n':
            self.x = None
            self.y = None
            self.app.event_generate('<<OnStopMove>>')

    def do_move(self, event):
        if event.widget.widgetName != 'textArea' or event.widget.get(event.widget.index('current')) == '\n':
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.app.winfo_x() + deltax
            y = self.app.winfo_y() + deltay
            self.app.geometry(f"+{x}+{y}")
            self.app.event_generate('<<OnMove>>')

class TextDisplayWindowWrapper:
    def __init__(self, root, mainTk: MainTKWrapper):
        self.mainTk = mainTk
        self.auto_mode = False
        self.hover = False
        self.root = root
        self.parent_toplevel = CustomBorderlessWindow(root, name="text_display_win_parent")
        self.main_window = self.parent_toplevel.app
        self.parent_toplevel.app.wm_attributes('-transparentcolor', 'black')
        self.parent_toplevel.app.configure(bg="black")
        self.parent_toplevel.app.geometry(f"{800}x{200}")
        self.parent_toplevel.app.wm_attributes('-topmost', True)
        self.parent_toplevel.app.bind('<<OnMove>>', self.on_parent_move)
        self.parent_toplevel.app.bind('<<OnStartMove>>', self.on_parent_move)
        self.parent_toplevel.app.bind('<<OnStopMove>>', self.on_parent_move)

        self.child_toplevel = BorderlessWindow(root, name="text_display_child")
        self.child_toplevel.app.attributes("-alpha", self.mainTk.state.text_opacity)
        self.child_toplevel.app.wm_attributes('-topmost', True)
        self.child_toplevel.app.configure(background='black')
        self.child_toplevel.app.bind('<<OnMove>>', self.on_child_move)
        self.child_toplevel.app.bind('<<OnStartMove>>', self.on_child_move)
        self.child_toplevel.app.bind('<<OnStopMove>>', self.on_child_move)
        
        self.parent_toplevel.app.update()
        self.parent_toplevel.app.update_idletasks()
        self.update_inner_window()
        
        # parent contet

        self.main_window.grid_columnconfigure(0, weight=1)
        self.main_window.grid_rowconfigure(1, weight=1)

        self.canvas_height = 30
        self.canvas = tk.Canvas(self.main_window, bg="black", highlightthickness=0, height=self.canvas_height)
        self.canvas.grid(row=0, column=0, sticky='ew')
        self.label = tk.Text(self.main_window, 
            fg='white', 
            border=0,
            background="black", 
            font=('Arial', 16))
        self.label.widgetName = 'textArea'
        self.label.grid(row=1, column=0, sticky='nesw', padx=self.canvas_height)
        self.label.configure(cursor='arrow')
        self.main_window.bind('<Configure>', self.update_parent_content)

        # parent grip
        self.grip_size = 10
        self.grip = tk.Frame(self.parent_toplevel.app, bg='white', width=self.grip_size, height=self.grip_size)
        self.grip.configure(cursor='sizing')
        self.grip.grid(row=2, column=0, sticky='se', pady=(self.canvas_height - self.grip_size,0))
        self.grip.bind('<ButtonPress-1>', self.start_resize)
        self.main_window.after(100, self.check_hover)

    def check_hover(self):

        x,y = self.main_window.winfo_pointerxy()
        wx, wy = self.main_window.winfo_x(), self.main_window.winfo_y()
        w, h = self.main_window.winfo_width(), self.main_window.winfo_height()
        endx, endy = wx + w, wy + h
        if x > wx and y > wy and x < endx and y < endy:
            if not self.hover:
                # in
                self.main_window.wm_attributes('-transparentcolor', '#3d0d01')
            self.hover = True
        else:
            if self.hover:
                # out
                 self.main_window.wm_attributes('-transparentcolor', 'black')
            self.hover = False
        self.main_window.after(100, self.check_hover)

    def update_parent_content(self, event):
        self.update_canvas()

    def update_canvas(self):
        if self.auto_mode:
            color = "#a83232"
        else:
            color = "black"
        self.canvas.delete('circle')
        circle_padding = 5
        circle_size = self.canvas_height - circle_padding
        circle_x = self.main_window.winfo_width() - circle_size - circle_padding 
        circle_y = circle_padding 

        self.canvas.create_oval(circle_x, 
            circle_y, 
            circle_x + circle_size, 
            circle_y + circle_size, 
            fill=color, tags='circle')

    def resize(self, event):
        x = self.parent_toplevel.app.winfo_rootx()  # Get the root window's x-coordinate
        y = self.parent_toplevel.app.winfo_rooty()  # Get the root window's y-coordinate
        w = event.x_root - x  # Calculate the new width relative to the root window
        h = event.y_root - y  # Calculate the new height relative to the root window
        if w > 0 and h > 0:
            self.parent_toplevel.app.geometry(f"{w}x{h}")
            self.child_toplevel.app.geometry(f"{w}x{h}")

    def stop_resize(self, event):
        self.resizing = False
        self.parent_toplevel.app.unbind('<B1-Motion>')
        self.parent_toplevel.app.unbind('<ButtonRelease-1>')
        self.parent_toplevel.app.bind("<ButtonRelease-1>", self.parent_toplevel.stop_move)
        self.parent_toplevel.app.bind("<B1-Motion>", self.parent_toplevel.do_move)

    def start_resize(self, event):
        self.resizing = True
        self.grip.configure(cursor='sizing')
        self.parent_toplevel.app.bind('<B1-Motion>', self.resize)
        self.parent_toplevel.app.bind('<ButtonRelease-1>', self.stop_resize)

    def update_inner_window(self):
        x = self.parent_toplevel.app.winfo_rootx()
        y = self.parent_toplevel.app.winfo_rooty()
        width = self.parent_toplevel.app.winfo_width()
        height = self.parent_toplevel.app.winfo_height()
        self.child_toplevel.app.geometry(f"{width}x{height}+{x}+{y}")

    def update_parent_window(self):
        x = self.child_toplevel.app.winfo_rootx()
        y = self.child_toplevel.app.winfo_rooty()
        width = self.parent_toplevel.app.winfo_width()
        height = self.parent_toplevel.app.winfo_height()
        self.parent_toplevel.app.geometry(f"{width}x{height}+{x}+{y}")
        self.parent_toplevel.app.lift()

    def on_parent_move(self, event):
        self.parent_toplevel.app.after_idle(self.update_inner_window)

    def on_child_move(self, event):
        self.parent_toplevel.app.after_idle(self.update_parent_window)


class TextDisplayWindowWrapperLinux:
    def __init__(self, root, mainTk: MainTKWrapper):
        self.mainTk = mainTk
        self.auto_mode = False
        self.root = root
        self.parent_toplevel = CustomBorderlessWindow(root, name="text_display_win_parent")
        self.main_window = self.parent_toplevel.app
        self.parent_toplevel.app.configure(bg="black")
        self.parent_toplevel.app.geometry(f"{800}x{200}")
        self.parent_toplevel.app.wm_attributes('-topmost', True)

        # parent contet

        self.main_window.grid_columnconfigure(0, weight=1)
        self.main_window.grid_rowconfigure(1, weight=1)

        self.canvas_height = 30
        self.canvas = tk.Canvas(self.main_window, bg="black", highlightthickness=0, height=self.canvas_height)
        self.canvas.grid(row=0, column=0, sticky='ew')

        self.label = tk.Text(self.main_window, 
                        fg='white', 
                        border=0,
                        background="black", 
                        font=('Arial', 16))
        self.label.widgetName = 'textArea'
        self.label.configure(cursor='arrow')
        self.label.grid(row=1, column=0, sticky='nesw', padx=self.canvas_height)
        
        self.main_window.bind('<Configure>', self.update_parent_content)

        # parent grip
        self.grip_size = 10
        self.grip = tk.Frame(self.parent_toplevel.app, bg='white', width=self.grip_size, height=self.grip_size)
        self.grip.configure(cursor='sizing')
        self.grip.grid(row=2, column=0, sticky='se', pady=(self.canvas_height - self.grip_size,0))
        self.grip.bind('<ButtonPress-1>', self.start_resize)

    def update_parent_content(self, event):
        self.update_canvas()

    def update_canvas(self):
        if self.auto_mode:
            color = "#a83232"
        else:
            color = "black"
        self.canvas.delete('circle')
        circle_padding = 5
        circle_size = self.canvas_height - circle_padding
        circle_x = self.main_window.winfo_width() - circle_size - circle_padding 
        circle_y = circle_padding 

        self.canvas.create_oval(circle_x, 
            circle_y, 
            circle_x + circle_size, 
            circle_y + circle_size, 
            fill=color, tags='circle')

    def resize(self, event):
        x = self.parent_toplevel.app.winfo_rootx()  # Get the root window's x-coordinate
        y = self.parent_toplevel.app.winfo_rooty()  # Get the root window's y-coordinate
        w = event.x_root - x  # Calculate the new width relative to the root window
        h = event.y_root - y  # Calculate the new height relative to the root window
        if w > 0 and h > 0:
            self.parent_toplevel.app.geometry(f"{w}x{h}")

    def stop_resize(self, event):
        self.resizing = False
        self.parent_toplevel.app.unbind('<B1-Motion>')
        self.parent_toplevel.app.unbind('<ButtonRelease-1>')
        self.parent_toplevel.app.bind("<ButtonRelease-1>", self.parent_toplevel.stop_move)
        self.parent_toplevel.app.bind("<B1-Motion>", self.parent_toplevel.do_move)

    def start_resize(self, event):
        self.resizing = True
        self.grip.configure(cursor='sizing')
        self.parent_toplevel.app.bind('<B1-Motion>', self.resize)
        self.parent_toplevel.app.bind('<ButtonRelease-1>', self.stop_resize)

