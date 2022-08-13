from kivy.app import App
from threading import Lock, Thread
import cv2
from kivy_camera import KivyCamera


class SmartCamApp(App):
    """
    The main application
    """
    _instance = None
    _lock: Lock = Lock()

    def __new__(cls, *args, **kwargs):
        """
        Thread Safe Singleton
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(SmartCamApp, cls).__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._capture = None

    def build(self):
        """
        :return:Integrated open-cv webcam into a kivy user interface
        """
        self.capture = cv2.VideoCapture(0)
        face_recognition_camera = KivyCamera(capture=self.capture, fps=30)
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
    SmartCamApp().run()
