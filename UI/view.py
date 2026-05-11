import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Tdp flights manager 2026"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_Cmin = None
        self.btn_analizzaAer = None

        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # title
        self._title = ft.Text("Tdp flights manager 2026", color="blue", size=24)
        self._page.controls.append(self._title)



        #ROW with some controls
        # text field for the name
        self.txt_Cmin = ft.TextField(
            label="N min compagnie",
            width=200,

        )

        # button for the "hello" reply
        self.btn_analizzaAer = ft.ElevatedButton(text="Analizza Aeroporti", on_click=self._controller.handleanalizza)
        row1 = ft.Row([self.txt_Cmin, self.btn_analizzaAer],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        self._ddAeroportoP=ft.Dropdown(label="Aeroporto di Partenza")
        self._btnAeroportiConnessi=ft.ElevatedButton(text="Aeroporti Connessi", on_click=self._controller.handleAerConnessi)
        row2=ft.Row([self._ddAeroportoP, self._btnAeroportiConnessi],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        self._ddAeroportoA=ft.Dropdown(label="Aeroporto di Arrivo")
        self._txtTratteMax=ft.TextField(label="Num tratte Max")
        self._btnCercaItinerario=ft.ElevatedButton(text="Cerca itinerario", on_click=self._controller.handlecerca)

        row3=ft.Row([self._ddAeroportoA, self._txtTratteMax, self._btnAeroportiConnessi],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)


        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
