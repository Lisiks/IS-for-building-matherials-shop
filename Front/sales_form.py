import customtkinter as ctk
import mysql.connector.errors
import Back.backend_for_sales as back
from tksheet import Sheet
from Front.global_const import *
from Back.query_for_comboboxes_values import get_products_articles, get_client_cards
from Front.dialog_window import InformationDialog, ModalDialog
from datetime import datetime




class SalesForm(ctk.CTkFrame):
    def __init__(self, master, window_w, window_h):
        super().__init__(master)
        self.configure(fg_color=master.cget("fg_color"))

        table_width = window_w - (window_w // 4) - 60
        table_height = window_h - (window_h // 2.7) - 60

        self.__table_column_width = int(table_width // 4)
        table_row_height = int(table_height // 7)

        head_font_size = round(CLASSIC_HEAD_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))
        font_size = round(CLASSIC_WIDGETS_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))
        table_font_size = (round(CLASSIC_TABLE_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH)))

        self.__found_frame = self.__create_found_frame(
            button_w=table_width // 6,
            button_h=window_h // 20,
            entry_w=table_width // 6 * 5,
            entry_h=window_h // 20,
            font_size=font_size
        )

        self.__creating_frame = self.__create_creation_frame(
            client_entry_w=self.__table_column_width * 2,
            article_entry_w=self.__table_column_width,
            count_entry_w=self.__table_column_width,
            entryes_h=window_h // 20,
            font_size=font_size,
        )

        self.__crud_frame = self.__create_crud_frame(
            button_w=table_width // 3 - 20,
            button_h=window_h // 20,
            font_size=font_size
        )

        self.__table_frame = ctk.CTkFrame(master=self, fg_color="#313131", corner_radius=10)

        self.__sales_table = Sheet(
            self.__table_frame,
            show_x_scrollbar=False,
            show_y_scrollbar=False,

            width=table_width,
            height=table_height,
            header_height=table_row_height,
            row_height=table_row_height,

            header_align="c",
            align="c",

            header_bg="#313131",
            header_selected_cells_bg="#313131",
            table_bg="#404040",

            header_font=("Arial", table_font_size, "bold"),
            header_selected_cells_fg="white",
            header_fg="white",

            font=("Arial", table_font_size, "normal"),
            table_fg="white",

            table_grid_fg="#313131",
            header_grid_fg="#313131",

            table_selected_rows_bg="#1E6AC4",
            table_selected_rows_border_fg="#1E6AC4",
            table_selected_rows_fg="white",

            show_row_index=False,
            show_top_left=False,

            empty_vertical=False,
            empty_horizontal=False
        )

        self.__sales_table.headers(
            [
                "ID",
                "Дата и время операции",
                "Дисконтная карта клиента",
                "Артикул товара",
                "Кол-во",
            ]
        )

        self.__sales_table.extra_bindings("cell_select", self.__table_row_selection)
        self.__sales_table.enable_bindings("single_select")
        self.__sales_table.hide_columns(columns=0)

        ctk.CTkLabel(
            master=self.__table_frame,
            text="Все операции",
            font=("Arial", font_size + 3),
            anchor="center",
            text_color="white"
        ).grid(row=0, column=0, padx=2)

        self.__sales_table.grid(row=1, column=0, sticky="w", pady=5)

        ctk.CTkLabel(
            master=self,
            text="Продажи",
            font=("Arial", head_font_size)
        ).grid(row=0, column=0, sticky="w", pady=2, padx=3)

        self.__found_frame.grid(row=1, column=0, sticky="w", pady=2, padx=3)
        self.__creating_frame.grid(row=2, column=0, sticky="w", pady=2, padx=3)
        self.__table_frame.grid(row=3, column=0, pady=2, padx=3)
        self.__crud_frame.grid(row=4, column=0, sticky="w", pady=2, padx=3)

        self.bind("<Map>", self.__on_form_show_actions)

    def __create_creation_frame(
            self,
            client_entry_w,
            article_entry_w,
            count_entry_w,
            entryes_h,
            font_size
    ) -> ctk.CTkFrame:
        creating_frame = ctk.CTkFrame(master=self, fg_color=self.cget("fg_color"))

        self.__client_combobox = ctk.CTkComboBox(
            master=creating_frame,
            width=client_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
            command=self.__format_client_card
        )

        self.__article_combobox = ctk.CTkComboBox(
            master=creating_frame,
            width=article_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
            command=self.__format_article
        )

        self.__count_entry = ctk.CTkEntry(
            master=creating_frame,
            width=count_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
            placeholder_text="Кол-во:"
        )

        self.__client_combobox.grid(row=1, column=0)
        self.__article_combobox.grid(row=1, column=1)
        self.__count_entry.grid(row=1, column=2)

        ctk.CTkLabel(
            master=creating_frame,
            text="№ дисконтной карты клиента",
            font=("Arial", font_size)
        ).grid(row=0, column=0, sticky="w", padx=2)

        ctk.CTkLabel(
            master=creating_frame,
            text="Артикул товара",
            font=("Arial", font_size)
        ).grid(row=0, column=1, sticky="w", padx=2)

        ctk.CTkLabel(
            master=creating_frame,
            text="Кол-во",
            font=("Arial", font_size)
        ).grid(row=0, column=2, sticky="w", padx=2)

        return creating_frame

    def __format_client_card(self, cb_choice):
        self.__client_combobox.set(cb_choice[:cb_choice.index(" ")])

    def __format_article(self, cb_choice):
        self.__article_combobox.set(cb_choice[:cb_choice.index(" ")])

    def __create_found_frame(self, entry_w, entry_h, button_w, button_h, font_size) -> ctk.CTkFrame:
        found_frame = ctk.CTkFrame(master=self, fg_color=self.cget("fg_color"))

        self.__found_entry = ctk.CTkEntry(
            master=found_frame,
            width=entry_w,
            height=entry_h,
            font=("Arial", font_size)
        )

        self.__found_button = ctk.CTkButton(
            master=found_frame,
            text="🔍",
            width=button_w,
            height=button_h,
            font=("Arial", font_size + 10),
            command=self.__find_sale
        )

        ctk.CTkLabel(
            master=found_frame,
            text="Найти запись",
            font=("Arial", font_size)
        ).grid(row=0, column=0, sticky="w", padx=2)

        self.__found_entry.grid(row=1, column=0, sticky="w", padx=2)
        self.__found_button.grid(row=1, column=1, sticky="w", padx=2)

        return found_frame

    def __create_crud_frame(self, button_w, button_h, font_size) -> ctk.CTkFrame:
        crud_frame = ctk.CTkFrame(self, fg_color=self.cget("fg_color"))

        self.__add_button = ctk.CTkButton(
            master=crud_frame,
            text="Добавить",
            width=button_w,
            height=button_h,
            font=("Arial", font_size),
            command=self.__add_sale
        )

        self.__del_button = ctk.CTkButton(
            master=crud_frame,
            text="Удалить",
            width=button_w,
            height=button_h,
            font=("Arial", font_size),
            command=self.__del_sale
        )

        self.__add_button.grid(row=0, column=0, padx=2)
        self.__del_button.grid(row=0, column=1, padx=2)

        return crud_frame

    def __clearing_entrys(self):
        self.__count_entry.delete(0, ctk.END)
        self.__article_combobox.set("")
        self.__client_combobox.set("")
        self.__count_entry._activate_placeholder()

    def __table_row_selection(self, event):
        selected_info = event["selected"]
        self.__sales_table.select_row(selected_info.row)

    def __updating_table_data(self, new_data):
        self.__sales_table.set_sheet_data(new_data)
        self.__sales_table.deselect(row="all")
        self.__sales_table.set_all_column_widths(self.__table_column_width)

    def __on_form_show_actions(self, _):
        self.__clearing_entrys()
        self.__found_entry.delete(0, ctk.END)
        table_data = list()
        products_articles = list()
        client_cards = list()

        try:
            table_data = back.get_sales()
            products_articles = get_products_articles()
            client_cards = get_client_cards()
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

        self.__article_combobox.configure(values=products_articles)
        self.__client_combobox.configure(values=client_cards)
        self.__updating_table_data(table_data)

    def __add_sale(self):
        date = datetime.now().replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
        client_card = self.__client_combobox.get()
        product_article = self.__article_combobox.get()
        product_count = self.__count_entry.get()
        try:
            operation_id = back.add_sale(date, client_card, product_article, product_count)
            added_record = [operation_id, date, client_card, product_article, product_count]
            self.__sales_table.insert_row(idx=0, row=added_record, redraw=True)
            self.__clearing_entrys()
            self.__sales_table.deselect(row="all")
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")
        except mysql.connector.errors.IntegrityError:
            InformationDialog(
                self.master,
                "Ошибка данных!",
                "Во время вышего сеанса критически важные данные были изменены!\nПерезайдите в текущий раздел для обновления данных.")
        except TypeError as current_error:
            if current_error.args[0] == "Incorrect article":
                info = "Некорректный формат артикула. Он должен\nсостоять из 10 цифр!"
            elif current_error.args[0] == "Incorrect count":
                info = "Некорректное кол-во товаров. Оно должно являться\nцелым положительным числом!"
            elif current_error.args[0] == "Incorrect card":
                info = "Некорректный формат номера карты. Он должен состоять из\n10 цифр!"
            elif current_error.args[0] == "Article doesnt exist":
                info = "Некорректный артикул. Товар с данным артикулом отсутствует\nв базе данных!"
            elif current_error.args[0] == "Client doesnt exist":
                info = "Некорректный номер карты. Клиент с данным номером отсутствует\nв базе данных!"
            elif current_error.args[0] == "Product count is very big":
                info = "Некорректное количество купленного товара. Оно не должно\nпревышать текущее количество товара!"
            else:
                info = "Непредвиденная ошибка :("
            InformationDialog(self.master, "Некорректный ввод!", info)

    def __del_sale(self):
        selected_table_row = self.__sales_table.get_selected_rows(return_tuple=True)
        if not selected_table_row:
            InformationDialog(
                self.master,
                "Ошибка!",
                "Ни одна строка таблицы не выбрана для удаления!")
            return 0
        selected_row = selected_table_row[0]
        write_off_id = self.__sales_table.get_row_data(r=selected_row)[0]
        dialog = ModalDialog(
            self.master,
            "Подтвердите действие.",
            f"Вы действительно хотите удалить выбранную в таблице запись?\nУдаление данной записи не возвратит изменения\nв количестве товара."
        )
        dialog.wait_window()
        if dialog.modal_result:
            try:
                back.del_sale(write_off_id)
                self.__sales_table.delete_row(selected_row, redraw=True)
                self.__clearing_entrys()
                self.__sales_table.deselect(row="all")
            except mysql.connector.errors.InterfaceError:
                InformationDialog(
                    self.master,
                    "Ошибка подключения к БД!",
                    "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

    def __find_sale(self):
        try:
            finding_record = back.get_finding_sales(self.__found_entry.get())
            self.__updating_table_data(finding_record)
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")


