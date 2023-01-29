from kivy.app import App
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager, Screen
from client_screen import ClientScreen
from admin_screen import AdminScreen

Builder.load_file('view/smart.kv')
Builder.load_file('view/kivy_camera.kv')
Builder.load_file('view/key_panel.kv')


class SmartApp(MDApp):
    def __init__(self, **kwargs):
        super(SmartApp, self).__init__(**kwargs)
        self.client_screen = None
        self.admin_screen = None

    def build(self):
        """
        Integrates open-cv webcam into a kivy user interface and returns it as a root object
        :return:root object
        """
        self.theme_cls.theme_style = "Light"
        # Create the screen manager
        sm = ScreenManager()
        self.client_screen = ClientScreen(name='client_screen')
        self.admin_screen = AdminScreen(name='admin_screen')
        sm.add_widget(self.client_screen)
        sm.add_widget(self.admin_screen)

        return sm

    def on_stop(self):
        """
        Without this method, app will not exit even if the window is closed
        """
        self.client_screen.camera.stop()


if __name__ == '__main__':
    SmartApp().run()
