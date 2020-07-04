# -*- coding: utf-8 -*-
from kivy.logger import Logger

class CameraHelper():

    EFFECT_STANDARD = "None"
    EFFECT_SEPIA = "Sepia"
    EFFECT_BLACKNWHITE = "Black & White"

    def __init__(self, **kwargs):
        super(CameraHelper, self).__init__(**kwargs)
        self.update_camera_effect(CameraHelper.EFFECT_STANDARD)

    def update_camera_effect(self, effect_name):
        Logger.info(effect_name)
        self.effect = effect_name.lower()

    def get_effect(self):
        return self.effect