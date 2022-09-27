from kivy.app import App
from kivy.lang import Builder
from smart_system import SmartSystem
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons



class SmartApp(MDApp):

    def __init__(self, **kwargs):
        super(SmartApp, self).__init__(**kwargs)
        self.smart_system = None
        self.face_recognition_camera = None
        Builder.load_file('view/smart.kv')

    def build(self):
        """
        Integrates open-cv webcam into a kivy user interface and returns it as a root object
        :return:root object
        """

        self.smart_system = SmartSystem()
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"
  
        return self.smart_system
    
  
    

    def on_stop(self):
        """
        Without this method, app will not exit even if the window is closed
        """

        self.smart_system.camera.stop()


if __name__ == '__main__':
    SmartApp().run()
