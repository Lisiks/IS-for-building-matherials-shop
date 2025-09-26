import customtkinter as ctk


class WriteOffsForm(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(master=self, text="Форма списаний").pack()



