import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from threading import Lock, Thread
import cv2
from kivy_camera import KivyCamera


class SmartApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_file('view/smart.kv')
        self._capture = None

    def build(self):
        """
        :return:Integrated open-cv webcam into a kivy user interface
        """
        self.capture = cv2.VideoCapture(0)
        face_recognition_camera = KivyCamera(capture=self.capture, fps=33.)
        return face_recognition_camera

    @property
    def capture(self):
        return self._capture

    @capture.setter
    def capture(self, capture):
        self._capture = capture

    def on_stop(self):
        """
        Without this method, app will not exit even if the window is closed
        """
        self.capture.release()


if __name__ == '__main__':
    SmartApp().run()
