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
import database as db


from datetime import date
from datetime import datetime
from datetime import timedelta
import json
from collections.abc import Iterable

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineIconListItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel

class ConnectItemSelect(TwoLineIconListItem):
    """Administra métodos respecto al diálogo de selección de puerto de comunicación."""

    def setter(self, instance_check):
        """Establece el ícono correcto y almacena el puerto actual."""
        self.set_icon(instance_check)
        self.set_actual_port()
    
    def set_icon(self, instance_check):
        """Marca la casilla de check con su selección."""
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False
    
    def set_actual_port(self):
        """Establece el puerto actual como el seleccionado."""
        self.app = MDApp.get_running_app()
        self.app.ser_com.actual_port = self.text

        if self.app.ser_com.actual_port:
            self.screen = self.app.root.get_screen("data_reading_window")
            self.screen.ids.start_test_button.disabled = False 
            self.t_screen = self.app.root.get_screen("treatment_window")
            self.t_screen.ids.start_treatment_button.disabled = False 
            # Habilita el botón para iniciar tests.

class ConnectionDialog(MDDialog):
    """Administra métodos respecto a el diálogo de conección de puertos."""

    def on_open(self):
        """Procedimientos a realizar al abrir el diálogo."""
        if not self.items:
            self.title = "No se encontraron puertos disponibles, verifique que el dispositivo esté encendido."
        else:
            self.title = "Seleccionar puerto de comunicación"
        return super().on_open()

class TestDialog(MDDialog):
    """Administra métodos respecto al diálogo de 'test de lectura de datos'."""

    def on_pre_dismiss(self):
        """Procedimientos a realizar antes de cerrar el diálogo."""
        self.app = MDApp.get_running_app()
        self.screen = MDApp.get_running_app().root.get_screen("data_reading_window")
        self.screen.enable_buttons_back() # Rehabilitar los botones del diálogo.
        if self.screen.reception_event:
            self.screen.reception_event.cancel() # Terminar bucle de lectura.
        #self.screen.data_list = [20, 16, 14]
        #self.screen.save_data(self.screen.data_list) # Datos de prueba para probar el almacenamiento
        #self.app.ser_com.arduino_ser.close() # Cerrar la instancia de serial.
        print("done")
        return super().on_pre_dismiss()

class TreatmentDialog(MDDialog):
    
    def on_pre_dismiss(self):
        self.screen = MDApp.get_running_app().root.get_screen("treatment_window")
        self.screen.enable_buttons_back() # Rehabilitar los botones del diálogo.
        if self.screen.reception_event:
            self.screen.reception_event.cancel() # Terminar bucle de lectura.
        return super().on_pre_dismiss()


class LoginWindow(Screen):
    pass

class MainWindow(Screen):

    data_history_dialog = None

    def select_sensor_graphs(self):

        if not self.data_history_dialog:

            # Crear 3 botones.
            self.button_list = [MDFillRoundFlatButton(
            text=f"Punto {i+1}",
            theme_text_color="Custom",
            disabled = False,
            md_bg_color= MDApp.get_running_app().theme_cls.primary_dark,
            ) for i in range(3)]

            # Crear el diálogo.
            self.data_history_dialog = MDDialog(
                title="Seleccione cual historial de datos quiere ver:",
                radius=[20, 7, 20, 7],
                buttons=self.button_list
            )

            # Asignar funciones a los botones.
            self.button_list[0].bind(on_release=partial(self.show_sensor_data, 0))
            self.button_list[1].bind(on_release=partial(self.show_sensor_data, 1))
            self.button_list[2].bind(on_release=partial(self.show_sensor_data, 2))
        
        self.data_history_dialog.open()
    
    def show_sensor_data(self, sensor_num, instance):
        self.app = MDApp.get_running_app()
        self.app.current_sensor_data = sensor_num
        
        self.app.root.current = "data_history_window"
        self.app.root.get_screen("login_window").manager.transition.direction = "left"
        self.data_history_dialog.dismiss()
    
    def update_data(self):
        self.new_user_data = [
            "",
            self.ids.user_name.text,
            self.ids.user_last_name.text,
            self.ids.user_email.text,
            "",
            self.ids.user_phone_number.text,
            self.ids.user_birth_date.text,
            self.ids.user_sex.text,
            self.ids.user_birth_place.text,
            self.ids.user_weight.text,
            self.ids.user_height.text,
            self.ids.user_health_center.text,
            self.ids.user_risser_index.text,
            self.ids.user_comorbilities.text,
            "",
            "",
            ""
        ]
        self.app = MDApp.get_running_app()

        for i in range(len(self.new_user_data)):
            if self.new_user_data[i] != "":
                self.app.current_user_data[i] = self.new_user_data[i]
        
        db.edit_patient(*self.app.current_user_data)


