import customtkinter as ctk
import Back.backend_for_purchases as back
import mysql.connector.errors
from Front.global_const import *
from tksheet import Sheet
from Back.query_for_comboboxes_values import get_products_articles, get_suppliers_inn
from Front.dialog_window import InformationDialog, ModalDialog



class PurchasesForm(ctk.CTkFrame):
    def __init__(self, master, window_w, window_h):
        super().__init__(master)
        self.configure(fg_color=master.cget("fg_color"))

        table_width = window_w - (window_w // 4) - 60
        table_height = window_h - (window_h // 2.7) - 60

        self.__table_column_width = int(table_width // 3)
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

        self.__crud_frame = self.__create_crud_frame(
            button_w=table_width // 3 - 20,
            button_h=window_h // 20,
            font_size=font_size
        )

        self.__table_frame = ctk.CTkScrollableFrame(
            master=self,
            width=table_width,
            height=table_width,
            fg_color=self.cget("fg_color")
        )

        self.__table_frame = ctk.CTkFrame(master=self, fg_color="#313131", corner_radius=10)

        self.__purchases_table = Sheet(
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

        self.__purchases_table.headers(
            [
             "ID",
             "Дата и время операции",
             "ИНН поставщика",
             "№ транспортной накладной",
             ]
        )

        self.__purchases_table.extra_bindings("cell_select", self.__table_row_selection)
        self.__purchases_table.enable_bindings("single_select")
        self.__purchases_table.hide_columns(columns=0)

        ctk.CTkLabel(
            master=self.__table_frame,
            text="Все операции",
            font=("Arial", font_size + 3),
            anchor="center",
            text_color="white"
        ).grid(row=0, column=0, padx=3)

        self.__purchases_table.grid(row=1, column=0, sticky="w", pady=5)

        ctk.CTkLabel(
            master=self,
            text="Поступления",
            font=("Arial", head_font_size)
        ).grid(row=0, column=0, sticky="w", pady=2, padx=3)

        self.__found_frame.grid(row=1, column=0, sticky="w", pady=2, padx=3)
        self.__table_frame.grid(row=2, column=0, pady=2, padx=3)
        self.__crud_frame.grid(row=3, column=0, sticky="w", pady=2, padx=3)
        self.bind("<Map>", self.__on_form_show_actions)


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
            font=("Arial", font_size+10),
            command=self.__find_purchases
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
            command=self.__add_purchase
        )

        self.__expect_button = ctk.CTkButton(
            master=crud_frame,
            text="Просмотреть",
            width=button_w,
            height=button_h,
            font=("Arial", font_size),
            command=self.__view_purchase

        )

        self.__del_button = ctk.CTkButton(
            master=crud_frame,
            text="Удалить",
            width=button_w,
            height=button_h,
            font=("Arial", font_size),
            command=self.__del_purchases
        )

        self.__add_button.grid(row=0, column=0, padx=2)
        self.__expect_button.grid(row=0, column=1, padx=2)
        self.__del_button.grid(row=0, column=2, padx=2)

        return crud_frame

    def __table_row_selection(self, event):
        selected_info = event["selected"]
        self.__purchases_table.select_row(selected_info.row)

    def __updating_table_data(self, new_data):
        self.__purchases_table.set_sheet_data(new_data)
        self.__purchases_table.deselect(row="all")
        self.__purchases_table.set_all_column_widths(self.__table_column_width)

    def __on_form_show_actions(self, _):
        self.__found_entry.delete(0, ctk.END)
        table_data = list()

        try:
            table_data = back.get_purchases()
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")
        self.__updating_table_data(table_data)

    def __add_purchase(self):
        try:
            suppliers_inn = get_suppliers_inn()
            product_articles = get_products_articles()
            adding_form = AddingPurchasesWindow(self, self.winfo_screenwidth(), self.winfo_screenheight(), suppliers_inn, product_articles)
            adding_form.wait_window()
            added_row = adding_form.added_record
            if added_row:
                self.__purchases_table.insert_row(added_row, idx=0, redraw=True)
                self.__purchases_table.deselect(row="all")
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")


    def __del_purchases(self):
        selected_table_row = self.__purchases_table.get_selected_rows(return_tuple=True)
        if not selected_table_row:
            InformationDialog(
                self.master,
                "Ошибка!",
                "Ни одна строка таблицы не выбрана для удаления!")
            return 0
        selected_row = selected_table_row[0]
        purchase_id = self.__purchases_table.get_row_data(r=selected_row)[0]
        dialog = ModalDialog(
            self.master,
            "Подтвердите действие.",
            f"Вы действительно хотите удалить выбранную в таблице запись?\nУдаление данной записи не возвратит изменения\nв количестве товара."
        )
        dialog.wait_window()
        if dialog.modal_result:
            try:
                back.del_purchase(purchase_id)
                self.__purchases_table.delete_row(selected_row, redraw=True)
                self.__purchases_table.deselect(row="all")
            except mysql.connector.errors.InterfaceError:
                InformationDialog(
                    self.master,
                    "Ошибка подключения к БД!",
                    "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

    def __view_purchase(self):
        selected_rows = self.__purchases_table.get_selected_rows(return_tuple=True)
        if len(selected_rows) == 0:
            InformationDialog(self.master,"Ошибка!","Для просмотра необходимо выбрать одну запись из таблицы!")
        else:
            try:
                purchase_id = self.__purchases_table.get_row_data(selected_rows[0])[0]
                purchase_info = back.get_purchase_information(purchase_id)
                view_window = ViewPurchasingWindow(self, self.winfo_screenwidth(), self.winfo_screenheight(), purchase_info)
                view_window.wait_window()
            except mysql.connector.errors.InterfaceError:
                InformationDialog(
                    self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

    def __find_purchases(self):
        try:
            finding_record = back.get_finding_purchases(self.__found_entry.get())
            self.__updating_table_data(finding_record)
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")


class AddingPurchasesWindow(ctk.CTkToplevel):
    def __init__(self, master, window_w, window_h, suppliers_inn, products_articles):
        super().__init__(master=master)
        self.__W = window_w // 4 * 3
        self.__H = window_h // 4 * 3
        self.title("Добавить поступление")
        self.geometry(f"{self.__W}x{self.__H}")
        self.minsize(self.__W, self.__H)
        self.maxsize(self.__W, self.__H)

        head_font_size = round(CLASSIC_HEAD_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))
        font_size = round(CLASSIC_WIDGETS_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))
        table_font_size = (round(CLASSIC_TABLE_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH)))

        widgets_width = self.__W // 2 - 20
        widgets_height = self.__H // 15

        self.__supplier_inn_cb = ctk.CTkComboBox(
            master=self,
            width=widgets_width,
            height=widgets_height,
            font=("Arial", font_size),
            values=suppliers_inn,
            command=self.__format_supplier_inn_cb
        )
        self.__supplier_inn_cb.set("")


        self.__landing_bill_number_entry = ctk.CTkEntry(
            master=self,
            width=widgets_width,
            height=widgets_height,
            font=("Arial", font_size),
            placeholder_text="№ документа:"
        )

        self.__product_article_cb = ctk.CTkComboBox(
            master=self,
            width=widgets_width,
            height=widgets_height,
            font=("Arial", font_size),
            values=products_articles,
            command=self.__format_product_article_cb
        )
        self.__product_article_cb.set("")


        self.__product_count_entry = ctk.CTkEntry(
            master=self,
            width=widgets_width,
            height=widgets_height,
            font=("Arial", font_size),
            placeholder_text="Кол-во:"
        )

        self.__add_product_button = ctk.CTkButton(
            master=self,
            text="Добавить товар",
            width=widgets_width,
            height=widgets_height,
            font=("Arial", font_size),
            command=self.__add_product
        )

        self.__del_product_button = ctk.CTkButton(
            master=self,
            text="Удалить товар",
            width=widgets_width,
            height=widgets_height,
            font=("Arial", font_size),
            command=self.__del_product
        )

        self.__table_frame = ctk.CTkFrame(master=self, fg_color="#313131", corner_radius=10)

        self.__product_table = Sheet(
            self.__table_frame,
            show_x_scrollbar=False,
            show_y_scrollbar=False,

            width=self.__W - 20,
            height=self.__H // 2,
            header_height=(self.__H // 2) // 6,
            row_height=(self.__H // 2) // 6,

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

        self.__product_table.headers(["Артикул товара", "Кол-во"])
        self.__product_table.extra_bindings("cell_select", lambda event: self.__product_table.select_row(event["selected"].row))
        self.__product_table.enable_bindings("single_select")
        self.__product_table.set_all_column_widths((self.__W - 20) // 2)

        self.__add_button = ctk.CTkButton(
            master=self,
            text="Добавить запись",
            width=widgets_width,
            height=widgets_height,
            font=("Arial", font_size),
            command=self.__add_record
        )

        self.__cancel_button = ctk.CTkButton(
            master=self,
            text="Отмена",
            width=widgets_width,
            height=widgets_height,
            font=("Arial", font_size),
            command=self.destroy
        )

        ctk.CTkLabel(
            master=self, text="Добавить запись", font=("Arial", head_font_size)
        ).grid(row=0, column=0, sticky="w", padx=4, pady=2)

        ctk.CTkLabel(
            master=self, text="ИНН поставщика", font=("Arial", font_size)
        ).grid(row=1, column=0, sticky="w", padx=4, pady=2)

        ctk.CTkLabel(
            master=self, text="№ транспортной накладной", font=("Arial", font_size)
        ).grid(row=1, column=1, sticky="e", padx=4, pady=2)

        self.__supplier_inn_cb.grid(row=2, column=0, sticky="w", padx=4, pady=4)
        self.__landing_bill_number_entry.grid(row=2, column=1, sticky="e", padx=4, pady=4)

        ctk.CTkLabel(
            master=self, text="Артикул товара", font=("Arial", font_size)
        ).grid(row=3, column=0, sticky="w", padx=4, pady=2)

        ctk.CTkLabel(
            master=self, text="Кол-во", font=("Arial", font_size)
        ).grid(row=3, column=1, sticky="e", padx=4, pady=2)

        self.__product_article_cb.grid(row=4, column=0, sticky="w", padx=4, pady=2)
        self.__product_count_entry.grid(row=4, column=1, sticky="e", padx=4, pady=2)

        self.__add_product_button.grid(row=5, column=0, sticky="w", padx=4, pady=2)
        self.__del_product_button.grid(row=5, column=1, sticky="e", padx=4, pady=2)

        self.__table_frame.grid(row=6, column=0, columnspan=2, sticky="w", padx=4, pady=2)
        ctk.CTkLabel(
            master=self.__table_frame, text="Поступившие товары", font=("Arial", font_size + 3), text_color="white",
        ).grid(row=0, column=0, padx=2, pady=2)
        self.__product_table.grid(row=1, column=0, sticky="w", padx=4, pady=2)

        self.__add_button.grid(row=7, column=0, sticky="w", padx=4, pady=2)
        self.__cancel_button.grid(row=7, column=1, sticky="e", padx=4, pady=2)
        self.grab_set()

        self.__added_product_set = set()
        self.added_record = []

    def __format_supplier_inn_cb(self, choice):
        self.__supplier_inn_cb.set(choice[:choice.index(" ")])

    def __format_product_article_cb(self, choice):
        self.__product_article_cb.set(choice[:choice.index(" ")])

    def __add_product(self):
        product_article = self.__product_article_cb.get()
        product_count = self.__product_count_entry.get()

        if product_article == "":
            InformationDialog(self, "Ошибка ввода!", "Для добавления поступившего товара укажите артикул!")
        elif product_article in self.__added_product_set:
            InformationDialog(self, "Ошибка ввода!", "Данный товар уже указан!")
        elif product_count == "" or not product_count.isdigit() or int(product_count) <= 0:
            InformationDialog(self, "Ошибка ввода!", "Некорректное кол-во товара! Оно должно быть целым положительным цислом.")
        else:
            self.__added_product_set.add(product_article)
            self.__product_table.insert_row(row=[product_article, product_count], idx=0, redraw=True)
            self.__product_table.deselect(row="all")
            self.__product_article_cb.set("")
            self.__product_count_entry.delete(0, ctk.END)

    def __del_product(self):
        selected_rows = self.__product_table.get_selected_rows(return_tuple=True)
        if len(selected_rows) == 0:
            InformationDialog(self, "Ошибка!", "Для удаления позиции выдерите ее в таблице.")
        else:
            deleted_row_idx = selected_rows[0]
            deleted_row = self.__product_table.get_data(deleted_row_idx)
            self.__added_product_set.remove(deleted_row[0])
            self.__product_table.delete_row(deleted_row_idx, redraw=True)

    def __add_record(self):
        supplier_inn = self.__supplier_inn_cb.get()
        document_number = self.__landing_bill_number_entry.get()
        product_data = self.__product_table.get_data()

        if len(product_data) == 0:
            InformationDialog(self, "Ошибка!", "Для создания записи укажите хотя бы одну позицию!")
            return 0
        if list != type(product_data[0]):
            product_data = [product_data]

        try:
            self.added_record = back.add_purchase(supplier_inn, document_number, product_data)
            self.destroy()
        except mysql.connector.errors.InterfaceError:
            InformationDialog(self.master,"Ошибка подключения к БД!","Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")
        except mysql.connector.errors.IntegrityError:
            InformationDialog(self.master,"Ошибка данных!","Во время вышего сеанса критически важные данные были изменены!\nПерезайдите в текущий раздел для обновления данных.")
        except TypeError as e:
            if e.args[0] == "Incorrect inn":
                InformationDialog(self, "Ошибка ввода!","Некорректный формат ИНН.")
            elif e.args[0] == "Incorrect document":
                InformationDialog(self, "Ошибка ввода!", "Некорректный формат номера транспортной накладной.\nОн должен быть не менее 1 и не более 30 символов\n и состоять только из латинских букв и цифр.")
            elif e.args[0] == "Article doesnt exist":
                InformationDialog(self, "Ошибка ввода!", f"Товар с артикулом {e.args[1]} отсутствует\nв базе данных.")
            else:
                InformationDialog(self, "Непридвиденная ошибка!", e.args[0])


class ViewPurchasingWindow(ctk.CTkToplevel):
    def __init__(self, master, window_w, window_h, purchase_info):
        super().__init__(master)
        self.__W = window_w // 4 * 3
        self.__H = window_h // 4 * 3
        self.title(f"Поставка №{purchase_info.purchase_id}")

        self.minsize(self.__W, self.__H)
        self.maxsize(self.__W, self.__H)
        self.geometry(f"{self.__W}x{self.__H}")

        head_font_size = round(CLASSIC_HEAD_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))
        font_size = round(CLASSIC_WIDGETS_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))
        table_font_size = (round(CLASSIC_TABLE_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH)))

        widgets_width = self.__W // 2 - 20
        widgets_height = self.__H // 15

        self.__close_button = ctk.CTkButton(
            master=self,
            text="Закрыть",
            width=widgets_width,
            height=widgets_height,
            font=("Arial", font_size),
            command=self.destroy
        )

        self.__table_frame = ctk.CTkFrame(master=self, fg_color="#313131", corner_radius=10)

        self.__product_table = Sheet(
            self.__table_frame,
            show_x_scrollbar=False,
            show_y_scrollbar=False,

            width=self.__W - 20,
            height=self.__H // 4 * 2.5,
            header_height=(self.__H // 4 * 2.5) // 8,
            row_height=(self.__H // 4 * 2.5) // 8,

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

        self.__product_table.headers(["Артикул товара", "Наименование", "Кол-во", "Общая стоимость"])
        self.__product_table.set_sheet_data(purchase_info.product_list)
        self.__product_table.set_all_column_widths((self.__W - 20)//4)

        ctk.CTkLabel(
            master=self, text=f"Поставка №{purchase_info.purchase_id}", font=("Arial", head_font_size)
        ).grid(row=0, column=0, sticky="w", padx=4, pady=2)

        ctk.CTkLabel(
            master=self, text=f"Дата: {purchase_info.purchase_date}",
            font=("Arial", font_size)).grid(row=1, column=0, sticky="w", padx=4, pady=2)

        ctk.CTkLabel(
            master=self, text=f"Поставщик: {purchase_info.supplier_name} ({purchase_info.supplier_inn})",
            font=("Arial", font_size)).grid(row=2, column=0, sticky="w", padx=4, pady=2)

        ctk.CTkLabel(
            master=self, text=f"№ транспортной накладной: {purchase_info.landing_bill_number}",
            font=("Arial", font_size)).grid(row=3, column=0, sticky="w", padx=4, pady=2)

        self.__table_frame.grid(row=4, column=0, sticky="w", padx=4, pady=2)
        ctk.CTkLabel(
            master=self.__table_frame, text="Поступившие товары", font=("Arial", font_size + 3), text_color="white",
        ).grid(row=0, column=0, padx=2, pady=2)
        self.__product_table.grid(row=1, column=0, sticky="w", padx=4, pady=2)
        ctk.CTkLabel(
            master=self,
            text=f"Итого: {sum([product_data[3] for product_data in purchase_info.product_list])}",
            font=("Arial", font_size)).grid(row=5, column=0, sticky="w", padx=4, pady=2)

        self.__close_button.grid(row=6, column=0, sticky="w", padx=4, pady=2)
        self.grab_set()



















