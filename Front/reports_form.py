import customtkinter as ctk
import threading
import mysql.connector.errors
from Front.report_result_form import RepostResultForm
from Front.global_const import *
from Back.query_for_comboboxes_values import get_products_articles
from Front.dialog_window import InformationDialog
from Back.Reports import purchases_reports, sales_reports, product_price_reports

from matplotlib import pyplot
from matplotlib.widgets import Button as PlotButton
import mplcursors


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
            command=lambda: self.__make_report(report_kind="sales")
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
            command=lambda: self.__make_report(report_kind="purchases")
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
            command=lambda: self.__make_product_price_report("buy_price_type")
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
            command=lambda: self.__make_product_price_report("sel_price_type")
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

    def __thread_report_function(self, report_function, period):
        try:
            report_data = report_function(period)
            self.__report_result_form.load_report_data(report_data)
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

    def __make_report(self, report_kind):
        thread_names = [thr.name for thr in threading.enumerate()]
        if "report_thread" in thread_names:
            InformationDialog(
                self,
                "Внимание",
                "Формирование данного отчета невозможно,\nт.к в данный момент идет формирование другого отчета!")
            return 0

        period = self.__period_entry.get()
        if period == "":
            InformationDialog(self,"Ошибка ввода","Для формирования отчета необходимо указать период!")
            return 0

        report_type = self.__purchasing_type_entry.get() if report_kind == "purchases" else self.__seller_type_entry.get()
        if report_type == "":
            InformationDialog(self,"Ошибка ввода","Для формирования отчета необходимо указать его тип!")
            return 0


        if report_type == "По товарам" and report_kind == "purchases":
            report_headers = f"Отчет по закупкам (по товарам) за {period.lower()}"
            report_table_headers = ["Артикул", "Наименование", "Объем закупки", "Стоимость закупки"]
            report_function = purchases_reports.make_product_purchases_report
        elif report_type == "По типу товаров" and report_kind == "purchases":
            report_headers = f"Отчет по закупкам (по типу) за {period.lower()}"
            report_table_headers = ["Тип", "Объем закупки", "Стоимость закупки"]
            report_function = purchases_reports.make_type_purchases_report
        elif report_type == "По поставщикам" and report_kind == "purchases":
            report_headers = f"Отчет по закупкам (по поставщикам) за {period.lower()}"
            report_table_headers = ["ИНН", "Наименование", "Объем закупки", "Стоимость закупки"]
            report_function = purchases_reports.make_suppliers_purchases_report
        elif report_type == "По товарам" and report_kind == "sales":
            report_headers = f"Отчет по продажам (по товарам) за {period.lower()}"
            report_table_headers = ["Артикул", "Наименование", "Объем продаж", "Выручка c учетом\ncкидок", "Прибыль с продажи"]
            report_function = sales_reports.make_product_sales_report
        elif report_type == "По типу товаров" and report_kind == "sales":
            report_headers = f"Отчет по продажам (по типу) за {period.lower()}"
            report_table_headers = ["Тип", "Объем продаж", "Выручка c учетом\ncкидок", "Прибыль с продажи"]
            report_function = sales_reports.make_type_sales_report
        else:
            report_headers = f"Отчет по продажам (по клиентам) за {period.lower()}"
            report_table_headers = ["№ дисконтной карты", "Клиент", "Объем продаж", "Выручка c учетом\ncкидок", "Прибыль с продажи"]
            report_function = sales_reports.make_client_sales_report

        self.__report_result_form = RepostResultForm(
            master=self.master,
            window_w=self.master.winfo_screenwidth(),
            window_h=self.master.winfo_screenheight(),
            report_header=report_headers,
            table_headers=report_table_headers
        )
        report_thread = threading.Thread(
            name="report_thread",
            target=self.__thread_report_function,
            args=(report_function, period),
            daemon=True
        )
        self.__application_window.change_form(self.__report_result_form)
        InformationDialog(
            self.master,
            "Создание отчета",
            "Процесс создания запущен, дождитесь его окончания,\nлибо перейдите в 'Последний сформированный отчет'\nраздела 'Отчеты' позже.")

        report_thread.start()

    def __make_product_price_report(self, report_type):
        def cursor_event(sel):
            nonlocal date_list, price_list
            x, y = sel.target

            current_date = date_list[int(x)].replace("\n", " ")
            current_price = price_list[int(x)]

            annotation_price = "-" if y != current_price else str(current_price)
            sel.annotation.set_text(f"Дата изменения: {current_date}\nНовая цена: {annotation_price}")


        period = self.__period_entry.get()
        if period == "":
            InformationDialog(self, "Ошибка ввода", "Для формирования отчета необходимо указать период!")
            return 0

        article = self.__article_for_selling_price_report.get() if report_type == "sel_price_type" else self.__article_for_purchasing_price_report.get()
        if article == "":
            InformationDialog(self, "Ошибка ввода", "Для формирования отчета необходимо указать артикул товара!")
            return 0

        try:
            if report_type == "sel_price_type":
                product_name, date_list, price_list = product_price_reports.make_product_selling_price_report(period, article)
            else:
                product_name, date_list, price_list = product_price_reports.make_product_buying_price_report(period, article)

        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,"Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")
            return 0
        except TypeError:
            InformationDialog(self.master,"Ошибка ввода!","Товар с данным артикулом отсутствует в БД!")
            return 0

        if len(date_list) == 0:
            InformationDialog(
                self.master,
                "Результат отчета!",
                "За указанный период не было совершено\nни одного изменения цены данного товара.")
            return 0

        graph_header = "Динамика цены продажи товара" if report_type == "sel_price_type" else "Динамика цены закупки товара"
        current_figure = pyplot.figure(
            num=f"{graph_header} '{article}' за {period.lower()}",
        )


        pyplot.title(f"{graph_header}: {product_name} (артикул:{article}) - за {period.lower()}")
        pyplot.xlabel("Дата изменения")
        pyplot.ylabel("Цена товара")

        pyplot.plot(date_list, price_list, "--o")

        if len(date_list) > 15:
            pyplot.tick_params(axis='x', labelbottom=False)

        button_place = pyplot.axes([0.01, 0.01, 0.2, 0.05])
        pyplot_button = PlotButton(button_place, 'Закрыть отчет', color='#E3E3E3', hovercolor='#F0F0F0')
        pyplot_button.on_clicked(lambda event: pyplot.close(current_figure))
        pyplot.get_current_fig_manager().full_screen_toggle()

        cursor = mplcursors.cursor(hover=True)
        cursor.connect("add", cursor_event)


        pyplot.show()


