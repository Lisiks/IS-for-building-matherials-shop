import customtkinter as ctk
import mysql.connector.errors
import Back.backend_for_suppliers as back
from tksheet import Sheet
from Front.global_const import *
from Front.dialog_window import InformationDialog, ModalDialog


class SuppliersForm(ctk.CTkFrame):
    def __init__(self, master, window_w, window_h):
        super().__init__(master)
        self.configure(fg_color=master.cget("fg_color"))

        table_width = window_w - (window_w // 4) - 60
        table_height = window_h - (window_h // 2.7) - 60

        self.__table_column_width = int(table_width // 5)
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
            suppliers_inn_entry_w=self.__table_column_width,
            suppliers_name_entry_w=self.__table_column_width,
            suppliers_address_entry_w=self.__table_column_width,
            suppliers_telephone_entry_w=self.__table_column_width,
            suppliers_mail_entry_w=self.__table_column_width,
            entryes_h=window_h // 20,
            font_size=font_size,
        )

        self.__crud_frame = self.__create_crud_frame(
            button_w=table_width // 3 - 20,
            button_h=window_h // 20,
            font_size=font_size
        )

        self.__table_frame = ctk.CTkFrame(master=self, fg_color="#313131", corner_radius=10)

        self.__suppliers_table = Sheet(
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

        self.__suppliers_table.headers(
            ["ИНН",
             "Наименование",
             "Адрес",
             "Телефон",
             "Электронная почта",
             ]
        )

        self.__suppliers_table.extra_bindings("cell_select", self.__table_row_selection)
        self.__suppliers_table.enable_bindings("single_select")
        self.__suppliers_table.set_all_column_widths(self.__table_column_width)

        ctk.CTkLabel(
            master=self.__table_frame,
            text="Поставщики",
            font=("Arial", font_size + 3),
            anchor="center",
            text_color="white"
        ).grid(row=0, column=0, pady=2)

        self.__suppliers_table.grid(row=1, column=0, sticky="w", pady=5)

        ctk.CTkLabel(
            master=self,
            text="Поставщики",
            font=("Arial", head_font_size)
        ).grid(row=0, column=0, sticky="w", pady=2, padx=3)

        self.__found_frame.grid(row=1, column=0, sticky="w", pady=2, padx=3)
        self.__creating_frame.grid(row=2, column=0, sticky="w", pady=2, padx=3)
        self.__table_frame.grid(row=3, column=0, pady=2, padx=3)
        self.__crud_frame.grid(row=4, column=0, sticky="w", pady=2, padx=3)

        self.bind("<Map>", self.__on_form_show_actions)

    def __create_creation_frame(
            self,
            suppliers_inn_entry_w,
            suppliers_name_entry_w,
            suppliers_address_entry_w,
            suppliers_telephone_entry_w,
            suppliers_mail_entry_w,
            entryes_h,
            font_size
    ) -> ctk.CTkFrame:
        creating_frame = ctk.CTkFrame(master=self, fg_color=self.cget("fg_color"))

        self.__suppliers_inn_entry = ctk.CTkEntry(
            master=creating_frame,
            width=suppliers_inn_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
            placeholder_text="ИНН: 0000000000"
        )

        self.__suppliers_name_entry = ctk.CTkEntry(
            master=creating_frame,
            width=suppliers_name_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
            placeholder_text="Наименование:"
        )

        self.__suppliers_address_entry = ctk.CTkEntry(
            master=creating_frame,
            width=suppliers_address_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
            placeholder_text="Адрес:"
        )

        self.__suppliers_telephone_entry = ctk.CTkEntry(
            master=creating_frame,
            width=suppliers_telephone_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
            placeholder_text="Тел: 0-000-000-00-00"
        )

        self.__suppliers_mail_entry = ctk.CTkEntry(
            master=creating_frame,
            width=suppliers_mail_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
            placeholder_text="Email:"
        )

        self.__suppliers_inn_entry.grid(row=1, column=0)
        self.__suppliers_name_entry.grid(row=1, column=1)
        self.__suppliers_address_entry.grid(row=1, column=2)
        self.__suppliers_telephone_entry.grid(row=1, column=3)
        self.__suppliers_mail_entry.grid(row=1, column=4)

        ctk.CTkLabel(
            master=creating_frame,
            text="ИНН поставщика",
            font=("Arial", font_size)
        ).grid(row=0, column=0, sticky="w", padx=2)

        ctk.CTkLabel(
            master=creating_frame,
            text="Наименование",
            font=("Arial", font_size)
        ).grid(row=0, column=1, sticky="w", padx=2)

        ctk.CTkLabel(
            master=creating_frame,
            text="Физический адрес",
            font=("Arial", font_size)
        ).grid(row=0, column=2, sticky="w", padx=2)

        ctk.CTkLabel(
            master=creating_frame,
            text="Телефон",
            font=("Arial", font_size)
        ).grid(row=0, column=3, sticky="w", padx=2)

        ctk.CTkLabel(
            master=creating_frame,
            text="Электронная почта",
            font=("Arial", font_size)
        ).grid(row=0, column=4, sticky="w", padx=2)

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
            command=self.__find_suppliers
        )

        ctk.CTkLabel(
            master=found_frame,
            text="Найти поставщика",
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
            command=self.__add_supplier
        )

        self.__del_button = ctk.CTkButton(
            master=crud_frame,
            text="Удалить",
            width=button_w,
            height=button_h,
            font=("Arial", font_size),
            command=self.__del_supplier
        )

        self.__change_button = ctk.CTkButton(
            master=crud_frame,
            text="Изменить",
            width=button_w,
            height=button_h,
            font=("Arial", font_size),
            command=self.__update_supplier
        )

        self.__add_button.grid(row=0, column=0, padx=2)
        self.__del_button.grid(row=0, column=1, padx=2)
        self.__change_button.grid(row=0, column=2, padx=2)

        return crud_frame

    def __clearing_entrys(self):
        self.__suppliers_inn_entry.delete(0, ctk.END)

        self.__suppliers_name_entry.delete(0, ctk.END)
        self.__suppliers_address_entry.delete(0, ctk.END)
        self.__suppliers_telephone_entry.delete(0, ctk.END)
        self.__suppliers_mail_entry.delete(0, ctk.END)


        self.__suppliers_inn_entry._activate_placeholder()
        self.__suppliers_name_entry._activate_placeholder()
        self.__suppliers_address_entry._activate_placeholder()
        self.__suppliers_telephone_entry._activate_placeholder()
        self.__suppliers_mail_entry._activate_placeholder()

    def __table_row_selection(self, event):
        selected_info = event["selected"]
        self.__suppliers_table.select_row(selected_info.row)
        inn, name, address, telephone, mail = self.__suppliers_table.get_row_data(r=selected_info.row)
        self.__clearing_entrys()
        self.__suppliers_inn_entry.insert(0, inn)
        self.__suppliers_name_entry.insert(0, name)
        self.__suppliers_address_entry.insert(0, address)
        self.__suppliers_telephone_entry.insert(0, telephone)
        self.__suppliers_mail_entry.insert(0,mail)

    def __updating_table_data(self, new_data):
        self.__suppliers_table.set_sheet_data(new_data)
        self.__suppliers_table.deselect(row="all")
        self.__suppliers_table.set_all_column_widths(self.__table_column_width)

    def __on_form_show_actions(self, _):
        self.__clearing_entrys()
        self.__found_entry.delete(0, ctk.END)
        table_data = list()

        try:
            table_data = back.get_suppliers_data()
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

        self.__updating_table_data(table_data)

    def __add_supplier(self):
        inn = self.__suppliers_inn_entry.get()
        name = self.__suppliers_name_entry.get()
        address = self.__suppliers_address_entry.get()
        telephone = self.__suppliers_telephone_entry.get()
        email = self.__suppliers_mail_entry.get()
        try:
            back.add_supplier(inn, name, address, telephone, email)
            added_record = [inn, name, address, telephone, email]
            self.__suppliers_table.insert_row(idx=0, row=added_record, redraw=True)
            self.__clearing_entrys()
            self.__suppliers_table.deselect(row="all")
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")
        except TypeError as current_error:
            if current_error.args[0] == "Incorrect inn":
                info = "Некорректный формат ИНН. Он должен состоять из\n10 цифр!"
            elif current_error.args[0] == "Incorrect name":
                info = "Некорректный формат наименования. Его длинна должна быть\nне менее 3 и не более 30 символов!"
            elif current_error.args[0] == "Incorrect address":
                info = "Некорректная длинна адреса. Она не должна превышать\n100 символов!"
            elif current_error.args[0] == "Incorrect telephone":
                info = "Некорректный формат номера телефона!"
            elif current_error.args[0] == "Incorrect email":
                info = "Некорректный формат электронной почты. Он должна состоять\nне менее чем из 5 и не более чем из 30 символов,\nа также содержать '@'!"
            elif current_error.args[0] == "Existing inn":
                info = "Поставщик с данным ИНН уже присутствует\nв базе данных"
            else:
                info = "Непредвиденная ошибка :("
            InformationDialog(self.master, "Некорректный ввод!", info)

    def __del_supplier(self):
        selected_table_row = self.__suppliers_table.get_selected_rows(return_tuple=True)
        if not selected_table_row:
            InformationDialog(
                self.master,
                "Ошибка!",
                "Ни одна строка таблицы не выбрана для удаления!")
            return 0
        selected_row = selected_table_row[0]
        inn = self.__suppliers_table.get_row_data(r=selected_row)[0]
        dialog = ModalDialog(
            self.master,
            "Подтвердите действие.",
            f"Вы действительно хотите удалить выбранную в таблице запись?\nПри удалении данной записи будут также уделены все записи\nо поступлениях от данного поставщика."
        )
        dialog.wait_window()
        if dialog.modal_result:
            try:
                back.del_supplier(inn)
                self.__suppliers_table.delete_row(selected_row, redraw=True)
                self.__clearing_entrys()
                self.__suppliers_table.deselect(row="all")
            except mysql.connector.errors.InterfaceError:
                InformationDialog(
                    self.master,
                    "Ошибка подключения к БД!",
                    "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

    def __update_supplier(self):
        selected_table_row = self.__suppliers_table.get_selected_rows(return_tuple=True)
        if not selected_table_row:
            InformationDialog(
                self.master,
                "Ошибка!",
                "Ни одна строка таблицы не выбрана для изменения!")
            return 0
        selected_row = selected_table_row[0]
        old_inn = self.__suppliers_table.get_row_data(r=selected_row)[0]
        dialog = ModalDialog(
            self.master,
            "Подтвердите действие.",
            f"Вы действительно хотите изменить выбранную в таблице запись?\nНекоторые изменения могут отразиться на записях о\nпоступлениях."
        )
        dialog.wait_window()
        if dialog.modal_result:
            inn = self.__suppliers_inn_entry.get()
            name = self.__suppliers_name_entry.get()
            address = self.__suppliers_address_entry.get()
            telephone = self.__suppliers_telephone_entry.get()
            email = self.__suppliers_mail_entry.get()
            try:
                back.update_supplier(old_inn, inn, name, address, telephone, email)
                updated_record = [inn, name, address, telephone, email]
                self.__suppliers_table.delete_row(rows=selected_row)
                self.__suppliers_table.insert_row(idx=selected_row, row=updated_record, redraw=True)
                self.__clearing_entrys()
                self.__suppliers_table.deselect(row="all")
            except mysql.connector.errors.InterfaceError:
                InformationDialog(
                    self.master,
                    "Ошибка подключения к БД!",
                    "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")
            except TypeError as current_error:
                if current_error.args[0] == "Incorrect inn":
                    info = "Некорректный формат ИНН. Он должен состоять из\n10 цифр!"
                elif current_error.args[0] == "Incorrect name":
                    info = "Некорректный формат наименования. Его длинна должна быть\nне менее 3 и не более 30 символов!"
                elif current_error.args[0] == "Incorrect address":
                    info = "Некорректная длинна адреса. Она не должна превышать\n100 символов!"
                elif current_error.args[0] == "Incorrect telephone":
                    info = "Некорректный формат номера телефона!"
                elif current_error.args[0] == "Incorrect email":
                    info = "Некорректный формат электронной почты. Он должна состоять\nне менее чем из 5 и не более чем из 30 символов,\nа также содержать '@'!"
                elif current_error.args[0] == "Existing inn":
                    info = "Поставщик с данным ИНН уже присутствует\nв базе данных"
                else:
                    info = "Непредвиденная ошибка :("
                InformationDialog(self.master, "Некорректный ввод!", info)

    def __find_suppliers(self):
        try:
            finding_record = back.get_finding_suppliers(self.__found_entry.get())
            self.__updating_table_data(finding_record)
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")
