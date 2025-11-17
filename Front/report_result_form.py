import customtkinter as ctk
from tksheet import Sheet
from Front.global_const import *


class RepostResultForm(ctk.CTkFrame):
    def __init__(self, master, window_w, window_h, report_header, table_headers):
        super().__init__(master)
        self.configure(fg_color=master.cget("fg_color"))

        self.__table_headers = table_headers

        self.__table_width = window_w - (window_w // 4) - 60
        self.__table_height = window_h - (window_h // 4) - 60

        self.__table_column_width = int(self.__table_width // len(table_headers))
        self.__table_row_height = int(self.__table_height // 9)

        self.__head_font_size = round(CLASSIC_HEAD_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))
        self.__font_size = round(CLASSIC_WIDGETS_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))
        self.__table_font_size = (round(CLASSIC_TABLE_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH)))

        ctk.CTkLabel(
            master=self,
            text=report_header,
            font=("Arial", self.__head_font_size)
        ).grid(row=0, column=0, sticky="w", pady=2, padx=3)

        self.__table_frame = ctk.CTkFrame(master=self, fg_color="#313131", corner_radius=10, width=self.__table_width, height=self.__table_height)
        self.__table_frame.grid(row=1, column=0, sticky="w", pady=2, padx=3)

    def load_report_data(self, data):
        report_table = Sheet(
            self.__table_frame,
            show_x_scrollbar=False,
            show_y_scrollbar=False,

            width=self.__table_width,
            height=self.__table_height,
            header_height=self.__table_row_height,
            row_height=self.__table_row_height,

            header_align="c",
            align="c",

            header_bg="#313131",
            header_selected_cells_bg="#313131",
            table_bg="#404040",

            headers=self.__table_headers,
            header_font=("Arial", self.__table_font_size, "bold"),
            header_selected_cells_fg="white",
            header_fg="white",

            font=("Arial", self.__table_font_size, "normal"),
            table_fg="white",
            data=data,

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
        report_table.set_all_column_widths(self.__table_column_width)
        report_table.grid(row=0, column=0, sticky="w", pady=7)