import customtkinter as ctk
import mysql.connector.errors
from Front.global_const import *
from Back.query_for_comboboxes_values import get_products_articles
from Front.dialog_window import InformationDialog


class ReportsForm(ctk.CTkFrame):
    def __init__(self, master, window_w, window_h):
        super().__init__(master)
        self.configure(fg_color=master.cget("fg_color"))

        head_font_size = round(CLASSIC_HEAD_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))
        font_size = round(CLASSIC_WIDGETS_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))

        x_padding = 3
        y_padding = 6

        ctk.CTkLabel(
            master=self,
            text="Отчеты",
            font=("Arial", head_font_size)
        ).grid(row=0, column=0, sticky="w", padx=x_padding, pady=y_padding)

        ctk.CTkLabel(
            master=self,
            text="Период отчета",
            font=("Arial", font_size + 3)
        ).grid(row=1, column=0, sticky="w",padx=x_padding, pady=y_padding)

        self.__period_entry = ctk.CTkComboBox(
            master=self,
            width=window_w // 3,
            height=window_h // 20,
            font=("Arial", font_size),
            values=["Месяц", "Год", "Все время"],
            state="readonly",
        )

        self.__period_entry.grid(row=2, column=0, padx=x_padding, pady=y_padding)

        ctk.CTkLabel(
            master=self,
            text="Тип отчета",
            font=("Arial", font_size + 3)
        ).grid(row=3, column=0, sticky="w", padx=x_padding, pady=y_padding)

        ctk.CTkLabel(
            master=self,
            text="Продажи",
            font=("Arial", font_size)
        ).grid(row=4, column=0, sticky="w", padx=x_padding, pady=y_padding)

        ctk.CTkLabel(
            master=self,
            text="Поступления",
            font=("Arial", font_size)
        ).grid(row=4, column=1, sticky="w", padx=x_padding, pady=y_padding)

        self.__seller_type_entry = ctk.CTkComboBox(
            master=self,
            width=window_w // 3,
            height=window_h // 20,
            font=("Arial", font_size),
            values=["По товарам", "По типу товаров", "По клиентам"],
            state="readonly",
        )

        self.__seller_type_entry.grid(row=5, column=0, padx=x_padding, pady=y_padding)

        self._sellers_report_create_button = ctk.CTkButton(
            master=self,
            text="Сформировать",
            font=("Arial", font_size),
            width=window_w // 3,
            height=window_h // 20,
        )

        self._sellers_report_create_button.grid(row=6, column=0, padx=x_padding, pady=y_padding)


        self.__purchasing_type_entry = ctk.CTkComboBox(
            master=self,
            width=window_w // 3,
            height=window_h // 20,
            font=("Arial", font_size),
            values=["По товарам", "По типу товаров", "По поставщикам"],
            state="readonly",
        )

        self.__purchasing_type_entry.grid(row=5, column=1, padx=x_padding, pady=y_padding)

        self._purchasing_report_create_button = ctk.CTkButton(
            master=self,
            text="Сформировать",
            font=("Arial", font_size),
            width=window_w // 3,
            height=window_h // 20,
        )

        self._purchasing_report_create_button.grid(row=6, column=1, padx=x_padding, pady=y_padding)

        ctk.CTkLabel(
            master=self,
            text="Динамика цен закупки",
            font=("Arial", font_size)
        ).grid(row=7, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__article_for_purchasing_price_report = ctk.CTkComboBox(
            master=self,
            width=window_w // 3,
            height=window_h // 20,
            font=("Arial", font_size),
            command=self.__purchases_article_cb_format
        )

        self.__article_for_purchasing_price_report.grid(row=8, column=0, padx=x_padding, pady=y_padding)

        self.__purchasing_price_report_create_button = ctk.CTkButton(
            master=self,
            text="Сформировать",
            font=("Arial", font_size),
            width=window_w // 3,
            height=window_h // 20,
        )

        self.__purchasing_price_report_create_button.grid(row=9, column=0, padx=x_padding, pady=y_padding)

        ctk.CTkLabel(
            master=self,
            text="Динамика цен продажи",
            font=("Arial", font_size)
        ).grid(row=7, column=1, sticky="w", padx=x_padding, pady=y_padding)

        self.__article_for_selling_price_report = ctk.CTkComboBox(
            master=self,
            width=window_w // 3,
            height=window_h // 20,
            font=("Arial", font_size),
            command=self.__selling_article_cb_format
        )

        self.__article_for_selling_price_report.grid(row=8, column=1, padx=x_padding, pady=y_padding)

        self.__selling_price_report_create_button = ctk.CTkButton(
            master=self,
            text="Сформировать",
            font=("Arial", font_size),
            width=window_w // 3,
            height=window_h // 20,
        )

        self.__selling_price_report_create_button.grid(row=9, column=1, padx=x_padding, pady=y_padding)
        self.bind("<Map>", self.__on_form_show_actions)

    def __on_form_show_actions(self, _):
        self.__period_entry.set("")
        self.__seller_type_entry.set("")
        self.__purchasing_type_entry.set("")

        self.__article_for_selling_price_report.set("")
        self.__article_for_purchasing_price_report.set("")

        articles = list()
        try:
            articles = get_products_articles()
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")
        self.__article_for_purchasing_price_report.configure(values=articles)
        self.__article_for_selling_price_report.configure(values=articles)

    def __selling_article_cb_format(self, cb_choice):
        self.__article_for_selling_price_report.set(cb_choice[:cb_choice.index(" ")])

    def __purchases_article_cb_format(self, cb_choice):
        self.__article_for_purchasing_price_report.set(cb_choice[:cb_choice.index(" ")])





