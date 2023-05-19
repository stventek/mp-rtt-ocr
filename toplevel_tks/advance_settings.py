
import customtkinter as ck
import main_tk

class AdvanceSettings():

    def __init__(self, mainTk: main_tk.MainTKWrapper):
        self.mainTk = mainTk
        self.log_levels = {
            "CRITICAL": 50,
            "ERROR": 40,
            "WARNING": 30,
            "INFO": 20,
            "DEBUG": 10,
            "NOTSET": 0,
        }
        self.app = ck.CTkToplevel(self.mainTk.app)
        self.app.title("Advance Settings")
        self.width = 600
        self.height = 400

        self.app.geometry(f"{self.width}x{self.height}+{800}+{0}")
        self.app.transient(self.mainTk.app)
        self.app.grab_set()

        self.frame_1 = ck.CTkFrame(master=self.app)
        self.frame_1.pack(pady=20, padx=60, fill="both", expand=True)
        self.frame_1.grid_columnconfigure(0, weight=1)
        self.frame_1.grid_columnconfigure(1, weight=1)
        
        self.label_ocr_interval = ck.CTkLabel(self.frame_1, text="OCR interval in ms (250 default)")
        self.label_ocr_interval.grid(row=0, column=0, pady=(60,0), padx=(0,20), sticky='e')

        self.ocr_interval = ck.StringVar(value=self.mainTk.state.ocr_interval)
        self.entry_ocr_interval = ck.CTkEntry(master=self.frame_1, placeholder_text="250 default", textvariable=self.ocr_interval)
        self.entry_ocr_interval.grid(row=0, column=1, pady=(60,0), sticky='w')

        self.label_translation_timeout = ck.CTkLabel(self.frame_1, text="Translation request timeout (8000 default)")
        self.label_translation_timeout.grid(row=1, column=0, pady=(20,0), padx=(0,20), sticky='e')

        self.translate_timeout = ck.StringVar(value=self.mainTk.state.translate_timeout)
        self.entry_translate_timeout = ck.CTkEntry(master=self.frame_1, placeholder_text="8000 default", textvariable=self.translate_timeout)
        self.entry_translate_timeout.grid(row=1, column=1, pady=(20,0), sticky='w')

        self.label_log_level = ck.CTkLabel(self.frame_1, text="Log level")
        self.label_log_level.grid(row=2, column=0, pady=(20,0), padx=(0,20), sticky='e')

        self.combobox_log_level = ck.CTkComboBox(self.frame_1, 
            state="readonly",
            values=list(self.log_levels.keys()))
        self.combobox_log_level.grid(row=2, column=1, pady=(20,0), sticky="w")
        self.combobox_log_level.set(self.mainTk.state.log_level)

        self.debug_mode = ck.StringVar(value=self.mainTk.state.debug_mode)
        self.checkbox_debug_mode = ck.CTkCheckBox(self.frame_1, text="Debug mode",
                                     variable=self.debug_mode, onvalue="on", offvalue="off")
        self.checkbox_debug_mode.grid(row=3, column=1, pady=(20,0), sticky='w')

        self.button_save = ck.CTkButton(master=self.frame_1, text="Save", command=self.save)
        self.button_save.grid(row=4, column=1, pady=(40,0), sticky="w")

    def save(self):
        self.mainTk.state.ocr_interval = self.ocr_interval.get()
        self.mainTk.state.translate_timeout = self.translate_timeout.get()
        self.mainTk.state.debug_mode = self.debug_mode.get()
        self.mainTk.state.log_level = self.combobox_log_level.get()
        self.mainTk.state.saveState()
        self.app.destroy()