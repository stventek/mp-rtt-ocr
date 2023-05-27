import customtkinter as ck
from windows.main_window.frames.custom_label_frame import CustomLabelFrame
from main_window_wrapper import MainTKWrapper
from utils.get_displays import get_displays

class SelectGroup(CustomLabelFrame):
    def __init__(self, mainW: MainTKWrapper, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainW = mainW

        self.button_select_frame = ck.CTkButton(master=self.frame_group, 
            text="Select frame")
        self.button_select_frame.pack(pady=(20,5), padx=10)

        self.label_display = ck.CTkLabel(master=self.frame_group, text="Select Display", font=("Arial", 16))
        self.label_display.pack(pady=5, padx=10)
        
        self.combobox_display = ck.CTkComboBox(self.frame_group, 
            state="readonly",
            values=[str(i + 1) for i in range(len(get_displays()))])
        self.combobox_display.pack(pady=5, padx=10)

        self.button_select_frame.configure(command=self.mainW.select_frame)
        self.combobox_display.configure(command=self.update_display)
        self.combobox_display.set(self.mainW.state.display['choice'])

    def update_display(self, choice):
        self.mainW.state.display = get_displays()[int(choice) - 1]
        self.mainW.state.display["choice"] = choice
        self.mainW.state.saveState()