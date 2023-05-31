import customtkinter
from customtkinter import ThemeManager
from main_window_wrapper import MainTKWrapper
from windows.main_window.frames.maintk_frame import MainTKFrame

customtkinter.set_default_color_theme("custom_theme.json")
appearance_mode = customtkinter.AppearanceModeTracker()

class MainTKWindow(customtkinter.CTk):
    def __init__(self, mainW: MainTKWrapper, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Real Time OCR translator")
        self.width = 900
        self.height = 600
        self.geometry(f"{self.width}x{self.height}")
        self.main_tk_frame = MainTKFrame(mainW, master=self, fg_color=ThemeManager.theme["CTk"]["fg_color"])
        self.main_tk_frame.pack(fill="both", expand=True)