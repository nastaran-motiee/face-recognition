from kivy.app import App
from kivy.lang import Builder
from kivy_camera import KivyCamera
from kivy.config import Config
import pyautogui


class SmartApp(App):
    def __init__(self, **kwargs):
        super(SmartApp, self).__init__(**kwargs)
        self.face_recognition_camera = None
        width, height = pyautogui.size()  # Get the width and height of the screen
        Config.set('graphics', 'width', str(width // 4))  # Set the window width
        Config.set('graphics', 'height', str(height - height // 3))  # Set the window height
        Builder.load_file('view/smart.kv')

    def build(self):
        """
        Integrates open-cv webcam into a kivy user interface and returns it as a root object
        :return:root object
        """
        self.face_recognition_camera = KivyCamera()
        return self.face_recognition_camera

    def on_stop(self):
        """
        Without this method, app will not exit even if the window is closed
        """
        self.face_recognition_camera.stop()


if __name__ == '__main__':
    SmartApp().run()
