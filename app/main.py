from kivy.app import App
from kivy.lang import Builder

from app.kivy_camera import KivyCamera
from kivy.config import Config
import pyautogui


class SmartApp(App):

    def __init__(self, **kwargs):
        super(SmartApp, self).__init__(**kwargs)
        self.face_recognition_camera = None
        width, height = pyautogui.size()  # Get the width and height of the screen
        self._window_width = width // 4
        self._window_height = height - height // 3
        Config.set('graphics', 'width', str(self.window_width))  # Set the window width
        Config.set('graphics', 'height', str(self.window_height))  # Set the window height
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

    @property
    def window_width(self) -> int:
        return self._window_width

    @property
    def window_height(self) -> int:
        return self._window_height


if __name__ == '__main__':
    SmartApp().run()