import customtkinter as ctk


class InformationDialog(ctk.CTkToplevel):
    def __init__(self, main, tittle, information):
        super().__init__(main)
        self.configure()
        self.title(tittle)
        self.grab_set()
        ctk.CTkLabel(
            master=self,
            text=information,
            font=("Arial", 20),
            justify="left"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=10, columnspan=2)

        ctk._ok_button = ctk.CTkButton(
            master=self,
            text="Ок",
            font=("Arial", 20),
            width=300,
            height=30,
            command=self._ok_command
        ).grid(row=1, column=0, padx=5, pady=10,  sticky="w")

    def _ok_command(self):
        self.destroy()


class ModalDialog(InformationDialog):
    def __init__(self, main, tittle, information):
        super().__init__(main, tittle, information)
        self.modal_result = False

        self._cancel_button = ctk.CTkButton(
            master=self,
            text="Отмена",
            font=("Arial", 20),
            width=300,
            height=30,
            command=self._cancel_command
        ).grid(row=1, column=1, padx=5, pady=10,  sticky="w")

    def _cancel_command(self):
        super()._ok_command()

    def _ok_command(self):
        self.modal_result = True
        super()._ok_command()


