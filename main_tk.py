import asyncio
import threading
import customtkinter
from frames.custom_label_frame import CustomLabelFrame
from utils.get_displays import get_displays
from utils.main_tk_state import StateData
from utils.translate_word import deepl_lang_codes, google_lang_codes
import tkinter as tk
import tkinter.ttk as ttk

customtkinter.set_default_color_theme("custom_theme.json")
#customtkinter.set_widget_scaling(1.2)
theme = customtkinter.ThemeManager()

class MainTKWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Real Time OCR translator")
        self.width = 900
        self.height = 600
        self.geometry(f"{self.width}x{self.height}+{800}+{0}")

        style = ttk.Style(self)
        style.theme_create("style", settings = { 
            "TLabelframe": {
                "configure": {
                    "background": theme.theme['CTkFrame']['top_fg_color'][1],
                    "borderwidth": 1
                }
            },
            'TLabelframe.Label': {
                'configure': {
                    'background': 'transparent',
                    'foreground': 'white'
                }
            }
        })
        style.theme_use("style")

        # logs group

        self.group_label_logs = CustomLabelFrame(self,
            text="Logs", 
        )
        self.group_label_logs.pack(fill='both', expand=True, side='left', padx=10, pady=10)

        self.label_logs = customtkinter.CTkLabel(master=self.group_label_logs.frame_group, text="Logs", font=("Arial", 24))
        self.label_logs.pack(pady=(20,5), padx=10)

        self.textbox_logs = customtkinter.CTkTextbox(master=self.group_label_logs.frame_group)
        self.textbox_logs.pack(pady=15, padx=20,  fill="both", expand=True)

        self.main_frame = customtkinter.CTkFrame(self, fg_color="gray14")
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

        self.button_snapshot = customtkinter.CTkButton(master=self.group_label_controls.frame_group, text="Snapshot")
        self.button_snapshot.grid(row=0, column=1, pady=(20,0), padx=(0,20), sticky='w')

        self.button_set_auto_mode = customtkinter.CTkButton(master=self.group_label_controls.frame_group, text="Auto mode")
        self.button_set_auto_mode.grid(row=1, column=1, pady=(20,0), padx=(0,20), sticky='w')

        self.label_mode = customtkinter.CTkLabel(master=self.group_label_controls.frame_group, text="OCR Mode")
        self.label_mode.grid(row=2, column=0, pady=(20,0), padx=(0,20), sticky='e')

        self.combobox_mode = customtkinter.CTkComboBox(self.group_label_controls.frame_group, 
            state="readonly", 
            values=["Static Frame", "Magic Window"])
        
        self.combobox_mode.grid(row=2, column=1, pady=(20,0), padx=(0,20), sticky='w')
        self.combobox_mode.set("Static Frame")

        self.label_1_translator = customtkinter.CTkLabel(master=self.group_label_controls.frame_group, text="Translator")
        self.label_1_translator.grid(row=3, column=0, pady=(20,0), padx=(0,20), sticky='e')

        self.combobox_translator = customtkinter.CTkComboBox(self.group_label_controls.frame_group, 
            state="readonly", 
            values=["Deepl", "Google"])
        
        self.combobox_translator.grid(row=3, column=1, pady=(20,0), padx=(0,20), sticky='w')

        self.label_2 = customtkinter.CTkLabel(master=self.group_label_controls.frame_group, text="From")
        self.label_2.grid(row=4, column=0, pady=(20,0), padx=(0,20), sticky='e')

        self.combobox_from = customtkinter.CTkComboBox(
            self.group_label_controls.frame_group, 
            state="readonly",
            values=list(deepl_lang_codes.keys()))
        self.combobox_from.grid(row=4, column=1, pady=(20,0), padx=(0,20), sticky='w')

        self.label_3 = customtkinter.CTkLabel(master=self.group_label_controls.frame_group, text="To")
        self.label_3.grid(row=5, column=0, pady=(20,0), padx=(0,20), sticky='e')

        self.combobox_to = customtkinter.CTkComboBox(self.group_label_controls.frame_group, 
            state="readonly",
            values=list(deepl_lang_codes.keys()))
        self.combobox_to.grid(row=5, column=1, pady=(20,0), padx=(0,20), sticky='w')

        self.button_advance = customtkinter.CTkButton(master=self.group_label_controls.frame_group, text="Advance Settings")
        self.button_advance.grid(row=6, column=1, pady=(20), padx=(0,20), sticky='w')

        # select frame group

        self.group_label_static_frame = CustomLabelFrame(self.main_frame,
            text="Static frame settings", 
        )
        self.group_label_static_frame.grid(row=0, column=1, sticky='ewns', pady=(0,10))

        self.button_select_frame = customtkinter.CTkButton(master=self.group_label_static_frame.frame_group, 
            text="Select frame")
        self.button_select_frame.pack(pady=(20,5), padx=10)

        self.label_display = customtkinter.CTkLabel(master=self.group_label_static_frame.frame_group, text="Select Display", font=("Arial", 16))
        self.label_display.pack(pady=5, padx=10)
        
        self.combobox_display = customtkinter.CTkComboBox(self.group_label_static_frame.frame_group, 
            state="readonly",
            values=[str(i + 1) for i in range(len(get_displays()))])
        self.combobox_display.pack(pady=5, padx=10)

        # Magic window group

        self.group_label_magic = CustomLabelFrame(self.main_frame,
            text="Magic window settings", 
        )
        self.group_label_magic.grid(row=1, column=0, sticky='ewns', pady=0, padx=(0,10))

        switch_var = customtkinter.StringVar(value="on")
        self.switch_frame_magic = customtkinter.CTkSwitch(master=self.group_label_magic.frame_group, text="Frame/ unframe",
            variable=switch_var, onvalue="on", offvalue="off")
        self.switch_frame_magic.pack(pady=5, padx=10)
        # metadata group

        self.group_label_metadata= CustomLabelFrame(self.main_frame,
            text="Metadata", 
        )
        self.group_label_metadata.grid(row=1, column=1, sticky='ewns')

        self.label_metadata = customtkinter.CTkLabel(master=self.group_label_metadata.frame_group, text="Metadata")
        self.label_metadata.pack(pady=(20,5), padx=10)

        self.label_translation_count = customtkinter.CTkLabel(master=self.group_label_metadata.frame_group, text="Translation count: 0")
        self.label_translation_count.pack(pady=5, padx=10)

        self.label_translation_timeouts = customtkinter.CTkLabel(master=self.group_label_metadata.frame_group, text="Translation timeouts: 0")
        self.label_translation_timeouts.pack(pady=5, padx=10)

