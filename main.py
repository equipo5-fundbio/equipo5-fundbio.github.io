from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.tab import MDTabsBase
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


class LoginWindow(Screen):
    pass

class MainWindow(Screen):
    pass

class TreatmentWindow(Screen):
    pass

class DataReadingWindow(Screen):
    pass

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