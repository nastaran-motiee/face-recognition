from multiprocessing.connection import Listener
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy_camera import KivyCamera
from kivy.uix.screenmanager import Screen


class ClientScreen(Screen):
    camera = ObjectProperty(None)



