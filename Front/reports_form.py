import customtkinter as ctk
import mysql.connector.errors
from Front.report_result_form import RepostResultForm
from Front.global_const import *
from Back.query_for_comboboxes_values import get_products_articles
from Front.dialog_window import InformationDialog
from Back.Reports import (products_sales, products_purchases, types_sales, product_buying_price_graphics,
                          types_purchases, clients_sales, suppliers_purchases, product_selling_price_graphics)
from matplotlib import pyplot
from matplotlib.widgets import Button as PlotButton
import threading


class ReportsForm(ctk.CTkFrame):
    def __init__(self, master, window_w, window_h):
        super().__init__(master)
        self.configure(fg_color=master.cget("fg_color"))

        self.__application_window = master

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
            command=self.__make_sale_report
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
            command=self.__make_purchase_report
        )

        self._purchasing_report_create_button.grid(row=6, column=1, padx=x_padding, pady=y_padding)

        self.__button_for_show_report_result = ctk.CTkButton(
            master=self,
            text="Последний сформированный отчет",
            font=("Arial", font_size),
            width=window_w // 3 * 2,
            height=window_h // 20,
            command=self.__open_current_result_form
        )
        self.__button_for_show_report_result.grid(row=7, column=0, columnspan=2, padx=x_padding, pady=y_padding)

        ctk.CTkLabel(
            master=self,
            text="Динамика цен закупки",
            font=("Arial", font_size)
        ).grid(row=8, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__article_for_purchasing_price_report = ctk.CTkComboBox(
            master=self,
            width=window_w // 3,
            height=window_h // 20,
            font=("Arial", font_size),
            command=self.__purchases_article_cb_format
        )

        self.__article_for_purchasing_price_report.grid(row=9, column=0, padx=x_padding, pady=y_padding)

        self.__purchasing_price_report_create_button = ctk.CTkButton(
            master=self,
            text="Сформировать",
            font=("Arial", font_size),
            width=window_w // 3,
            height=window_h // 20,
            command=self.__make_product_buying_price_report
        )

        self.__purchasing_price_report_create_button.grid(row=10, column=0, padx=x_padding, pady=y_padding)

        ctk.CTkLabel(
            master=self,
            text="Динамика цен продажи",
            font=("Arial", font_size)
        ).grid(row=8, column=1, sticky="w", padx=x_padding, pady=y_padding)

        self.__article_for_selling_price_report = ctk.CTkComboBox(
            master=self,
            width=window_w // 3,
            height=window_h // 20,
            font=("Arial", font_size),
            command=self.__selling_article_cb_format
        )

        self.__article_for_selling_price_report.grid(row=9, column=1, padx=x_padding, pady=y_padding)

        self.__selling_price_report_create_button = ctk.CTkButton(
            master=self,
            text="Сформировать",
            font=("Arial", font_size),
            width=window_w // 3,
            height=window_h // 20,
            command=self.__make_product_selling_price_report
        )

        self.__selling_price_report_create_button.grid(row=10, column=1, padx=x_padding, pady=y_padding)



        self.bind("<Map>", self.__on_form_show_actions)

        self.__report_result_form = None

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

    def __open_current_result_form(self):
        if self.__report_result_form is None:
            InformationDialog(
                self,
                "Ошибка",
                "За текущий сеанс не было сформировано\nни одного отчета!")
        else:
            self.__application_window.change_form(self.__report_result_form)

    def __make_product_purchase_report(self, period):
        try:
            report_data = products_purchases.make_product_purchases_reposts(period)
            self.__report_result_form.load_report_data(report_data)
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

    def __make_type_purchase_report(self, period):
        try:
            report_data = types_purchases.make_type_purchases_reposts(period)
            self.__report_result_form.load_report_data(report_data)
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

    def __make_supplier_purchase_report(self, period):
        try:
            report_data = suppliers_purchases.make_suppliers_purchases_reposts(period)
            self.__report_result_form.load_report_data(report_data)
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

    def __make_purchase_report(self):
        thread_names = [thr.name for thr in threading.enumerate()]
        if "report_thread" in thread_names:
            InformationDialog(
                self,
                "Внимание",
                "Формирование данного отчета невозможно,\nт.к в данный момент идет формирование другого отчета!")
            return 0

        period = self.__period_entry.get()
        if period == "":
            InformationDialog(
                self,
                "Ошибка ввода",
                "Для формирования отчета необходимо указать период!")
            return 0

        report_type = self.__purchasing_type_entry.get()
        if report_type == "":
            InformationDialog(
                self,
                "Ошибка ввода",
                "Для формирования отчета необходимо указать его тип!")
            return 0

        if report_type == "По товарам":
            self.__report_result_form = RepostResultForm(
                master=self.master,
                window_w=self.master.winfo_screenwidth(),
                window_h=self.master.winfo_screenheight(),
                report_header=f"Отчет по закупкам (по товарам) за {period.lower()}",
                table_headers=["Артикул", "Наименование", "Объем закупки", "Стоимость закупки"])

            report_thread = threading.Thread(name="report_thread",target=self.__make_product_purchase_report, args=(period,), daemon=True)
        elif report_type == "По типу товаров":
            self.__report_result_form = RepostResultForm(
                master=self.master,
                window_w=self.master.winfo_screenwidth(),
                window_h=self.master.winfo_screenheight(),
                report_header=f"Отчет по закупкам (по типу) за {period.lower()}",
                table_headers=["Тип", "Объем закупки", "Стоимость закупки"])
            report_thread = threading.Thread(name="report_thread", target=self.__make_type_purchase_report,args=(period,), daemon=True)

        else:
            self.__report_result_form = RepostResultForm(
                master=self.master,
                window_w=self.master.winfo_screenwidth(),
                window_h=self.master.winfo_screenheight(),
                report_header=f"Отчет по закупкам (по поставщикам) за {period.lower()}",
                table_headers=["ИНН", "Наименование", "Объем закупки", "Стоимость закупки"])
            report_thread = threading.Thread(name="report_thread", target=self.__make_supplier_purchase_report,args=(period,), daemon=True)

        self.__application_window.change_form(self.__report_result_form)

        InformationDialog(
            self.master,
            "Создание отчета",
            "Процесс создания запущен, дождитесь его окончания,\nлибо перейдите в 'Последний сформированный отчет'\nраздела 'Отчеты' позже.")

        report_thread.start()

    def __make_product_sales_report(self, period):
        try:
            report_data = products_sales.make_product_sales_reposts(period)
            self.__report_result_form.load_report_data(report_data)
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

    def __make_type_sales_report(self, period):
        try:
            report_data = types_sales.make_type_sales_reposts(period)
            self.__report_result_form.load_report_data(report_data)
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

    def __make_client_sales_report(self, period):
        try:
            report_data = clients_sales.make_client_sales_reposts(period)
            self.__report_result_form.load_report_data(report_data)
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

    def __make_sale_report(self):
        thread_names = [thr.name for thr in threading.enumerate()]
        if "report_thread" in thread_names:
            InformationDialog(
                self,
                "Внимание",
                "Формирование данного отчета невозможно,\nт.к в данный момент идет формирование другого отчета!")
            return 0

        period = self.__period_entry.get()
        if period == "":
            InformationDialog(
                self,
                "Ошибка ввода",
                "Для формирования отчета необходимо указать период!")
            return 0

        report_type = self.__seller_type_entry.get()
        if report_type == "":
            InformationDialog(
                self,
                "Ошибка ввода",
                "Для формирования отчета необходимо указать его тип!")
            return 0

        if report_type == "По товарам":
            self.__report_result_form = RepostResultForm(
                master=self.master,
                window_w=self.master.winfo_screenwidth(),
                window_h=self.master.winfo_screenheight(),
                report_header=f"Отчет по продажам (по товарам) за {period.lower()}",
                table_headers=["Артикул", "Наименование", "Объем продажи", "Выручка", "Прибыль"])
            report_thread = threading.Thread(name="report_thread",target=self.__make_product_sales_report, args=(period,), daemon=True)

        elif report_type == "По типу товаров":
            self.__report_result_form = RepostResultForm(
                master=self.master,
                window_w=self.master.winfo_screenwidth(),
                window_h=self.master.winfo_screenheight(),
                report_header=f"Отчет по продажам (по типу) за {period.lower()}",
                table_headers=["Тип", "Объем продажи", "Выручка", "Прибыль"])
            report_thread = threading.Thread(name="report_thread", target=self.__make_type_sales_report, args=(period,), daemon=True)

        else:
            self.__report_result_form = RepostResultForm(
                master=self.master,
                window_w=self.master.winfo_screenwidth(),
                window_h=self.master.winfo_screenheight(),
                report_header=f"Отчет по продажам (по клиентам) за {period.lower()}",
                table_headers=["№ дисконтной карты", "Клиент", "Объем продажи", "Выручка", "Прибыль"])
            report_thread = threading.Thread(name="report_thread", target=self.__make_client_sales_report,args=(period,), daemon=True)

        self.__application_window.change_form(self.__report_result_form)

        InformationDialog(
            self.master,
            "Создание отчета",
            "Процесс создания запущен, дождитесь его окончания,\nлибо перейдите в 'Последний сформированный отчет'\nраздела 'Отчеты' позже.")

        report_thread.start()

    def __make_product_buying_price_report(self):
        period = self.__period_entry.get()
        if period == "":
            InformationDialog(
                self,
                "Ошибка ввода",
                "Для формирования отчета необходимо указать период!")
            return 0

        article = self.__article_for_purchasing_price_report.get()
        if article == "":
            InformationDialog(
                self,
                "Ошибка ввода",
                "Для формирования отчета необходимо указать артикул товара!")
            return 0

        try:
            date_list, price_list = product_buying_price_graphics.make_product_buying_price_report(period, article)
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")
            return 0
        except TypeError:
            InformationDialog(
                self.master,
                "Ошибка ввода!",
                "Товар с данным артикулом отсутствует в БД!")
            return 0

        if len(date_list) == 0:
            InformationDialog(
                self.master,
                "Результат отчета!",
                "За указанный период не было совершено\nни одного изменения цены данного товара.")
            return 0

        current_figure = pyplot.figure(
            num=f"Динамика цены закупки товара '{article}' за {period.lower()}",
        )

        pyplot.title(f"Динамика цены закупки товара '{article}' за {period.lower()}")
        pyplot.xlabel("Дата изменения")
        pyplot.ylabel("Цена товара")

        pyplot.plot(date_list, price_list, "--o")

        if len(date_list) > 15:
            pyplot.tick_params(axis='x', labelbottom=False)

        button_place = pyplot.axes([0.01, 0.01, 0.2, 0.05])
        pyplot_button = PlotButton(button_place, 'Выход', color='#0D95E8', hovercolor='#00B2FF')
        pyplot_button.on_clicked(lambda event: pyplot.close(pyplot.close(current_figure)))

        pyplot.get_current_fig_manager().full_screen_toggle()
        pyplot.show()

    def __make_product_selling_price_report(self):
        period = self.__period_entry.get()
        if period == "":
            InformationDialog(
                self,
                "Ошибка ввода",
                "Для формирования отчета необходимо указать период!")
            return 0

        article = self.__article_for_selling_price_report.get()
        if article == "":
            InformationDialog(
                self,
                "Ошибка ввода",
                "Для формирования отчета необходимо указать артикул товара!")
            return 0

        try:
            date_list, price_list = product_selling_price_graphics.make_product_selling_price_report(period, article)
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")
            return 0
        except TypeError:
            InformationDialog(
                self.master,
                "Ошибка ввода!",
                "Товар с данным артикулом отсутствует в БД!")
            return 0

        if len(date_list) == 0:
            InformationDialog(
                self.master,
                "Результат отчета!",
                "За указанный период не было совершено\nни одного изменения цены данного товара.")
            return 0

        current_figure = pyplot.figure(
            num=f"Динамика цены продажи товара '{article}' за {period.lower()}",
        )

        pyplot.title(f"Динамика цены продажи товара '{article}' за {period.lower()}")
        pyplot.xlabel("Дата изменения")
        pyplot.ylabel("Цена товара")

        pyplot.plot(date_list, price_list, "--o")

        if len(date_list) > 15:
            pyplot.tick_params(axis='x', labelbottom=False)

        button_place = pyplot.axes([0.01, 0.01, 0.2, 0.05])
        pyplot_button = PlotButton(button_place, 'Выход', color='#0D95E8', hovercolor='#00B2FF')
        pyplot_button.on_clicked(lambda event: pyplot.close(pyplot.close(current_figure)))

        pyplot.get_current_fig_manager().full_screen_toggle()
        pyplot.show()