class TreatmentWindow(Screen):
    
    treatment_dialog = None

    def start_treatment(self):

        if not self.treatment_dialog:

            # Crear 3 botones.
            self.button_list = [MDFillRoundFlatButton(
            text=f"Punto {i+1}",
            theme_text_color="Custom",
            disabled = False,
            md_bg_color= MDApp.get_running_app().theme_cls.primary_dark,
            ) for i in range(3)]

            # Crear el diálogo.
            self.treatment_dialog = TreatmentDialog(
                title="Seleccione donde quiere aplicar presión:",
                radius=[20, 7, 20, 7],
                buttons=self.button_list
            )

            # Asignar funciones a los botones.
            self.button_list[0].bind(on_release=partial(self.activate_pump, "d"))
            self.button_list[1].bind(on_release=partial(self.activate_pump, "e"))
            self.button_list[2].bind(on_release=partial(self.activate_pump, "f"))

        self.treatment_dialog.open()

    def enable_buttons_back(self):
        for i in range(len(self.button_list)):
                self.button_list[i].disabled = False

    def activate_pump(self, command, instance):
        self.current_pump = ord(command) - 99
        for i in range(len(self.button_list)):
                self.button_list[i].disabled = True
        
        self.pressure_data = self.get_pressure()

        self.app = MDApp.get_running_app()
        print("Connecting to",self.app.ser_com.actual_port)
        self.treatment_dialog.title = "Espere..."
        #self.app.ser_com.open_and_write(command)
        #self.app.ser_com.arduino_ser.write(bytes(self.pressure_data,'utf-8'))
        self.reception_event = Clock.schedule_interval(
            self.data_reception, 0.2) # Iniciar bucle de lectura
    
    def data_reception(self, *largs):
        """Lectura de una línea de datos."""
        #self.do_reception = self.app.ser_com.receive_data(data_list)
        #self.treatment_dialog.title = f"La presión actual es {self.app.ser_com.actual_pressure_val}"
        #if not self.do_reception:
            #self.app.ser_com.arduino_ser.close()
            #self.enable_buttons_back()
            #return False
    
    def get_pressure(self):
        self.app = MDApp.get_running_app()
        db_data = self.app.current_user_data

        pump_pressures = json.loads(db_data[16])
        pump_pressure_data = pump_pressures[str(self.current_pump)]

        return pump_pressure_data


