import customtkinter as ctk
from PIL import Image

from Front.main_menu_form import MainMenuForm
from Front.nomenclature_form import NomenclatureForm
from Front.sales_form import SalesForm
from Front.purchases_form import PurchasesForm
from Front.write_offs_form import WriteOffsForm
from Front.suppliers_form import SuppliersForm
from Front.clients_form import ClientsForm
from Front.reports_form import ReportsForm
from Front.global_const import *


class Application(ctk.CTk):
    __CLASSIC_NAVIGATION_PANEL_FONT_SIZE = 30
    __CLASSIC_BUTTON_IMAGE_W = 100
    __CLASSIC_BUTTON_IMAGE_H = 100

    def __init__(self):
        super().__init__()
        self.after(0, lambda: self.state('zoomed'))
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.title("Информационная система для строительного магазина")

        self.__current_form: ctk.CTkFrame = None

        self.__navigation_panel = self.__create_navigation_panel()
        self.__main_menu_form = MainMenuForm(self, self.width, self.height)
        self.__nomenclature_form = NomenclatureForm(self, self.width, self.height)
        self.__purchases_form = PurchasesForm(self, self.width, self.height)
        self.__sales_form = SalesForm(self, self.width, self.height)
        self.__write_offs_form = WriteOffsForm(self, self.width, self.height)
        self.__suppliers_form = SuppliersForm(self, self.width, self.height)
        self.__clients_form = ClientsForm(self, self.width, self.height)
        self.__reports_form = ReportsForm(self, self.width, self.height)

        self.__navigation_panel.grid(row=0, column=0)
        self.change_form(self.__main_menu_form)

    def change_form(self, new_form: ctk.CTkFrame):
        if self.__current_form is not None:
            self.__current_form.grid_forget()
        self.__current_form = new_form
        self.__current_form.grid(row=0, column=1, columnspan=3, padx=10, pady=10, sticky="n")

    def __create_navigation_panel(self) -> ctk.CTkFrame:
        buttons_w = self.width // 4
        buttons_h = (self.height - 65) // 8
        buttons_font_size = round(CLASSIC_HEAD_FONT_SIZE * (self.width / CLASSIC_WINDOW_WIDTH))

        navigation_panel = ctk.CTkFrame(master=self)

        button_image_w = round(self.__CLASSIC_BUTTON_IMAGE_W * (self.width / CLASSIC_WINDOW_WIDTH))
        button_image_h = round(self.__CLASSIC_BUTTON_IMAGE_H * (self.height / CLASSIC_WINDOW_HEIGHT))

        self.__navigation_panel = ctk.CTkFrame(master=self)
        self.__main_menu_button = ctk.CTkButton(
            master=navigation_panel,
            text="",
            width=buttons_w,
            height=buttons_h,
            corner_radius=0,
            command=lambda: self.change_form(self.__main_menu_form),
            image=ctk.CTkImage(light_image=Image.open("images/logo.png"), size=(button_image_w, button_image_h))
        )

        self.__nomenclature_button = ctk.CTkButton(
            master=navigation_panel,
            text="Номенклатура",
            font=("Arial", buttons_font_size),
            width=buttons_w,
            height=buttons_h,
            corner_radius=0,
            command=lambda: self.change_form(self.__nomenclature_form)
        )

        self.__purchases_button = ctk.CTkButton(
            master=navigation_panel,
            text="Поступления",
            font=("Arial", buttons_font_size),
            width=buttons_w,
            height=buttons_h,
            corner_radius=0,
            command=lambda: self.change_form(self.__purchases_form)
        )

        self.__sales_button = ctk.CTkButton(
            master=navigation_panel,
            text="Продажи",
            font=("Arial", buttons_font_size),
            width=buttons_w,
            height=buttons_h,
            corner_radius=0,
            command=lambda: self.change_form(self.__sales_form)
        )

        self.__write_offs_button = ctk.CTkButton(
            master=navigation_panel,
            text="Списания",
            font=("Arial", buttons_font_size),
            width=buttons_w,
            height=buttons_h,
            corner_radius=0,
            command=lambda: self.change_form(self.__write_offs_form)
        )

        self.__suppliers_button = ctk.CTkButton(
            master=navigation_panel,
            text="Поставщики",
            font=("Arial", buttons_font_size),
            width=buttons_w,
            height=buttons_h,
            corner_radius=0,
            command=lambda: self.change_form(self.__suppliers_form)
        )

        self.__clients_button = ctk.CTkButton(
            master=navigation_panel,
            text="Клиенты",
            font=("Arial", buttons_font_size),
            width=buttons_w,
            height=buttons_h,
            corner_radius=0,
            command=lambda: self.change_form(self.__clients_form)
        )

        self.__reports_button = ctk.CTkButton(
            master=navigation_panel,
            text="Отчеты",
            font=("Arial", buttons_font_size),
            width=buttons_w,
            height=buttons_h,
            corner_radius=0,
            command=lambda: self.change_form(self.__reports_form)
        )

        self.__main_menu_button.grid(row=0, column=0)
        self.__nomenclature_button.grid(row=1, column=0)
        self.__purchases_button.grid(row=2, column=0)
        self.__sales_button.grid(row=3, column=0)
        self.__write_offs_button.grid(row=4, column=0)
        self.__suppliers_button.grid(row=5, column=0)
        self.__clients_button.grid(row=6, column=0)
        self.__reports_button.grid(row=7, column=0)

        return navigation_panel

    def run(self):
        self.mainloop()
