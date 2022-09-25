from kivy.app import App
from kivy.lang import Builder
from smart_system import SmartSystem
from kivy.core.window import Window

class SmartApp(App):

    def __init__(self, **kwargs):
        super(SmartApp, self).__init__(**kwargs)
        self.face_recognition_camera = None
        Builder.load_file('view/smart.kv')

    def build(self):
        """
        Integrates open-cv webcam into a kivy user interface and returns it as a root object
        :return:root object
        """
       
        #self.face_recognition_camera = KivyCamera()
        smart_system = SmartSystem()

        Window.clearcolor = (1, 1, 1, 1)

        return smart_system

    def on_stop(self):
        """
        Without this method, app will not exit even if the window is closed
        """
    
        self.face_recognition_camera.stop()



if __name__ == '__main__':
    SmartApp().run()
