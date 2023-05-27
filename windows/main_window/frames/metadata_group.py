import customtkinter as ck
from windows.main_window.frames.custom_label_frame import CustomLabelFrame
from main_window_wrapper import MainTKWrapper

class MetadataGroup(CustomLabelFrame):
    def __init__(self, mainW: MainTKWrapper, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainW = mainW

        self.translation_count = 0
        self.translation_timeouts = 0

        self.label_translation_count = ck.CTkLabel(master=self.frame_group, text="Translation count: 0")
        self.label_translation_count.pack(pady=5, padx=10)

        self.label_translation_timeouts = ck.CTkLabel(master=self.frame_group, text="Translation timeouts: 0")
        self.label_translation_timeouts.pack(pady=5, padx=10)
    
    def add_translation_count(self):
        self.translation_count += 1
        self.label_translation_count.configure(text=f"Translation count: {self.translation_count}")

    def add_translation_timeout(self):
        self.translation_timeouts += 1
        self.label_translation_timeouts.configure(text=f"Translation timeouts: {self.translation_timeouts}")