class DataReadingWindow(Screen):
    """Administrar la ventana de lectura de datos."""

    # Diálogos para los botones.
    con_dialog = None
    test_dialog = None

    def start_connection(self):
        """Buscar los puertos disponibles y mostrarlos en un diálogo."""

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
        """Incluir los puertos en una pantalla de selección."""
        for port in ports:
            text_pair = port.split(" ", 1)
            item = ConnectItemSelect(text=text_pair[0], secondary_text=text_pair[1])
            self.items_list.append(item)

    def start_test(self):
        """Mostrar un diálogo con los botones de selección de sensor para lectura."""
        self.data_list = []
        
        if not self.test_dialog:

            # Crear 3 botones.
            self.button_list = [MDFillRoundFlatButton(
            text=f"Sensor {i+1}",
            theme_text_color="Custom",
            disabled = False,
            md_bg_color= MDApp.get_running_app().theme_cls.primary_dark,
            ) for i in range(3)]

            # Crear el diálogo.
            self.test_dialog = TestDialog(
                title="Seleccione donde quiere realizar el test:",
                radius=[20, 7, 20, 7],
                buttons=self.button_list
            )

            # Asignar funciones a los botones.
            self.button_list[0].bind(on_release=partial(self.read_sensor, "a"))
            self.button_list[1].bind(on_release=partial(self.read_sensor, "b"))
            self.button_list[2].bind(on_release=partial(self.read_sensor, "c"))

        self.test_dialog.open()
    
    def enable_buttons_back(self):
        """Rehabilitar los botones de lectura."""
        for i in range(len(self.button_list)):
                self.button_list[i].disabled = False

    def read_sensor(self, command, instance):
        """Leer el sensor seleccionado."""
        self.current_sensor = ord(command) - 96
        for i in range(len(self.button_list)):
                self.button_list[i].disabled = True
        
        self.app = MDApp.get_running_app()
        print("Connecting to",self.app.ser_com.actual_port)
        self.test_dialog.title = "Espere mientras se leen los datos..."
        #self.app.ser_com.open_and_write(command)
        print("Sending command")
        self.reception_event = Clock.schedule_interval(
            partial(self.data_reception, self.data_list), 0.2) # Iniciar bucle de lectura

    def data_reception(self, data_list, *largs):
        """Lectura de una línea de datos."""
        print("Reading")
        #self.do_reception = self.app.ser_com.receive_data(data_list)
        #if not self.do_reception:
            #self.app.ser_com.arduino_ser.close()
            #self.save_data(data_list)
            #self.enable_buttons_back()
            #self.test_dialog.title = "Los datos se han almacenado con éxito." 
            #return False
    
    def save_data(self, data_list):
        pressure_num = sum(data_list)/(len(data_list))
        today = date.today()
        today_str = today.strftime("%d/%m/%Y")

        self.app = MDApp.get_running_app()
        db_data = self.app.current_user_data

        sensor_data_list = json.loads(db_data[15])
        sensor_data = sensor_data_list[self.current_sensor-1]
        sensor_data[today_str] = pressure_num

        json_str = json.JSONEncoder().encode(sensor_data_list)
        self.app.current_user_data[15] = json_str
        db.edit_patient(*self.app.current_user_data)

class DataHistoryWindow(Screen):
    
    def on_enter(self, *args):
        self.ids.graphics_box.clear_widgets()
        self.create_plot()
        box = self.ids.graphics_box
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

    def create_plot(self):
        self.app = MDApp.get_running_app()

        current_sensor = self.app.current_sensor_data
        self.ids.data_history_label.text = f"Gráfica fuerza vs tiempo del punto{current_sensor+1}"
        db_data = self.app.current_user_data
        sensor_data_list = json.loads(db_data[15])
        sensor_data = sensor_data_list[current_sensor]

        dates_str = sensor_data.keys()
        dates_obj = [datetime.strptime(i, "%d/%m/%Y") for i in dates_str]
        min_date = min(dates_obj)
        dates_obj.sort()
        y = [sensor_data[one_date.strftime("%d/%m/%Y")] for one_date in dates_obj]
        x = [(one_date - min_date).days for one_date in dates_obj]

        figure(tight_layout=True)
        plt.plot(x, y)

        plt.ylabel("Fuerza ejercida en N")
        plt.xlabel("Tiempo en días")

class WindowManager(ScreenManager):
    pass

