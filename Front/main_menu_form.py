import customtkinter as ctk
from Front.global_const import *
from Front.settings_form import SettingsForm


class MainMenuForm(ctk.CTkFrame):
    def __init__(self, master, window_w, window_h):
        super().__init__(master)
        self.configure(fg_color=master.cget("fg_color"))

        head_font_size = round(CLASSIC_HEAD_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))
        font_size = round(CLASSIC_WIDGETS_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))

        x_padding = 2
        y_padding = 6

        ctk.CTkLabel(
            master=self,
            text="Главная",
            font=("Arial", head_font_size)
        ).grid(row=0, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__settings_form = SettingsForm(master, window_w, window_h)

        self.__settings_button = ctk.CTkButton(
            master=self,
            text="Настройки",
            command=lambda: master.change_form(self.__settings_form)
        )

        self.__settings_button.grid(row=1, column=0)




