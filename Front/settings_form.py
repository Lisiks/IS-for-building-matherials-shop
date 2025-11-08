import customtkinter as ctk
import Back.backend_for_settings as back
import mysql.connector.errors

from Front.global_const import *
from Front.dialog_window import InformationDialog, ModalDialog
from Back.query_for_comboboxes_values import get_product_units, get_product_types


class SettingsForm(ctk.CTkFrame):
    def __init__(self, master, window_w, window_h):
        super().__init__(master=master)

        self.configure(fg_color=master.cget("fg_color"))

        head_font_size = round(CLASSIC_HEAD_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))
        font_size = round(CLASSIC_WIDGETS_FONT_SIZE * (window_w / CLASSIC_WINDOW_WIDTH))

        x_padding = round(2 * (window_w / CLASSIC_WINDOW_WIDTH))
        y_padding = round(6 * (window_h / CLASSIC_WINDOW_HEIGHT))

        widgets_w = window_w // 5
        widgets_h = window_h // 20

        self.__organization_name_entry = ctk.CTkEntry(
            master=self,
            width=widgets_w,
            height=widgets_h,
            font=("Arial", font_size),
            placeholder_text="Название: "
        )

        self.__organization_inn_entry = ctk.CTkEntry(
            master=self,
            width=widgets_w,
            height=widgets_h,
            font=("Arial", font_size),
            placeholder_text="ИНН: 0000000000"
        )

        self.__organization_ogrn_entry = ctk.CTkEntry(
            master=self,
            width=widgets_w,
            height=widgets_h,
            font=("Arial", font_size),
            placeholder_text="ОГРН: 0000000000000"
        )

        self.__organization_telephone_entry = ctk.CTkEntry(
            master=self,
            width=widgets_w,
            height=widgets_h,
            font=("Arial", font_size),
            placeholder_text="Тел: 0-000-000-00-00"
        )

        self.__organization_address_entry = ctk.CTkEntry(
            master=self,
            width=widgets_w,
            height=widgets_h,
            font=("Arial", font_size),
            placeholder_text="Адрес: "
        )

        self.__save_organization_data_button = ctk.CTkButton(
            master=self,
            text="Сохранить изменения",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            command=self.__saving_organization_data
        )

        ctk.CTkLabel(
            master=self,
            text="Настройки",
            font=("Arial", head_font_size),
        ).grid(row=0, column=0, sticky="w", padx=x_padding, pady=y_padding)

        ctk.CTkLabel(
            master=self,
            text="Название организации",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            anchor="sw"
        ).grid(row=1, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__organization_name_entry.grid(row=2, column=0, sticky="w", padx=x_padding, pady=y_padding)

        ctk.CTkLabel(
            master=self,
            text="ИНН",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            anchor="sw"
        ).grid(row=3, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__organization_inn_entry.grid(row=4, column=0, sticky="w", padx=x_padding, pady=y_padding)

        ctk.CTkLabel(
            master=self,
            text="ОГРН",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            anchor="sw"
        ).grid(row=5, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__organization_ogrn_entry.grid(row=6, column=0, sticky="w", padx=x_padding, pady=y_padding)

        ctk.CTkLabel(
            master=self,
            text="Телефон",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            anchor="sw"
        ).grid(row=7, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__organization_telephone_entry.grid(row=8, column=0, sticky="w", padx=x_padding, pady=y_padding)

        ctk.CTkLabel(
            master=self,
            text="Адрес",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            anchor="sw"
        ).grid(row=9, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__organization_address_entry.grid(row=10, column=0, sticky="w", padx=x_padding, pady=y_padding)
        self.__save_organization_data_button.grid(row=11, column=0, sticky="w", padx=x_padding, pady=y_padding)

        self.__product_types_combobox = ctk.CTkComboBox(
            master=self,
            width=widgets_w,
            height=widgets_h,
            font=("Arial", font_size),
        )

        self.__add_type_button = ctk.CTkButton(
            master=self,
            text="Добавить",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            command=self.__add_product_type
        )

        self.__del_type_button = ctk.CTkButton(
            master=self,
            text="Удалить",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            command=self.__del_product_type
        )

        ctk.CTkLabel(
            master=self,
            text="Тип товара",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            anchor="sw"
        ).grid(row=1, column=1, sticky="w", padx=x_padding, pady=y_padding)
        self.__product_types_combobox.grid(row=2, column=1, sticky="w", padx=x_padding, pady=y_padding)
        self.__add_type_button.grid(row=3, column=1, sticky="w", padx=x_padding, pady=y_padding)
        self.__del_type_button.grid(row=4, column=1, sticky="w", padx=x_padding, pady=y_padding)

        self.__product_unit_combobox = ctk.CTkComboBox(
            master=self,
            width=widgets_w,
            height=widgets_h,
            font=("Arial", font_size)
        )

        self.__add_unit_button = ctk.CTkButton(
            master=self,
            text="Добавить",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            command=self.__add_product_unit
        )

        self.__del_unit_button = ctk.CTkButton(
            master=self,
            text="Удалить",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            command=self.__del_product_unit
        )

        ctk.CTkLabel(
            master=self,
            text="Единица измерения",
            font=("Arial", font_size),
            width=widgets_w,
            height=widgets_h,
            anchor="sw"
        ).grid(row=1, column=2, sticky="w", padx=x_padding, pady=y_padding)
        self.__product_unit_combobox.grid(row=2, column=2, sticky="w", padx=x_padding, pady=y_padding)
        self.__add_unit_button.grid(row=3, column=2, sticky="w", padx=x_padding, pady=y_padding)
        self.__del_unit_button.grid(row=4, column=2, sticky="w", padx=x_padding, pady=y_padding)

        self.bind("<Map>", self.__on_form_show_actions)

    def __on_form_show_actions(self, _):
        self.__organization_name_entry.delete(0, ctk.END)
        self.__organization_inn_entry.delete(0, ctk.END)
        self.__organization_ogrn_entry.delete(0, ctk.END)
        self.__organization_telephone_entry.delete(0, ctk.END)
        self.__organization_address_entry.delete(0, ctk.END)

        try:
            org_data = back.get_organization_data()
            self.__organization_name_entry.insert(0, org_data["organization_name"])
            self.__organization_inn_entry.insert(0, org_data["organization_inn"])
            self.__organization_ogrn_entry.insert(0, org_data["organization_ogrn"])
            self.__organization_telephone_entry.insert(0, org_data["organization_telephone"])
            self.__organization_address_entry.insert(0, org_data["organization_address"])
        except FileNotFoundError:
            InformationDialog(
                self.master,
                "Ошибка чтения файла!",
                "Файл 'organization_data.json' был поврежден\n перемещен или утерян!"
            )

        self.__product_types_combobox.set("")
        self.__product_unit_combobox.set("")
        self.__product_types_combobox.configure(values=[])
        self.__product_types_combobox.configure(values=[])
        try:
            types_list = get_product_types()
            self.__product_types_combobox.configure(values=types_list)
            units_list = get_product_units()
            self.__product_unit_combobox.configure(values=units_list)
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")

    def __add_product_type(self):
        product_type = self.__product_types_combobox.get()
        try:
            back.add_product_type(product_type)
            self.__product_types_combobox.set("")

            values_list = list(self.__product_types_combobox.cget("values"))
            values_list.append(product_type)
            self.__product_types_combobox.configure(values=values_list)

        except TypeError as current_error:
            if current_error.args[0] == "Incorrect type length":
                info = "Длинна введенного типа должна быть не более 30\nи не менее 3 символов!"
            elif current_error.args[0] == "Existing type":
                info = "Данный тип уже присутствует в базе данных!"
            else:
                info = "Непредвиденная ошибка :("
            InformationDialog(self.master,"Некорректный ввод!", info)
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

    def __add_product_unit(self):
        product_unit = self.__product_unit_combobox.get()
        try:
            back.add_product_unit(product_unit)
            self.__product_unit_combobox.set("")
            values_list = list(self.__product_unit_combobox.cget("values"))
            values_list.append(product_unit)
            self.__product_unit_combobox.configure(values=values_list)
        except TypeError as current_error:
            if current_error.args[0] == "Incorrect unit length":
                info = "Длинна введенной единицы измерения должна быть не более 30\nи не менее 1 символа!"
            elif current_error.args[0] == "Existing unit":
                info = "Данная единица измерения уже присутствует в базе данных!"
            else:
                info = "Непредвиденная ошибка :("
            InformationDialog(self.master, "Некорректный ввод!", info)
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

    def __del_product_type(self):
        product_type = self.__product_types_combobox.get()
        try:
            dialog = ModalDialog(
                self.master,
                "Подтвердите действие.",
                f"Вы действительно хотите удалить тип '{product_type}'?\nПри его удалении будут также удалены все записи о товарах\nс данным типом."
            )
            dialog.wait_window()

            if dialog.modal_result:
                back.del_product_type(product_type)
                values_list = list(self.__product_types_combobox.cget("values"))
                values_list.remove(product_type)
                self.__product_types_combobox.configure(values=values_list)
                self.__product_types_combobox.set("")

        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")
        except TypeError:
            InformationDialog(
                self.master,
                "Некорректный ввод!",
                f"Тип '{product_type}' отсутствует в базе данных!'!")

    def __del_product_unit(self):
        product_unit = self.__product_unit_combobox.get()
        try:
            dialog = ModalDialog(
                self.master,
                "Подтвердите действие.",
                f"Вы действительно хотите единицу измерения '{product_unit}'?\nПри ее удалении будут также удалены все записи о товарах\nс данной единицей."
            )
            dialog.wait_window()

            if dialog.modal_result:
                back.del_product_unit(product_unit)
                values_list = list(self.__product_unit_combobox.cget("values"))
                values_list.remove(product_unit)
                self.__product_unit_combobox.configure(values=values_list)
                self.__product_unit_combobox.set("")
        except mysql.connector.errors.InterfaceError:
            InformationDialog(
                self.master,
                "Ошибка подключения к БД!",
                "Проверьте подключение к сети интернет\nлибо обратитесь к техническому специалисту!")
        except TypeError:
            InformationDialog(
                self.master,
                "Некорректный ввод!",
                f"Единица измерения '{product_unit}' отсутствует в базе данных!'!")

    def __saving_organization_data(self):
        org_name = self.__organization_name_entry.get()
        org_inn = self.__organization_inn_entry.get()
        org_ogrn = self.__organization_ogrn_entry.get()
        org_telephone = self.__organization_telephone_entry.get()
        org_address = self.__organization_address_entry.get()
        try:
            back.set_organization_data(org_name, org_inn, org_ogrn, org_telephone, org_address)
        except FileNotFoundError:
            InformationDialog(
                self.master,
                "Ошибка чтения файла!",
                "Файл 'organization_data.json' был поврежден\n перемещен или утерян!"
            )
        except TypeError as current_error:
            if current_error.args[0] == "Incorrect inn":
                info = "Некорректный формат ИНН!"
            elif current_error.args[0] == "Incorrect ogrn":
                info = "Некорректный формат ОГРН!"
            elif current_error.args[0] == "Incorrect telephone":
                info = "Некорректный формат номера телефона!"
            else:
                info = "Непредвиденная ошибка :("
            InformationDialog(self.master, "Некорректный ввод!", info)
