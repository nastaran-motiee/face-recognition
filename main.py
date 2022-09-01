from kivy.app import App
from kivy.lang import Builder
import cv2
from kivy_camera import KivyCamera
from model.mongo_db import Model


class SmartApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file('view/smart.kv')
        self._capture = None

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
