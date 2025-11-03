import customtkinter as ctk
from global_const import *


class SettingsForm(ctk.CTkFrame):
    def __init__(self, master, window_w, window_h):
        super().__init__(master=master)

        self.configure(fg_color=master.cget("fg_color"))

        head_font_size = round(CLASSIC_HEAD_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))
        font_size = round(CLASSIC_WIDGETS_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))

        x_padding = round(2 * (window_w / CLASSIC_WINDOW_WIDTH))
        y_padding = round(6 * (window_h / CLASSIC_WINDOW_HEIGHT))

        widgets_w = window_w // 5
        widgets_h = window_h // 20

        self.__organization_name_entry = ctk.CTkEntry(
            master=self,
            width=widgets_w,
            height=widgets_h,
            font=("Arial", font_size)
        )

        self.__organization_inn_entry = ctk.CTkEntry(
            master=self,
            width=widgets_w,
            height=widgets_h,
            font=("Arial", font_size)
        )

        self.__organization_ogrn_entry = ctk.CTkEntry(
            master=self,
            width=widgets_w,
            height=widgets_h,
            font=("Arial", font_size)
        )

        self.__organization_telephone_entry = ctk.CTkEntry(
            master=self,
            width=widgets_w,
            height=widgets_h,
            font=("Arial", font_size)
        )

        self.__organization_address_entry = ctk.CTkEntry(
            master=self,
            width=widgets_w,
            height=widgets_h,
            font=("Arial", font_size)
        )

        self.__save_organization_data_button = ctk.CTkButton(
            master=self,
            text="Сохранить изменения",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
        )

        ctk.CTkLabel(
            master=self,
            text="Настройки",
            font=("Arial", head_font_size),
        ).grid(row=0, column=0, sticky="w", padx=x_padding, pady=y_padding)

        ctk.CTkLabel(
            master=self,
            text="Название организации",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            anchor="sw"
        ).grid(row=1, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__organization_name_entry.grid(row=2, column=0, sticky="w", padx=x_padding, pady=y_padding)

        ctk.CTkLabel(
            master=self,
            text="ИНН",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            anchor="sw"
        ).grid(row=3, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__organization_inn_entry.grid(row=4, column=0, sticky="w", padx=x_padding, pady=y_padding)

        ctk.CTkLabel(
            master=self,
            text="ОГРН",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            anchor="sw"
        ).grid(row=5, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__organization_ogrn_entry.grid(row=6, column=0, sticky="w", padx=x_padding, pady=y_padding)

        ctk.CTkLabel(
            master=self,
            text="Телефон",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            anchor="sw"
        ).grid(row=7, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__organization_telephone_entry.grid(row=8, column=0, sticky="w", padx=x_padding, pady=y_padding)

        ctk.CTkLabel(
            master=self,
            text="Адрес",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            anchor="sw"
        ).grid(row=9, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__organization_address_entry.grid(row=10, column=0, sticky="w", padx=x_padding, pady=y_padding)
        self.__save_organization_data_button.grid(row=11, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__product_types_combobox = ctk.CTkComboBox(
            master=self,
            width=widgets_w,
            height=widgets_h,
            font=("Arial", font_size)
        )

        self.__add_type_button = ctk.CTkButton(
            master=self,
            text="Добавить",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
        )

        self.__del_type_button = ctk.CTkButton(
            master=self,
            text="Удалить",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
        )

        ctk.CTkLabel(
            master=self,
            text="Тип товара",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            anchor="sw"
        ).grid(row=1, column=1, sticky="w", padx=x_padding, pady=y_padding)
        self.__product_types_combobox.grid(row=2, column=1, sticky="w", padx=x_padding, pady=y_padding)
        self.__add_type_button.grid(row=3, column=1, sticky="w", padx=x_padding, pady=y_padding)
        self.__del_type_button.grid(row=4, column=1, sticky="w", padx=x_padding, pady=y_padding)

        self.__product_unit_combobox = ctk.CTkComboBox(
            master=self,
            width=widgets_w,
            height=widgets_h,
            font=("Arial", font_size)
        )

        self.__add_unit_button = ctk.CTkButton(
            master=self,
            text="Добавить",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
        )

        self.__del_unit_button = ctk.CTkButton(
            master=self,
            text="Удалить",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
        )

        ctk.CTkLabel(
            master=self,
            text="Единица измерения",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            anchor="sw"
        ).grid(row=1, column=2, sticky="w", padx=x_padding, pady=y_padding)
        self.__product_unit_combobox.grid(row=2, column=2, sticky="w", padx=x_padding, pady=y_padding)
        self.__add_unit_button.grid(row=3, column=2, sticky="w", padx=x_padding, pady=y_padding)
        self.__del_unit_button.grid(row=4, column=2, sticky="w", padx=x_padding, pady=y_padding)
