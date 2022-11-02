from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy_camera import KivyCamera


class SmartSystem(Widget):
    camera = ObjectProperty(None)

    def verify_button_clicked(self):
        self.camera.verify_button_action()
