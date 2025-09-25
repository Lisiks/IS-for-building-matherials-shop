import customtkinter as ctk


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.w = self.winfo_screenwidth()
        self.h = self.winfo_screenheight()
        self.after(0, lambda: self.state('zoomed'))
        self.title("Информационная система для строительного магазина")

    def run(self):
        self.mainloop()


my_application = Application()
if __name__ == '__main__':
    my_application.run()