class LoginTab(BoxLayout, MDTabsBase):
    
    patient_dialog = None

    def login(self):
        dni = self.ids.user_login_dni.text
        pwd = self.ids.user_login_password.text

        info = list(db.patient_info(dni)) if isinstance(db.patient_info(dni), Iterable) else None
        if info != None:
            if pwd == info[4]:
                self.app = MDApp.get_running_app()
                self.app.current_user_data = info
                self.app.current_medic_data = db.medic_info(info[14])
                self.app.root.get_screen("login_window").manager.transition.direction = "left"
                self.app.root.current = "main_window"
            else:
                print("Contraseña incorrecta")
        else:
            info = list(db.medic_info(dni)) if isinstance(db.medic_info(dni), Iterable) else None
            if info != None:
                if pwd == info[4]:
                    self.app = MDApp.get_running_app()
                    self.app.current_medic_data = info
                    self.disable_buttons_medic()
                    self.open_choosing_dialog()
                    self.app.root.get_screen("login_window").manager.transition.direction = "left"
                    self.app.root.current = "main_window"
                else:
                    print("Contraseña incorrecta")
            else:
                print("El DNI no está registrado")
    
    def disable_buttons_medic(self):
        self.screen = self.app.root.get_screen("data_reading_window")
        self.screen.ids.start_test_button.disabled = True
        self.screen.ids.establish_connection_button.disabled = True

        self.t_screen = self.app.root.get_screen("treatment_window")
        self.t_screen.ids.start_treatment_button.disabled = True
        self.t_screen.ids.force_to_exert.disabled = False
        self.t_screen.ids.use_time.disabled = False
        self.t_screen.ids.finish_time.disabled = False
    
    def open_choosing_dialog(self):
        if not self.patient_dialog:
            
            self.patients = db.patients_from_medic(self.app.current_medic_data[0])

            self.button_list = [MDFillRoundFlatButton(
            text=f"{patient[0]}",
            theme_text_color="Custom",
            disabled = False,
            md_bg_color= MDApp.get_running_app().theme_cls.primary_dark,
            ) for patient in self.patients]

            # Crear el diálogo.
            self.patient_dialog = MDDialog(
                title="Seleccione cual paciente supervisará:",
                radius=[20, 7, 20, 7],
                buttons=self.button_list
            )
            i=0
            for button in self.button_list:
                button.bind(on_release=partial(self.choose_patient, i))
                i+=1
        
        self.patient_dialog.open()
    
    def choose_patient(self, num, instance):
        self.app.current_user_data = self.patients[num]
        self.patient_dialog.dismiss()
            
class RegisterTab(BoxLayout, MDTabsBase):
    
    def register(self):
        self.user_data = [
            self.ids.user_dni.text,
            self.ids.user_name.text,
            self.ids.user_last_name.text,
            self.ids.user_email.text,
            self.ids.user_password.text,
            self.ids.user_phone_number.text,
            self.ids.user_birth_date.text,
            self.ids.user_sex.text,
            self.ids.user_birth_place.text,
            self.ids.user_weight.text,
            self.ids.user_height.text,
            self.ids.user_health_center.text,
            self.ids.user_risser_index.text,
            self.ids.user_comorbilities.text,
            self.ids.user_medic_dni.text,
            "[{},{},{}]",
            "{}"
        ]

        if self.confirm_register(): 
            db.new_patient(*self.user_data)
        else:
            print("Las contraseñas no coinciden")
    
    def confirm_register(self):
        pwd_equal = self.ids.user_password.text == self.ids.user_password_confirmation.text
        return pwd_equal

class RegisterMedicTab(BoxLayout, MDTabsBase):
    def register_medic(self):
        self.medic_data = [
            self.ids.medic_dni.text,
            self.ids.medic_name.text,
            self.ids.medic_last_name.text,
            self.ids.medic_email.text,
            self.ids.medic_password.text,
            self.ids.medic_phone_number.text,
        ]

        if self.confirm_register(): 
            db.new_medic(*self.medic_data)
        else:
            print("Las contraseñas no coinciden")
    
    def confirm_register(self):
        pwd_equal = self.ids.medic_password.text == self.ids.medic_password_confirmation.text
        return pwd_equal

Window.size = (360, 640)

class TaniWasaApp(MDApp): # Hereda los métodos de la clase App de kivy (como run())
    
    ser_com = SerialCom()
    current_user_data = None
    current_sensor_data = None
    current_medic_data = None

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
        self.root.get_screen("login_window").ids.tabs.add_widget(RegisterMedicTab(text = "[font=Candara]Soy médico[/font]"))

if __name__ == "__main__":
    TaniWasaApp().run() # Llama run sobre una instancia de MyApp