class MainTKWrapper():

    def __init__(self):
        self.app = MainTKWindow()
        self.state = StateData()
        self.translation_count = 0
        self.translation_timeouts = 0
        self.translate_window_wrapper = None
        self.selectable_frame_window = None
        self.select_monitor_window = None

        self.app.button_set_auto_mode.configure(command=self.toggle_auto)

        self.app.button_snapshot.configure(command=self.snapshot)

        self.app.button_select_frame.configure(command=self.select_frame)
        
        self.app.combobox_display.configure(command=self.update_display)
        self.app.combobox_display.set(self.state.display['choice'])

        self.app.combobox_translator.configure(command=self.update_translator_combobox)
        self.app.combobox_translator.set(self.state.translator)

        self.app.combobox_from.configure(command=self.update_from_lang_combobox)
        self.app.combobox_from.set(self.state.from_lang)

        self.app.combobox_to.configure(command=self.update_to_lang_combobox)
        self.app.combobox_to.set(self.state.to_lang)

        self.app.button_advance.configure(command=self.open_advance)

        self.open_translate_window()

    def open_advance(self):
        from toplevel_tks.advance_settings import AdvanceSettings
        self.advance_settings_wrapper = AdvanceSettings(self) 

    def toggle_auto(self):
        if self.translate_window_wrapper:
            self.translate_window_wrapper.toggle_auto()

    def snapshot(self):
        if self.translate_window_wrapper:
            threading.Thread(target=self.snapshot_call).start()

    def snapshot_call(self):
        asyncio.run(self.translate_window_wrapper.keep_translating())

    def open_translate_window(self):
        if self.state.x1 is not None:
            from toplevel_tks.real_time_translate import TranslateWindowWrapper
            self.translate_window_wrapper = TranslateWindowWrapper(self)

    def add_log(self, log):
        self.app.textbox_logs.configure(state="normal") 
        self.app.textbox_logs.insert(tk.END, log + "\n")
        self.app.textbox_logs.see(tk.END)
        self.app.textbox_logs.configure(state="disabled") 
        self.app.textbox_logs.update()

    def add_translation_count(self):
        self.translation_count += 1
        self.app.label_translation_count.configure(text=f"Translation count: {self.translation_count}")

    def add_translation_timeout(self):
        self.translation_timeouts += 1
        self.app.label_translation_timeouts.configure(text=f"Translation timeouts: {self.translation_timeouts}")

    def update_from_lang_combobox(self, choice):
        self.state.from_lang = choice
        self.state.saveState()

    def update_to_lang_combobox(self, choice):
        self.state.to_lang = choice
        self.state.saveState()

    def update_display(self, choice):
        self.state.display = get_displays()[int(choice) - 1]
        self.state.display["choice"] = choice
        self.state.saveState()

    def update_translator_combobox(self, choice):
        self.state.translator = choice
        self.state.saveState()

        if choice == "Deepl":
            self.app.combobox_from.configure(values=list(deepl_lang_codes.keys()))
            self.app.combobox_to.configure(values=list(deepl_lang_codes.keys()))

            if deepl_lang_codes.get(self.state.from_lang) is None:
                from_lang = next(iter(deepl_lang_codes)) 
                self.state.from_lang = from_lang
                self.state.saveState()
                self.app.combobox_from.set(from_lang)

            if deepl_lang_codes.get(self.state.to_lang) is None:
                to_lang = next(iter(deepl_lang_codes)) 
                self.state.to_lang = to_lang
                self.state.saveState()
                self.app.combobox_to.set(to_lang)
            
        elif choice == "Google":
            self.app.combobox_from.configure(values=list(google_lang_codes.keys()))
            self.app.combobox_to.configure(values=list(google_lang_codes.keys()))

            if google_lang_codes.get(self.state.from_lang) is None:
                from_lang = next(iter(google_lang_codes)) 
                self.state.from_lang = from_lang
                self.state.saveState()
                self.app.combobox_to.set(from_lang)
            if google_lang_codes.get(self.state.to_lang) is None:
                to_lang = next(iter(google_lang_codes)) 
                self.state.to_lang = to_lang
                self.state.saveState()
                self.app.combobox_to.set(to_lang)

    def bring_child_windows(self):
        for child in self.app.winfo_children():
            if isinstance(child, tk.Toplevel):
                if child.winfo_name() == 'translate_window':
                    child.state("normal")
                else:
                    child.deiconify()

    def minimize_child_windows(self):
        for child in self.app.winfo_children():
            if isinstance(child, tk.Toplevel):
                if child.winfo_name() == 'translate_window':
                    child.state("withdrawn")
                else:
                    child.iconify()

    def select_frame(self):
        if self.state.display['top'] is None:
            answer = tk.messagebox.askquestion(title="Display selection", message="Is display number 1 correct?")
            if answer == 'yes':
                self.update_display('1')
            else:
                return
        self.minimize_child_windows()
        self.app.iconify()
        from toplevel_tks.selectable_frame import SelectableFrame
        self.selectable_frame_window = SelectableFrame(self)