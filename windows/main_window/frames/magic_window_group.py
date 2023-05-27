import customtkinter as ck
from windows.main_window.frames.custom_label_frame import CustomLabelFrame
from main_window_wrapper import MainTKWrapper

class MagicWindowGroup(CustomLabelFrame):
    def __init__(self, mainW: MainTKWrapper, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainW = mainW
        self.switch_var = ck.StringVar(value="on")
        self.switch_frame_magic = ck.CTkSwitch(master=self.frame_group, text="Frame/ unframe",
            variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch_frame_magic.pack(pady=5, padx=10)
        self.switch_frame_magic.configure(command=self.mainW.unframe_magic)