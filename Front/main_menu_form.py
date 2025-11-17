import customtkinter as ctk
import Back.backend_for_main_menu as back
import mysql.connector.errors
from Front.global_const import *
from Front.settings_form import SettingsForm
from Front.dialog_window import InformationDialog
from os import listdir
from PIL import Image




class MainMenuForm(ctk.CTkFrame):
    def __init__(self, master, window_w, window_h):
        super().__init__(master)
        self.configure(fg_color=master.cget("fg_color"))

        head_font_size = round(CLASSIC_HEAD_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))
        font_size = round(CLASSIC_WIDGETS_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))

        x_padding = 3
        y_padding = 6

        self.__application_window = master

        ctk.CTkLabel(
            master=self,
            text="Главная",
            font=("Arial", head_font_size)
        ).grid(row=0, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__info_label_frame = ctk.CTkFrame(master=self, fg_color=master.cget("fg_color"))

        self.__company_name_label = ctk.CTkLabel(
            master=self.__info_label_frame,
            text="Наименование компании:",
            font=("Arial", font_size)
        )
        self.__company_name_label.grid(row=1, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__month_sales_label = ctk.CTkLabel(
            master=self.__info_label_frame,
            text="Продаж в текущем месяце:",
            font=("Arial", font_size)
        )
        self.__month_sales_label.grid(row=2, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__month_purchases_label = ctk.CTkLabel(
            master=self.__info_label_frame,
            text="Закупок в текущем месяце:",
            font=("Arial", font_size)
        )
        self.__month_purchases_label.grid(row=3, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__info_label_frame.grid(row=1, column=0, sticky="wn", padx=x_padding, pady=y_padding)

        self.__logo_image_size = window_w // 2 - 100
        self.__company_logo_label = ctk.CTkLabel(
            master=self,
            width=self.__logo_image_size,
            height=self.__logo_image_size,
            text=""
        )
        self.__company_logo_label.grid(row=1, column=1, sticky="e", padx=x_padding, pady=y_padding)

        self.__settings_form = SettingsForm(master, window_w, window_h)
        self.__settings_button = ctk.CTkButton(
            master=self,
            text="Настройки",
            width=window_w // 4,
            height=window_h // 20,
            font=("Arial", font_size),
            command=lambda: self.__application_window.change_form(self.__settings_form)
        )

        self.__settings_button.grid(row=4, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__change_logo_button = ctk.CTkButton(
            master=self,
            text="Загрузить логотип",
            width=window_w // 4,
            height=window_h // 20,
            font=("Arial", font_size),
            command=self.__change_company_logo
        )

        self.__change_logo_button.grid(row=4, column=1, sticky="e", padx=x_padding, pady=y_padding)

        self.bind("<Map>", self.__on_form_show_action)

    def __on_form_show_action(self, _):
        organization_name_label_text = "Наименование компании: "
        month_sales_count = "Продаж в текущем месяце: "
        month_purchases_count = "Закупок в текущем месяце: "
        try:
            organization_name_label_text += str(back.get_organization_name())
        except FileNotFoundError:
            InformationDialog(
                self.master,
                "Ошибка чтения файла!",
                "Файл 'organization_data.json' был поврежден\n перемещен или утерян!"
            )
        try:
            purchases_count, sales_count = back.get_month_purchases_sales_count()
            month_sales_count += str(sales_count)
            month_purchases_count += str(purchases_count)
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

        self.__company_name_label.configure(text=organization_name_label_text)
        self.__month_sales_label.configure(text=month_sales_count)
        self.__month_purchases_label.configure(text=month_purchases_count)
        self.__load_company_logo()

    def __load_company_logo(self):
        logo_file_name = "images/logo.png"
        for file_name in listdir("images"):
            if "company_logo" in file_name:
                logo_file_name = f"images/{file_name}"
                break
        company_logo_image = ctk.CTkImage(light_image=Image.open(logo_file_name), size=(self.__logo_image_size, self.__logo_image_size))
        self.__company_logo_label.configure(image=company_logo_image)

    def __change_company_logo(self):
        try:
            back.get_company_logo()
        except TypeError:
            InformationDialog(
                main=self,
                tittle="Некорректный формат файла!",
                information="Допустимые форматы: png, jpg, bmp."
            )
        self.__load_company_logo()



