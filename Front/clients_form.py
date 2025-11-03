import customtkinter as ctk
import CTkTable
from global_const import *


class ClientsForm(ctk.CTkFrame):
    def __init__(self, master, window_w, window_h):
        super().__init__(master)
        self.configure(fg_color=master.cget("fg_color"))

        scrollbar_frame_width = window_w - (window_w // 4) - 60
        scrollbar_frame_height = window_h - (window_h // 2.7) - 60

        all_table_width = scrollbar_frame_width - 20
        all_table_height = scrollbar_frame_height - 20

        cell_table_height = all_table_height // 7

        table_width_percentage = all_table_width / 100

        head_font_size = round(CLASSIC_HEAD_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))
        font_size = round(CLASSIC_WIDGETS_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))
        table_font_size = (round(CLASSIC_TABLE_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH)))

        self.__found_frame = self.__create_found_frame(
            button_w=scrollbar_frame_width // 6,
            button_h=window_h // 20,
            entry_w=scrollbar_frame_width // 6 * 5,
            entry_h=window_h // 20,
            font_size=font_size
        )

        self.__creating_frame = self.__create_creation_frame(
            client_card_entry_w=round(30 * table_width_percentage),
            client_fam_entry_w=round(20 * table_width_percentage),
            client_name_entry_w=round(20 * table_width_percentage),
            client_telephone_entry_w=round(20 * table_width_percentage),
            client_discount_entry_w=round(10 * table_width_percentage),
            entryes_h=window_h // 20,
            font_size=font_size,
        )

        self.__crud_frame = self.__create_crud_frame(
            button_w=scrollbar_frame_width // 3 - 20,
            button_h=window_h // 20,
            font_size=font_size
        )

        self.__table_frame = ctk.CTkScrollableFrame(
            master=self,
            width=scrollbar_frame_width,
            height=scrollbar_frame_height,
            fg_color=self.cget("fg_color")
        )

        self.__clients_table = CTkTable.CTkTable(
            master=self.__table_frame,
            values=[["№ дисконтной карты клиента", "Фамилия", "Имя", "Телефон", "Скидка"]],
            row=12,
            column=5,
            height=cell_table_height,
            font=("Arial", table_font_size)

        )

        self.__clients_table.edit_row(0, font=("Arial", font_size))
        self.__clients_table.edit_column(0, width=round(30 * table_width_percentage))
        self.__clients_table.edit_column(1, width=round(20 * table_width_percentage))
        self.__clients_table.edit_column(2, width=round(20 * table_width_percentage))
        self.__clients_table.edit_column(3, width=round(20 * table_width_percentage))
        self.__clients_table.edit_column(4, width=round(10 * table_width_percentage))

        ctk.CTkLabel(
            master=self.__table_frame,
            text="Клиенты",
            font=("Arial", font_size + 3),
            anchor="center"
        ).grid(row=0, column=0, padx=3, pady=3)

        self.__clients_table.grid(row=1, column=0, padx=3, pady=3)

        ctk.CTkLabel(
            master=self,
            text="Клиенты",
            font=("Arial", head_font_size)
        ).grid(row=0, column=0, sticky="w", pady=3, padx=2)

        self.__found_frame.grid(row=1, column=0, sticky="w", pady=3, padx=2)
        self.__creating_frame.grid(row=2, column=0, sticky="w", pady=3, padx=2)
        self.__table_frame.grid(row=3, column=0, pady=3, padx=2)
        self.__crud_frame.grid(row=4, column=0, sticky="w", pady=3, padx=2)

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
            font=("Arial", font_size)
        )

        self.__client_fam_entry = ctk.CTkEntry(
            master=creating_frame,
            width=client_fam_entry_w,
            height=entryes_h,
            font=("Arial", font_size)
        )

        self.__client_name_entry = ctk.CTkEntry(
            master=creating_frame,
            width=client_name_entry_w,
            height=entryes_h,
            font=("Arial", font_size)
        )

        self.__client_telephone_entry = ctk.CTkEntry(
            master=creating_frame,
            width=client_telephone_entry_w,
            height=entryes_h,
            font=("Arial", font_size)
        )

        self.__client_discount_entry = ctk.CTkEntry(
            master=creating_frame,
            width=client_discount_entry_w,
            height=entryes_h,
            font=("Arial", font_size)
        )

        self.__client_card_entry.grid(row=1, column=0, padx=2)
        self.__client_fam_entry.grid(row=1, column=1, padx=2)
        self.__client_name_entry.grid(row=1, column=2, padx=2)
        self.__client_telephone_entry.grid(row=1, column=3, padx=2)
        self.__client_discount_entry.grid(row=1, column=4, padx=2)

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
            text="Поиск",
            width=button_w,
            height=button_h,
            font=("Arial", font_size)
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
            font=("Arial", font_size)
        )

        self.__del_button = ctk.CTkButton(
            master=crud_frame,
            text="Удалить",
            width=button_w,
            height=button_h,
            font=("Arial", font_size)
        )

        self.__change_button = ctk.CTkButton(
            master=crud_frame,
            text="Изменить",
            width=button_w,
            height=button_h,
            font=("Arial", font_size)
        )

        self.__add_button.grid(row=0, column=0, padx=2)
        self.__del_button.grid(row=0, column=1, padx=2)
        self.__change_button.grid(row=0, column=2, padx=2)

        return crud_frame


