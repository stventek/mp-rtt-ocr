import customtkinter as ck
from frames.custom_label_frame import CustomLabelFrame
from customtkinter import ThemeManager
from utils.get_displays import get_displays

class MainTKFrame(ck.CTkFrame):
    def __init__(self, *args, **kwargs):
        ck.CTkFrame.__init__(self, *args, **kwargs)

        # logs group
        self.group_label_logs = CustomLabelFrame(self,
            text="Logs", 
        )

        self.label_logs = ck.CTkLabel(master=self.group_label_logs.frame_group, text="Logs", font=("Arial", 24))
        self.label_logs.pack(pady=(20,5), padx=10)

        self.textbox_logs = ck.CTkTextbox(master=self.group_label_logs.frame_group, state='disabled')
        self.textbox_logs.pack(pady=15, padx=20,  fill="both", expand=True)

        self.main_frame = ck.CTkFrame(self, fg_color=ThemeManager.theme['CTk']['fg_color'])
        self.main_frame.pack(fill='y', side='right', padx=(0,10), pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        # controls group
        self.group_label_controls = CustomLabelFrame(self.main_frame,
            text="Controls", 
        )
        self.group_label_controls.grid(row=0, column=0, sticky='ewns', pady=(0,10), padx=(0,10))

        self.group_label_controls.frame_group.grid_columnconfigure(0, weight=1)
        self.group_label_controls.frame_group.grid_columnconfigure(1, weight=1)

        self.button_snapshot = ck.CTkButton(master=self.group_label_controls.frame_group, text="Snapshot")
        self.button_snapshot.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        self.button_set_auto_mode = ck.CTkButton(master=self.group_label_controls.frame_group, text="Auto mode")
        self.button_set_auto_mode.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        self.label_mode = ck.CTkLabel(master=self.group_label_controls.frame_group, text="OCR Mode")
        self.label_mode.grid(row=2, column=0, padx=10, pady=10, sticky='e')

        self.combobox_mode = ck.CTkComboBox(self.group_label_controls.frame_group,
            state="readonly", 
            values=["Static Frame", "Magic Window"])
        
        self.combobox_mode.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.combobox_mode.set("Static Frame")

        self.label_1_translator = ck.CTkLabel(master=self.group_label_controls.frame_group, text="Translator")
        self.label_1_translator.grid(row=3, column=0, padx=10, pady=10, sticky='e')

        self.combobox_translator = ck.CTkComboBox(self.group_label_controls.frame_group, 
            state="readonly", 
            values=["Deepl", "Google"])
        
        self.combobox_translator.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        self.label_2 = ck.CTkLabel(master=self.group_label_controls.frame_group, text="From")
        self.label_2.grid(row=4, column=0, padx=10, pady=10, sticky='e')

        self.combobox_from = ck.CTkComboBox(
            self.group_label_controls.frame_group, 
            state="readonly",
            values=[])
        self.combobox_from.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        self.label_3 = ck.CTkLabel(master=self.group_label_controls.frame_group, text="To")
        self.label_3.grid(row=5, column=0, padx=10, pady=10, sticky='e')

        self.combobox_to = ck.CTkComboBox(self.group_label_controls.frame_group, 
            state="readonly",
            values=[])
        self.combobox_to.grid(row=5, column=1, padx=10, pady=10, sticky='w')

        self.button_advance = ck.CTkButton(master=self.group_label_controls.frame_group, text="Advance Settings")
        self.button_advance.grid(row=6, column=1, padx=10, pady=10, sticky='w')

        # select frame group

        self.group_label_static_frame = CustomLabelFrame(self.main_frame,
            text="Static frame settings", 
        )
        self.group_label_static_frame.grid(row=0, column=1, sticky='ewns', pady=(0,10))

        self.button_select_frame = ck.CTkButton(master=self.group_label_static_frame.frame_group, 
            text="Select frame")
        self.button_select_frame.pack(pady=(20,5), padx=10)

        self.label_display = ck.CTkLabel(master=self.group_label_static_frame.frame_group, text="Select Display", font=("Arial", 16))
        self.label_display.pack(pady=5, padx=10)
        
        self.combobox_display = ck.CTkComboBox(self.group_label_static_frame.frame_group, 
            state="readonly",
            values=[str(i + 1) for i in range(len(get_displays()))])
        self.combobox_display.pack(pady=5, padx=10)

        # Magic window group

        self.group_label_magic = CustomLabelFrame(self.main_frame,
            text="Magic window settings", 
        )
        self.group_label_magic.grid(row=1, column=0, sticky='ewns', pady=0, padx=(0,10))

        self.switch_var = ck.StringVar(value="on")
        self.switch_frame_magic = ck.CTkSwitch(master=self.group_label_magic.frame_group, text="Frame/ unframe",
            variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch_frame_magic.pack(pady=5, padx=10)

        # metadata group

        self.group_label_metadata= CustomLabelFrame(self.main_frame,
            text="Metadata", 
        )
        self.group_label_metadata.grid(row=1, column=1, sticky='ewns')

        self.label_translation_count = ck.CTkLabel(master=self.group_label_metadata.frame_group, text="Translation count: 0")
        self.label_translation_count.pack(pady=5, padx=10)

        self.label_translation_timeouts = ck.CTkLabel(master=self.group_label_metadata.frame_group, text="Translation timeouts: 0")
        self.label_translation_timeouts.pack(pady=5, padx=10)