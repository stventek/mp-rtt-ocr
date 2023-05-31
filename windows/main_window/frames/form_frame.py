import customtkinter as ck
from windows.main_window.frames.controls_group import ControlsGroup
from windows.main_window.frames.custom_label_frame import CustomLabelFrame
from windows.main_window.frames.magic_window_group import MagicWindowGroup
from main_window_wrapper import MainTKWrapper
from windows.main_window.frames.metadata_group import MetadataGroup
from windows.main_window.frames.select_group import SelectGroup

class FormFrame(ck.CTkFrame):
    def __init__(self, mainW: MainTKWrapper, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainW = mainW

        # controls group
        self.group_label_controls = ControlsGroup(mainW, master=self,
            text="Controls", 
        )
        self.group_label_controls.grid(row=0, column=0, sticky='ewns', pady=(0,10), padx=(0,10))
        # select frame group
        self.group_label_static_frame = SelectGroup(mainW, master=self,
            text="Static frame settings", 
        )
        self.group_label_static_frame.grid(row=0, column=1, sticky='ewns', pady=(0,10))
        # Magic window group
        self.group_label_magic = MagicWindowGroup(mainW, master=self,
            text="Magic window settings", 
        )
        self.group_label_magic.grid(row=1, column=0, sticky='ewns', pady=0, padx=(0,10))
        # metadata group
        self.group_label_metadata= MetadataGroup(mainW, master=self,
            text="Metadata", 
        )
        self.group_label_metadata.grid(row=1, column=1, sticky='ewns')
