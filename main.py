import customtkinter as ctk


CLASSIC_WINDOW_WIDTH = 1980
CLASSIC_WINDOW_HEIGHT = 1080


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.w = self.winfo_screenwidth()
        self.h = self.winfo_screenheight()
        self.after(0, lambda: self.state('zoomed'))
        self.title("Информационная система для строительного магазина")

        self.navigation_panel = self.__NavigationPanel(self, self.w, self.h)
        self.navigation_panel.grid(row=0, column=0)

    def run(self):
        self.mainloop()

    class __NavigationPanel(ctk.CTkFrame):
        __CLASSIC_FONT_SIZE = 30

        def __init__(self, master, window_w, window_h):
            super().__init__(master)
            self.configure(fg_color="#3F48CC", corner_radius=0, width=window_w)

            font_size = int(self.__CLASSIC_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))
            buttons_h = (window_h - 65) // 9
            buttons_w = buttons_h * 4

            self.__main_menu_button = ctk.CTkButton(
                master=self,
                text="ИС",
                font=("Times new roman", font_size + 20),
                width=buttons_w,
                height=buttons_h,
                corner_radius=0
            )

            self.__fin_operation_button = ctk.CTkButton(
                master=self,
                text="Финансовые операции",
                font=("Arial", font_size),
                width=buttons_w,
                height=buttons_h,
                corner_radius=0
            )

            self.__nomenclature_button = ctk.CTkButton(
                master=self,
                text="Номенклатура",
                font=("Arial", font_size),
                width=buttons_w,
                height=buttons_h,
                corner_radius=0
            )

            self.__sales_button = ctk.CTkButton(
                master=self,
                text="Продажи",
                font=("Arial", font_size),
                width=buttons_w,
                height=buttons_h,
                corner_radius=0
            )

            self.__purchases_button = ctk.CTkButton(
                master=self,
                text="Закупки",
                font=("Arial", font_size),
                width=buttons_w,
                height=buttons_h,
                corner_radius=0
            )

            self.__write_offs_button = ctk.CTkButton(
                master=self,
                text="Списания",
                font=("Arial", font_size),
                width=buttons_w,
                height=buttons_h,
                corner_radius=0
            )

            self.__suppliers_offs_button = ctk.CTkButton(
                master=self,
                text="Поставщики",
                font=("Arial", font_size),
                width=buttons_w,
                height=buttons_h,
                corner_radius=0
            )

            self.__clients_offs_button = ctk.CTkButton(
                master=self,
                text="Клиенты",
                font=("Arial", font_size),
                width=buttons_w,
                height=buttons_h,
                corner_radius=0
            )

            self.__reports_offs_button = ctk.CTkButton(
                master=self,
                text="Отчеты",
                font=("Arial", font_size),
                width=buttons_w,
                height=buttons_h,
                corner_radius=0
            )

            self.__main_menu_button.grid(row=0, column=0)
            self.__fin_operation_button.grid(row=1, column=0)
            self.__nomenclature_button.grid(row=2, column=0)
            self.__sales_button.grid(row=3, column=0)
            self.__purchases_button.grid(row=4, column=0)
            self.__write_offs_button.grid(row=5, column=0)
            self.__suppliers_offs_button.grid(row=6, column=0)
            self.__clients_offs_button.grid(row=7, column=0)
            self.__reports_offs_button.grid(row=8, column=0)


my_application = Application()
if __name__ == '__main__':
    my_application.run()
