import customtkinter as ck

theme = ck.ThemeManager()

class CustomLabelFrame(ck.CTkFrame):

    def __init__(self, master, text, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.frame_group = ck.CTkFrame(master=self)
        self.label = ck.CTkLabel(self, text=text, height=0)
        self.label.pack()
        self.frame_group.pack(fill="both", expand=True)
