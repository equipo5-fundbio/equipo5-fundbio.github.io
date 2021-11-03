from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.tab import MDTabsBase
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from kivy.clock import Clock
from serial_com import SerialCom
from functools import partial

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineIconListItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel

class ItemSelect(TwoLineIconListItem):
    def setter(self, instance_check):
        self.set_icon(instance_check)
        self.set_actual_port()
        
    
    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False
    
    def set_actual_port(self):
        self.app = MDApp.get_running_app()
        self.app.ser_com.actual_port = self.text
        if self.app.ser_com.actual_port:
            self.app.root.get_screen("data_reading_window").ids.start_test_button.disabled = False

class ConnectionDialog(MDDialog):
    def on_open(self):
        if not self.items:
            self.title = "No se encontraron puertos disponibles, verifique que el dispositivo esté encendido."
        else:
            self.title = "Seleccionar puerto de comunicación"
        return super().on_open()

class TestDialog(MDDialog):
    def on_pre_dismiss(self):
        self.app = MDApp.get_running_app()
        self.screen = MDApp.get_running_app().root.get_screen("data_reading_window")
        self.screen.enable_buttons_back()
        self.screen.reception_event.cancel()
        #self.app.ser_com.arduino_ser.close()
        print("done")
        return super().on_pre_dismiss()

class LoginWindow(Screen):
    pass

class MainWindow(Screen):
    pass

class TreatmentWindow(Screen):
    pass

class DataReadingWindow(Screen):
    con_dialog = None
    test_dialog = None

    def start_connection(self):
        self.app = MDApp.get_running_app()
        self.app.ser_com.update_ports()
        ports = self.app.ser_com.port_list
        
        # Datos de prueba (para uso de depuracion):
        ports = [
            "COM2 - Communications Port (COM2)", 
            "COM1 - ELTIMA Virtual Serial Port (COM1->COM5)",
            "COM5 - ELTIMA Virtual Serial Port (COM5->COM1)"
        ]

        self.items_list = []
        self.list_port_items(ports)

        if not self.con_dialog:
            self.con_dialog = ConnectionDialog(
                title="Seleccionar puerto de comunicación",
                radius=[20, 7, 20, 7],
                type="confirmation",
                items=self.items_list,
                buttons=[
                    MDFlatButton(
                        text="CANCELAR",
                        theme_text_color="Custom",
                        text_color= MDApp.get_running_app().theme_cls.primary_dark,
                    ),
                    MDFlatButton(
                        text="CONFIRMAR",
                        theme_text_color="Custom",
                        text_color= MDApp.get_running_app().theme_cls.primary_dark,
                    ),
                ]
            )
        
        self.con_dialog.open()
    
    def list_port_items(self, ports):
        for port in ports:
            text_pair = port.split(" ", 1)
            item = ItemSelect(text=text_pair[0], secondary_text=text_pair[1])
            self.items_list.append(item)

    def start_test(self):
        self.data_list = []
        
        if not self.test_dialog:
            self.button_list = [MDFillRoundFlatButton(
            text=f"Sensor {i}",
            theme_text_color="Custom",
            disabled = False,
            md_bg_color= MDApp.get_running_app().theme_cls.primary_dark,
            ) for i in range(3)]

            self.test_dialog = TestDialog(
                title="Seleccione donde quiere realizar el test:",
                radius=[20, 7, 20, 7],
                buttons=self.button_list
            )

            self.button_list[0].bind(on_release=partial(self.read_sensor, "a"))
            self.button_list[1].bind(on_release=partial(self.read_sensor, "b"))
            self.button_list[2].bind(on_release=partial(self.read_sensor, "c"))

        self.test_dialog.open()
        
    
    def enable_buttons_back(self):
        for i in range(len(self.button_list)):
                self.button_list[i].disabled = False
        

    def read_sensor(self, command, instance):
        for i in range(len(self.button_list)):
                self.button_list[i].disabled = True
        
        self.app = MDApp.get_running_app()
        print("Connecting to",self.app.ser_com.actual_port)
        self.test_dialog.title = "Espere mientras se leen los datos..."
        #self.app.ser_com.open_and_write(command)
        print("Sending command")
        self.reception_event = Clock.schedule_interval(partial(self.data_reception, self.data_list), 0.2)


    def data_reception(self, data_list, *largs):
        print("Reading")
        #self.do_reception = self.app.ser_com.receive_data(data_list)
        #if not self.do_reception:
            #self.app.ser_com.arduino_ser.close()
            #return False


class DataHistoryWindow(Screen):
    
    def on_enter(self, *args):
        self.create_plot()
        box = self.ids.graphics_box
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def create_plot(self):
        x = [i for i in range(30)]
        y = [100,120,90,150,120]
        y *= 6
        figure(tight_layout=True)
        plt.plot(x, y)

        plt.ylabel("Fuerza ejercida en N")
        plt.xlabel("Tiempo en días")

class WindowManager(ScreenManager):
    pass

class LoginTab(BoxLayout, MDTabsBase):
    pass

class RegisterTab(BoxLayout, MDTabsBase):
    pass


Window.size = (360, 640)

class TaniWasaApp(MDApp): # Hereda los métodos de la clase App de kivy (como run())
    
    ser_com = SerialCom()

    def return_main(self):
        self.root.current = "main_window"
        self.root.get_screen("login_window").manager.transition.direction = "right"

    def build(self): # Interfaz de la app
        kv_file = Builder.load_file('main.kv')
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Cyan"
        return kv_file
    
    def on_start(self):
        self.root.get_screen("login_window").ids.tabs.add_widget(LoginTab(text = "[font=Candara]Iniciar Sesión[/font]"))
        self.root.get_screen("login_window").ids.tabs.add_widget(RegisterTab(text = "[font=Candara]Registrarse[/font]"))

if __name__ == "__main__":
    TaniWasaApp().run() # Llama run sobre una instancia de MyApp