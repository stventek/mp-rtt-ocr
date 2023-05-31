import customtkinter as ct

class LogsFrame(ct.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ct.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.label_logs = ct.CTkLabel(master=self, text="Logs", font=("Arial", 24))
        self.label_logs.pack(pady=(20,5), padx=10)

        self.textbox_logs = ct.CTkTextbox(master=self)
        self.textbox_logs.pack(pady=15, padx=20,  fill="both", expand=True)
