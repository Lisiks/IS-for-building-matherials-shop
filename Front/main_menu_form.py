import customtkinter as ctk


class MainMenuForm(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(master=self, text="Форма главного меню").pack()



