# -*- coding: utf-8 -*-
from kivy.uix.gridlayout import GridLayout
from pihqcam.device.camerahelper import CameraHelper

class PiCameraEffectGridLayout(GridLayout):
    def __init__(self, **kwargs):
        super(PiCameraEffectGridLayout, self).__init__(**kwargs)
        self.camera_helper = CameraHelper()

    def update_camera_effect(self, effect_name):
        self.camera_helper.update_camera_effect(effect_name)

    def get_effect(self):
        return self.camera_helper.get_effect()
        