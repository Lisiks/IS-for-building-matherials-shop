import customtkinter as ctk


class SuppliersForm(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(master=self, text="Форма поставщиков").pack()



