
import customtkinter as ck
import main_tk
from test import get_displays

class SelectMonitor():

    def __init__(self, mainTk: main_tk.MainTKWrapper):
        self.mainTk = mainTk
        self.app = ck.CTkToplevel(self.mainTk.app)
        self.width = 500
        self.height = 400
        self.app.geometry(f"{self.width}x{self.height}+{800}+{0}")
        self.app.grab_set()

        self.frame_1 = ck.CTkFrame(master=self.app)
        self.frame_1.pack(pady=20, padx=60, fill="both", expand=True)
        self.frame_1.grid_columnconfigure(0, weight=1)

        self.label_display = ck.CTkLabel(master=self.frame_1, text="Select Display", font=("Arial", 16))
        self.label_display.grid(row=0, column=0, padx=60, pady=20)
        
        self.combobox_display = ck.CTkComboBox(self.frame_1, 
            state="readonly",
            command=self.select_monitor,
            values=[str(i + 1) for i in range(len(get_displays()))])
        self.combobox_display.grid(row=1, column=0, padx=60, pady=(0,20))
        
    def select_monitor(self, choice):
        self.mainTk.update_display(get_displays()[int(choice) - 1])
