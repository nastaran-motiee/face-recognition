from multiprocessing.connection import Listener
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from real_time_face_recognition import KivyCamera
from key_panel import KeyPanel
from kivy.uix.screenmanager import Screen


class ClientScreen(Screen):
    camera = ObjectProperty(None)

    def verify_button_clicked(self):
        self.camera.verify_button_action()

