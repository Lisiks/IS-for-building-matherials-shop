import customtkinter as ctk
import Back.backend_for_nomenclature as back
import mysql.connector.errors
from tksheet import Sheet
from Front.dialog_window import InformationDialog, ModalDialog
from Back.query_for_comboboxes_values import get_product_types, get_product_units
from Front.global_const import *


class NomenclatureForm(ctk.CTkFrame):
    def __init__(self, master, window_w, window_h):
        super().__init__(master)
        self.configure(fg_color=master.cget("fg_color"))

        table_width = window_w - (window_w // 4) - 60
        table_height = window_h - (window_h // 2.7) - 60

        self.__table_column_width = int(table_width // 7)
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
            article_entry_w=self.__table_column_width,
            name_entry_w=self.__table_column_width,
            buying_price_entry_w=self.__table_column_width,
            selling_price_entry_w=self.__table_column_width,
            type_entry_w=self.__table_column_width,
            unit_entry_w=self.__table_column_width * 2,
            entryes_h=window_h//20,
            font_size=font_size,
        )

        self.__crud_frame = self.__create_crud_frame(
            button_w=table_width // 3 - 20,
            button_h=window_h // 20,
            font_size=font_size
        )

        self.__table_frame = ctk.CTkFrame(master=self, fg_color="#313131", corner_radius=10)

        self.__nomenclature_table = Sheet(
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

        self.__nomenclature_table.headers(
            ["Артикул",
             "Наименование",
             "Актуальная\nцена закупки",
             "Актуальная\nцена продажи",
             "Тип",
             "Единица измерения",
             "Количество"]
        )

        self.__nomenclature_table.extra_bindings("cell_select", self.__table_row_selection)
        self.__nomenclature_table.enable_bindings("single_select")

        ctk.CTkLabel(
            master=self.__table_frame,
            text="Товары",
            font=("Arial", font_size + 3),
            text_color="white",
            anchor="center"
        ).grid(row=0, column=0, pady=2)

        self.__nomenclature_table.grid(row=1, column=0, sticky="w", pady=5)

        ctk.CTkLabel(
            master=self,
            text="Номенклатура",
            font=("Arial", head_font_size)
        ).grid(row=0, column=0, sticky="w", pady=2, padx=3)

        self.__found_frame.grid(row=1, column=0,  sticky="w", pady=2, padx=3)
        self.__creating_frame.grid(row=2, column=0, sticky="w", pady=2, padx=3)
        self.__table_frame.grid(row=3, column=0, sticky="w", pady=2, padx=3)
        self.__crud_frame.grid(row=4, column=0, sticky="w", pady=2, padx=3)

        self.bind("<Map>", self.__on_form_show_actions)

    def __create_creation_frame(
            self,
            article_entry_w,
            name_entry_w,
            buying_price_entry_w,
            selling_price_entry_w,
            type_entry_w,
            unit_entry_w,
            entryes_h,
            font_size
    ) -> ctk.CTkFrame:
        creating_frame = ctk.CTkFrame(master=self, fg_color=self.cget("fg_color"))

        self.__article_entry = ctk.CTkEntry(
            master=creating_frame,
            width=article_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
            placeholder_text="Артикул: 0000000000"
        )

        self.__name_entry = ctk.CTkEntry(
            master=creating_frame,
            width=name_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
            placeholder_text="Наименование:"
        )

        self.__buying_price_entry = ctk.CTkEntry(
            master=creating_frame,
            width=buying_price_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
            placeholder_text="00000000.00"
        )

        self.__selling_price_entry = ctk.CTkEntry(
            master=creating_frame,
            width=selling_price_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
            placeholder_text="00000000.00"
        )

        self.__type_combobox = ctk.CTkComboBox(
            master=creating_frame,
            width=type_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
        )

        self.__unit_combobox = ctk.CTkComboBox(
            master=creating_frame,
            width=unit_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
        )

        self.__article_entry.grid(row=1, column=0)
        self.__name_entry.grid(row=1, column=1)
        self.__buying_price_entry.grid(row=1, column=2)
        self.__selling_price_entry.grid(row=1, column=3)
        self.__type_combobox.grid(row=1, column=4)
        self.__unit_combobox.grid(row=1, column=5)

        ctk.CTkLabel(
            master=creating_frame,
            text="Артикул товара",
            font=("Arial", font_size)
        ).grid(row=0, column=0, sticky="w", padx=2)

        ctk.CTkLabel(
            master=creating_frame,
            text="Наименование",
            font=("Arial", font_size)
        ).grid(row=0, column=1, sticky="w", padx=2)

        ctk.CTkLabel(
            master=creating_frame,
            text="Цена закупки",
            font=("Arial", font_size)
        ).grid(row=0, column=2, sticky="w", padx=2)

        ctk.CTkLabel(
            master=creating_frame,
            text="Цена продажи",
            font=("Arial", font_size)
        ).grid(row=0, column=3, sticky="w", padx=2)

        ctk.CTkLabel(
            master=creating_frame,
            text="Тип",
            font=("Arial", font_size)
        ).grid(row=0, column=4, sticky="w", padx=2)

        ctk.CTkLabel(
            master=creating_frame,
            text="Ед. измерения",
            font=("Arial", font_size)
        ).grid(row=0, column=5, sticky="w", padx=2)

        return creating_frame

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
            command=self.__find_products
        )

        ctk.CTkLabel(
            master=found_frame,
            text="Найти товар",
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
            command=self.__add_product
        )

        self.__del_button = ctk.CTkButton(
            master=crud_frame,
            text="Удалить",
            width=button_w,
            height=button_h,
            font=("Arial", font_size),
            command=self.__del_product
        )

        self.__change_button = ctk.CTkButton(
            master=crud_frame,
            text="Изменить",
            width=button_w,
            height=button_h,
            font=("Arial", font_size),
            command=self.__update_product
        )

        self.__add_button.grid(row=0, column=0, padx=2)
        self.__del_button.grid(row=0, column=1, padx=2)
        self.__change_button.grid(row=0, column=2, padx=2)

        return crud_frame

    def __clearing_entrys(self):
        self.__article_entry.delete(0, ctk.END)

        self.__name_entry.delete(0, ctk.END)
        self.__buying_price_entry.delete(0, ctk.END)
        self.__selling_price_entry.delete(0, ctk.END)
        self.__type_combobox.set("")
        self.__unit_combobox.set("")

        self.__article_entry._activate_placeholder()
        self.__name_entry._activate_placeholder()
        self.__buying_price_entry._activate_placeholder()
        self.__selling_price_entry._activate_placeholder()

    def __table_row_selection(self, event):
        selected_info = event["selected"]
        self.__nomenclature_table.select_row(selected_info.row)
        article, name, buy_price, sel_price, prod_type, prod_unit, *_ = self.__nomenclature_table.get_row_data(r=selected_info.row)
        self.__clearing_entrys()
        self.__article_entry.insert(0, article)
        self.__name_entry.insert(0, name)
        self.__buying_price_entry.insert(0, buy_price)
        self.__selling_price_entry.insert(0, sel_price)
        self.__type_combobox.set(prod_type)
        self.__unit_combobox.set(prod_unit)

    def __updating_table_data(self, new_data):
        self.__nomenclature_table.set_sheet_data(new_data)
        self.__nomenclature_table.deselect(row="all")
        self.__nomenclature_table.set_all_column_widths(self.__table_column_width)

    def __on_form_show_actions(self, _):
        self.__clearing_entrys()
        self.__found_entry.delete(0, ctk.END)
        self.__type_combobox.configure(values=[])
        self.__unit_combobox.configure(values=[])
        table_data = list()

        try:
            type_list = get_product_types()
            self.__type_combobox.configure(values=type_list)
            unit_list = get_product_units()
            self.__unit_combobox.configure(values=unit_list)
            table_data = back.get_nomenclature()
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

        self.__updating_table_data(table_data)

    def __add_product(self):
        article = self.__article_entry.get()
        name = self.__name_entry.get()
        buy_price = self.__buying_price_entry.get()
        sel_price = self.__selling_price_entry.get()
        prod_type = self.__type_combobox.get()
        prod_unit = self.__unit_combobox.get()
        try:
            back.add_product(article, name, buy_price, sel_price, prod_type, prod_unit)
            added_record = [article, name, buy_price, sel_price, prod_type, prod_unit, 0]
            self.__nomenclature_table.insert_row(idx=0, row=added_record, redraw=True)
            self.__clearing_entrys()
            self.__nomenclature_table.deselect(row="all")
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
        except ValueError:
            InformationDialog(
                self.master,
                "Некорректный ввод!",
                "Цены продажи и закупки должны быть\nвещественным числом!")
        except TypeError as current_error:
            if current_error.args[0] == "Incorrect length":
                info = "Некорректный формат артикула. Он должен\nсостоять из 10 цифр!"
            elif current_error.args[0] == "Incorrect name length":
                info = "Некорректный формат наименования. Его длинна должна быть\nне менее 3 и не более 30 символов!"
            elif current_error.args[0] == "Incorrect buy price value":
                info = "Некорректная величина цены закупки. Она должна составлять\nне менее 0.01 и не более 99999999.99 руб.!"
            elif current_error.args[0] == "Incorrect sel price value":
                info = "Некорректная величина цены продажи. Она должна составлять\nне менее 0.01 и не более 99999999.99 руб.!"
            elif current_error.args[0] == "Existing article":
                info = "Товар с данным артикулом уже присутствует\nв базе данных"
            elif current_error.args[0] == "Type doesnt exist":
                info = "Указанный тип товара отсутствует в базе данных!"
            elif current_error.args[0] == "Unit doesnt exist":
                info = "Указанная единица измерения товара отсутствует в базе данных!"
            else:
                info = "Непредвиденная ошибка :("
            InformationDialog(self.master, "Некорректный ввод!", info)

    def __del_product(self):
        selected_table_row = self.__nomenclature_table.get_selected_rows(return_tuple=True)
        if not selected_table_row:
            InformationDialog(
                self.master,
                "Ошибка!",
                "Ни одна строка таблицы не выбрана для удаления!")
            return 0
        selected_row = selected_table_row[0]
        article = self.__nomenclature_table.get_row_data(r=selected_row)[0]
        dialog = ModalDialog(
            self.master,
            "Подтвердите действие.",
            f"Вы действительно хотите удалить выбранную в таблице запись?\nПри удалении данной записи будут также уделены все записи\nо поступлениях, продажах и списаниях."
        )
        dialog.wait_window()
        if dialog.modal_result:
            try:
                back.del_product(article)
                self.__nomenclature_table.delete_row(selected_row, redraw=True)
                self.__clearing_entrys()
                self.__nomenclature_table.deselect(row="all")
            except mysql.connector.errors.InterfaceError:
                InformationDialog(
                    self.master,
                    "Ошибка подключения к БД!",
                    "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

    def __update_product(self):
        selected_table_row = self.__nomenclature_table.get_selected_rows(return_tuple=True)
        if not selected_table_row:
            InformationDialog(
                self.master,
                "Ошибка!",
                "Ни одна строка таблицы не выбрана для изменения!")
            return 0
        selected_row = selected_table_row[0]
        old_article, *_, count = self.__nomenclature_table.get_row_data(r=selected_row)
        dialog = ModalDialog(
            self.master,
            "Подтвердите действие.",
            f"Вы действительно хотите изменить выбранную в таблице запись?\nНекоторые изменения могут отразиться на записях о\nпоступлениях, продажах и списаниях."
        )
        dialog.wait_window()
        if dialog.modal_result:
            article = self.__article_entry.get()
            name = self.__name_entry.get()
            buy_price = self.__buying_price_entry.get()
            sel_price = self.__selling_price_entry.get()
            prod_type = self.__type_combobox.get()
            prod_unit = self.__unit_combobox.get()
            try:
                back.update_product(old_article, article, name, buy_price, sel_price, prod_type, prod_unit)
                updated_record = [article, name, buy_price, sel_price, prod_type, prod_unit, count]
                self.__nomenclature_table.delete_row(rows=selected_row)
                self.__nomenclature_table.insert_row(idx=selected_row, row=updated_record, redraw=True)
                self.__nomenclature_table.deselect(row="all")
                self.__clearing_entrys()
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
            except ValueError:
                InformationDialog(
                    self.master,
                    "Некорректный ввод!",
                    "Цены продажи и закупки должны быть\nвещественным числом!")
            except TypeError as current_error:
                if current_error.args[0] == "Incorrect length":
                    info = "Некорректный формат артикула. Он должен\nсостоять из 10 цифр!"
                elif current_error.args[0] == "Incorrect name length":
                    info = "Некорректный формат наименования. Его длинна должна быть\nне менее 3 и не более 30 символов!"
                elif current_error.args[0] == "Incorrect buy price value":
                    info = "Некорректная величина цены. Цена должна составлять\nне менее 0.01 и не более 99999999.99 руб.!"
                elif current_error.args[0] == "Type doesnt exist":
                    info = "Указанный тип товара отсутствует в базе данных!"
                elif current_error.args[0] == "Unit doesnt exist":
                    info = "Указанная единица измерения товара отсутствует в базе данных!"
                elif current_error.args[0] == "Existing article":
                    info = "Товар с данным артикулом уже присутствует\nв базе данных"
                else:
                    info = "Непредвиденная ошибка :("
                InformationDialog(self.master, "Некорректный ввод!", info)

    def __find_products(self):
        try:
            finding_record = back.get_finding_products(self.__found_entry.get())
            self.__updating_table_data(finding_record)
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")





