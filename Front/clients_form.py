import customtkinter as ctk
import Back.backend_for_clients as back
import mysql.connector.errors
from tksheet import Sheet
from global_const import *
from Front.dialog_window import InformationDialog, ModalDialog



class ClientsForm(ctk.CTkFrame):
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
            client_card_entry_w=self.__table_column_width,
            client_fam_entry_w=self.__table_column_width,
            client_name_entry_w=self.__table_column_width,
            client_telephone_entry_w=self.__table_column_width,
            client_discount_entry_w=self.__table_column_width,
            entryes_h=window_h // 20,
            font_size=font_size,
        )

        self.__crud_frame = self.__create_crud_frame(
            button_w=table_width // 3 - 20,
            button_h=window_h // 20,
            font_size=font_size
        )

        self.__table_frame = ctk.CTkFrame(master=self, fg_color="#313131", corner_radius=10)

        self.__clients_table = Sheet(
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

        self.__clients_table.headers(
            ["№ Дисконтной карты",
             "Фамилия",
             "Имя",
             "Телефон",
             "Скидка %",
             ]
        )

        self.__clients_table.extra_bindings("cell_select", self.__table_row_selection)
        self.__clients_table.enable_bindings("single_select")
        self.__clients_table.set_all_column_widths(self.__table_column_width)

        ctk.CTkLabel(
            master=self.__table_frame,
            text="Клиенты",
            font=("Arial", font_size + 3),
            anchor="center",
            text_color="white"
        ).grid(row=0, column=0, pady=2)

        self.__clients_table.grid(row=1, column=0, sticky="w", pady=5)

        ctk.CTkLabel(
            master=self,
            text="Клиенты",
            font=("Arial", head_font_size)
        ).grid(row=0, column=0, sticky="w", pady=2, padx=3)

        self.__found_frame.grid(row=1, column=0, sticky="w", pady=2, padx=3)
        self.__creating_frame.grid(row=2, column=0, sticky="w", pady=2, padx=3)
        self.__table_frame.grid(row=3, column=0, pady=2, padx=3)
        self.__crud_frame.grid(row=4, column=0, sticky="w", pady=2, padx=3)

        self.bind("<Map>", self.__on_form_show_actions)

    def __create_creation_frame(
            self,
            client_card_entry_w,
            client_fam_entry_w,
            client_name_entry_w,
            client_telephone_entry_w,
            client_discount_entry_w,
            entryes_h,
            font_size
    ) -> ctk.CTkFrame:
        creating_frame = ctk.CTkFrame(master=self, fg_color=self.cget("fg_color"))

        self.__client_card_entry = ctk.CTkEntry(
            master=creating_frame,
            width=client_card_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
            placeholder_text="№ карты: 0000000000"
        )

        self.__client_fam_entry = ctk.CTkEntry(
            master=creating_frame,
            width=client_fam_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
            placeholder_text="Фамилия:"
        )

        self.__client_name_entry = ctk.CTkEntry(
            master=creating_frame,
            width=client_name_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
            placeholder_text="Имя:"
        )

        self.__client_telephone_entry = ctk.CTkEntry(
            master=creating_frame,
            width=client_telephone_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
            placeholder_text="Тел: 0-000-000-00-00"
        )

        self.__client_discount_entry = ctk.CTkEntry(
            master=creating_frame,
            width=client_discount_entry_w,
            height=entryes_h,
            font=("Arial", font_size),
            placeholder_text="%:"
        )

        self.__client_card_entry.grid(row=1, column=0)
        self.__client_fam_entry.grid(row=1, column=1)
        self.__client_name_entry.grid(row=1, column=2)
        self.__client_telephone_entry.grid(row=1, column=3)
        self.__client_discount_entry.grid(row=1, column=4)

        ctk.CTkLabel(
            master=creating_frame,
            text="№ дисконтной карты клиента",
            font=("Arial", font_size)
        ).grid(row=0, column=0, sticky="w", padx=2)

        ctk.CTkLabel(
            master=creating_frame,
            text="Фамилия",
            font=("Arial", font_size)
        ).grid(row=0, column=1, sticky="w", padx=2)

        ctk.CTkLabel(
            master=creating_frame,
            text="Имя",
            font=("Arial", font_size)
        ).grid(row=0, column=2, sticky="w", padx=2)

        ctk.CTkLabel(
            master=creating_frame,
            text="Телефон",
            font=("Arial", font_size)
        ).grid(row=0, column=3, sticky="w", padx=2)

        ctk.CTkLabel(
            master=creating_frame,
            text="Скидка по карте",
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
            command=self.__find_client
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
            command=self.__add_client
        )

        self.__del_button = ctk.CTkButton(
            master=crud_frame,
            text="Удалить",
            width=button_w,
            height=button_h,
            font=("Arial", font_size),
            command=self.__del_client
        )

        self.__change_button = ctk.CTkButton(
            master=crud_frame,
            text="Изменить",
            width=button_w,
            height=button_h,
            font=("Arial", font_size),
            command=self.__update_client
        )

        self.__add_button.grid(row=0, column=0, padx=2)
        self.__del_button.grid(row=0, column=1, padx=2)
        self.__change_button.grid(row=0, column=2, padx=2)

        return crud_frame

    def __clearing_entrys(self):
        self.__client_card_entry.delete(0, ctk.END)
        self.__client_fam_entry.delete(0, ctk.END)
        self.__client_name_entry.delete(0, ctk.END)
        self.__client_telephone_entry.delete(0, ctk.END)
        self.__client_discount_entry.delete(0, ctk.END)

        self.__client_card_entry._activate_placeholder()
        self.__client_fam_entry._activate_placeholder()
        self.__client_name_entry._activate_placeholder()
        self.__client_telephone_entry._activate_placeholder()
        self.__client_discount_entry._activate_placeholder()

    def __table_row_selection(self, event):
        selected_info = event["selected"]
        self.__clients_table.select_row(selected_info.row)
        card, fam, name, telephone, discount = self.__clients_table.get_row_data(r=selected_info.row)
        self.__clearing_entrys()
        self.__client_card_entry.insert(0, card)
        self.__client_fam_entry.insert(0, fam)
        self.__client_name_entry.insert(0, name)
        self.__client_telephone_entry.insert(0, telephone)
        self.__client_discount_entry.insert(0, discount)


    def __updating_table_data(self, new_data):
        self.__clients_table.set_sheet_data(new_data)
        self.__clients_table.deselect(row="all")
        self.__clients_table.set_all_column_widths(self.__table_column_width)

    def __on_form_show_actions(self, _):
        self.__clearing_entrys()
        self.__found_entry.delete(0, ctk.END)
        table_data = list()

        try:
            table_data = back.get_clients_data()
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

        self.__updating_table_data(table_data)

    def __add_client(self):
        card = self.__client_card_entry.get()
        fam = self.__client_fam_entry.get()
        name = self.__client_name_entry.get()
        telephone = self.__client_telephone_entry.get()
        discount = self.__client_discount_entry.get()
        try:
            added_record = back.add_client(card, fam, name, telephone, discount)
            self.__clients_table.insert_row(idx=0, row=added_record, redraw=True)
            self.__clearing_entrys()
            self.__clients_table.deselect(row="all")
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")
        except mysql.connector.errors.IntegrityError:
            InformationDialog(
                self.master,
                "Некорректный ввод!",
                "Клиент с данным номером карты уже\nприсутствует в базе данных")
        except TypeError as current_error:
            if current_error.args[0] == "Incorrect card":
                info = "Некорректный формат номера карты. Он должен состоять из\n10 цифр!"
            elif current_error.args[0] == "Incorrect fam":
                info = "Некорректная длинна фамилии. Ее длинна должна быть\nне менее 2 и не более 30 символов!"
            elif current_error.args[0] == "Incorrect name":
                info = "Некорректная длинна имени. Его длинна должна быть\nне менее 2 и не более 30 символов!"
            elif current_error.args[0] == "Incorrect telephone":
                info = "Некорректный формат номера телефона!"
            elif current_error.args[0] == "Incorrect discount":
                info = "Некорректный формат скидки. Она должна являтся числом и \nсоставлять не менее 1 и не более 100 %."
            else:
                info = "Непредвиденная ошибка :("
            InformationDialog(self.master, "Некорректный ввод!", info)

    def __del_client(self):
        selected_table_row = self.__clients_table.get_selected_rows(return_tuple=True)
        if not selected_table_row:
            InformationDialog(
                self.master,
                "Ошибка!",
                "Ни одна строка таблицы не выбрана для удаления!")
            return 0
        selected_row = selected_table_row[0]
        card = self.__clients_table.get_row_data(r=selected_row)[0]
        dialog = ModalDialog(
            self.master,
            "Подтвердите действие.",
            f"Вы действительно хотите удалить выбранную в таблице запись?\nПри удалении данной записи будут также уделена вся информация о клиенте в\nзаписях о продажах."
        )
        dialog.wait_window()
        if dialog.modal_result:
            try:
                back.del_client(card)
                self.__clients_table.delete_row(selected_row, redraw=True)
                self.__clearing_entrys()
                self.__clients_table.deselect(row="all")
            except mysql.connector.errors.InterfaceError:
                InformationDialog(
                    self.master,
                    "Ошибка подключения к БД!",
                    "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

    def __update_client(self):
        selected_table_row = self.__clients_table.get_selected_rows(return_tuple=True)
        if not selected_table_row:
            InformationDialog(
                self.master,
                "Ошибка!",
                "Ни одна строка таблицы не выбрана для изменения!")
            return 0
        selected_row = selected_table_row[0]
        old_card = self.__clients_table.get_row_data(r=selected_row)[0]
        dialog = ModalDialog(
            self.master,
            "Подтвердите действие.",
            f"Вы действительно хотите изменить выбранную в таблице запись?\nНекоторые изменения могут отразиться на записях о\nпродажах."
        )
        dialog.wait_window()
        if dialog.modal_result:
            card = self.__client_card_entry.get()
            fam = self.__client_fam_entry.get()
            name = self.__client_name_entry.get()
            telephone = self.__client_telephone_entry.get()
            discount = self.__client_discount_entry.get()
            try:
                updated_record = back.update_client(old_card, card, fam, name, telephone, discount)
                self.__clients_table.delete_row(rows=selected_row)
                self.__clients_table.insert_row(idx=selected_row, row=updated_record, redraw=True)
                self.__clearing_entrys()
                self.__clients_table.deselect(row="all")
            except mysql.connector.errors.InterfaceError:
                InformationDialog(
                    self.master,
                    "Ошибка подключения к БД!",
                    "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")
            except mysql.connector.errors.IntegrityError:
                InformationDialog(
                    self.master,
                    "Некорректный ввод!",
                    "Клиент с данным номером карты уже\nприсутствует в базе данных")
            except TypeError as current_error:
                if current_error.args[0] == "Incorrect card":
                    info = "Некорректный формат номера карты. Он должен состоять из\n10 цифр!"
                elif current_error.args[0] == "Incorrect fam":
                    info = "Некорректная длинна фамилии. Ее длинна должна быть\nне менее 2 и не более 30 символов!"
                elif current_error.args[0] == "Incorrect name":
                    info = "Некорректная длинна имени. Его длинна должна быть\nне менее 2 и не более 30 символов!"
                elif current_error.args[0] == "Incorrect telephone":
                    info = "Некорректный формат номера телефона!"
                elif current_error.args[0] == "Incorrect discount":
                    info = "Некорректный формат скидки. Он должна являтся числом и \nсоставлять не менее 1 и не более 100 %."
                else:
                    info = "Непредвиденная ошибка :("
                InformationDialog(self.master, "Некорректный ввод!", info)

    def __find_client(self):
        try:
            finding_record = back.get_finding_clients(self.__found_entry.get())
            self.__updating_table_data(finding_record)
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")


