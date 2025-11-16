import customtkinter as ctk
from tksheet import Sheet
from Front.global_const import *


class RepostResultForm(ctk.CTkFrame):
    def __init__(self, master, window_w, window_h, report_header, table_headers):
        super().__init__(master)
        self.configure(fg_color=master.cget("fg_color"))

        table_width = window_w - (window_w // 4) - 60
        table_height = window_h - (window_h // 4) - 60

        self.__table_column_width = int(table_width // len(table_headers))
        table_row_height = int(table_height // 7)

        head_font_size = round(CLASSIC_HEAD_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))
        font_size = round(CLASSIC_WIDGETS_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))
        table_font_size = (round(CLASSIC_TABLE_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH)))

        ctk.CTkLabel(
            master=self,
            text=report_header,
            font=("Arial", head_font_size)
        ).grid(row=0, column=0, sticky="w", pady=2, padx=3)

        self.__table_frame = ctk.CTkFrame(master=self, fg_color="#313131", corner_radius=10)

        self.__report_table = Sheet(
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
        self.__table_frame.grid(row=1, column=0, sticky="w", pady=2, padx=3)
        self.__report_table.grid(row=0, column=0, sticky="w", pady=3, padx=0)

        self.__report_table.headers(table_headers)
        self.__report_table.set_all_column_widths(self.__table_column_width)

    def load_report_data(self, data):
        self.__report_table.set_data(data)
        self.__report_table.set_all_column_widths(self.__table_column_width)