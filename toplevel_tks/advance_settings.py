
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

        self.app.geometry(f"{self.width}x{self.height}")
        self.app.transient(self.mainTk.app)

        self.tabview = ck.CTkTabview(self.app)

        # Create the "Settings" tab
        self.settings_tab = self.tabview.add("Settings")

        # Add widgets to the "Settings" tab
        self.ocr_label = ck.CTkLabel(self.settings_tab, text="OCR interval in ms (250 default)")
        self.ocr_interval = ck.StringVar(value=self.mainTk.state.ocr_interval)
        self.ocr_interval_entry = ck.CTkEntry(self.settings_tab, textvariable=self.ocr_interval)
        self.timeout_label = ck.CTkLabel(self.settings_tab, text="Translation Timeout")
        self.translate_timeout = ck.StringVar(value=self.mainTk.state.translate_timeout)
        self.timeout_entry = ck.CTkEntry(self.settings_tab, textvariable=self.translate_timeout)
        self.log_level_label = ck.CTkLabel(self.settings_tab, text="Log Level")
        self.log_level_combo = ck.CTkComboBox(self.settings_tab, values=list(self.log_levels.keys()), state="readonly")
        self.log_level_combo.set(self.mainTk.state.log_level)
        self.debug_mode_label = ck.CTkLabel(self.settings_tab, text="Debug Mode")
        self.debug_mode = ck.StringVar(value=self.mainTk.state.debug_mode)
        self.checkbox_debug_mode = ck.CTkCheckBox(self.settings_tab, text="Debug mode",
                                     variable=self.debug_mode, onvalue="on", offvalue="off")
        self.save_button = ck.CTkButton(self.settings_tab, text="Save", command=self.save)

        # Layout using grid geometry manager in the "Settings" tab
        self.ocr_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.ocr_interval_entry.grid(row=0, column=1, padx=10, pady=10)
        self.timeout_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.timeout_entry.grid(row=1, column=1, padx=10, pady=10)
        self.log_level_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.log_level_combo.grid(row=2, column=1, padx=10, pady=10)
        self.debug_mode_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.checkbox_debug_mode.grid(row=3, column=1, padx=10, pady=10)
        self.save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Create the "Preferences" tab
        preferences_tab = self.tabview.add("Preferences")

        # Add widgets to the "Preferences" tab
        self.theme_label = ck.CTkLabel(preferences_tab, text="Theme")
        self.theme_combo = ck.CTkComboBox(preferences_tab, values=['System', 'Dark', 'Light'], state="readonly")
        self.theme_combo.set(self.mainTk.state.theme)
        self.opacity_label = ck.CTkLabel(preferences_tab, text="Text Window Opacity")
        self.opacity_slider = ck.CTkSlider(preferences_tab, from_=0, to=100, command=self.on_opacity_change)
        self.preferences_save_button = ck.CTkButton(preferences_tab, text="Save", command=self.save)

        # Layout using grid geometry manager in the "Preferences" tab
        self.theme_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.theme_combo.grid(row=0, column=1, padx=10, pady=10)
        self.opacity_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.opacity_slider.grid(row=1, column=1, padx=10, pady=10)
        self.preferences_save_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Pack and display the tabview
        self.tabview.pack(pady=20, padx=20)

    def on_opacity_change(self, event):
        self.mainTk.update_text_win_opacity(self.opacity_slider.get())
        
    def save(self):
        self.mainTk.state.ocr_interval = self.ocr_interval_entry.get()
        self.mainTk.state.translate_timeout = self.timeout_entry.get()
        self.mainTk.state.debug_mode = self.debug_mode.get()
        self.mainTk.state.log_level = self.log_level_combo.get()
        self.mainTk.state.theme = self.theme_combo.get()
        self.mainTk.state.text_opacity = self.opacity_slider.get() / 100
        self.mainTk.state.saveState()
        self.mainTk.update_log_level()
        self.mainTk.open_debug_group()
        self.mainTk.update_theme()
        self.app.destroy()