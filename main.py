import customtkinter as ctk
from main_menu_form import MainMenuForm
from global_const import *


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.w = self.winfo_screenwidth()
        self.h = self.winfo_screenheight()
        self.after(0, lambda: self.state('zoomed'))
        self.title("Информационная система для строительного магазина")

        self.__current_form: ctk.CTkFrame = None

        self.__navigation_panel = self.__create_navigation_panel()
        self.main_menu_form = MainMenuForm(self)

        self.__navigation_panel.grid(row=0, column=0)
        self.change_form(self.main_menu_form)

    def change_form(self, new_form: ctk.CTkFrame):
        if self.__current_form is not None:
            self.__current_form.forget()
        self.__current_form = new_form
        new_form.grid(row=0, column=1, columnspan=3, padx=10, pady=10)

    def run(self):
        self.mainloop()

    def __create_navigation_panel(self) -> ctk.CTkFrame:
        font_size = int(CLASSIC_NAVIGATION_PANEL_FONT_SIZE * (self.w / CLASSIC_WINDOW_WIDTH))
        buttons_w = self.w // 4
        buttons_h = (self.h - 65) // 8

        navigation_panel = ctk.CTkFrame(master=self)

        self.__navigation_panel = ctk.CTkFrame(master=self)
        self.__main_menu_button = ctk.CTkButton(
            master=navigation_panel,
            text="ИС",
            font=("Times new roman", font_size + 20),
            width=buttons_w,
            height=buttons_h,
            corner_radius=0,
        )

        self.__nomenclature_button = ctk.CTkButton(
            master=navigation_panel,
            text="Номенклатура",
            font=("Arial", font_size),
            width=buttons_w,
            height=buttons_h,
            corner_radius=0,
        )

        self.__sales_button = ctk.CTkButton(
            master=navigation_panel,
            text="Продажи",
            font=("Arial", font_size),
            width=buttons_w,
            height=buttons_h,
            corner_radius=0,
        )

        self.__purchases_button = ctk.CTkButton(
            master=navigation_panel,
            text="Закупки",
            font=("Arial", font_size),
            width=buttons_w,
            height=buttons_h,
            corner_radius=0,
        )

        self.__write_offs_button = ctk.CTkButton(
            master=navigation_panel,
            text="Списания",
            font=("Arial", font_size),
            width=buttons_w,
            height=buttons_h,
            corner_radius=0,
        )

        self.__suppliers_button = ctk.CTkButton(
            master=navigation_panel,
            text="Поставщики",
            font=("Arial", font_size),
            width=buttons_w,
            height=buttons_h,
            corner_radius=0,
        )

        self.__clients_button = ctk.CTkButton(
            master=navigation_panel,
            text="Клиенты",
            font=("Arial", font_size),
            width=buttons_w,
            height=buttons_h,
            corner_radius=0,
        )

        self.__reports_button = ctk.CTkButton(
            master=navigation_panel,
            text="Отчеты",
            font=("Arial", font_size),
            width=buttons_w,
            height=buttons_h,
            corner_radius=0,
        )

        self.__main_menu_button.grid(row=0, column=0)
        self.__nomenclature_button.grid(row=1, column=0)
        self.__sales_button.grid(row=2, column=0)
        self.__purchases_button.grid(row=3, column=0)
        self.__write_offs_button.grid(row=4, column=0)
        self.__suppliers_button.grid(row=5, column=0)
        self.__clients_button.grid(row=6, column=0)
        self.__reports_button.grid(row=7, column=0)

        return navigation_panel


my_application = Application()
if __name__ == '__main__':
    my_application.run()
