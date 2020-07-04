# -*- coding: utf-8 -*-
import kivy
kivy.require('1.11.1') 

from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, FadeTransition

# import os
# from os.path import sep, join, dirname
# import sys

# from kivy.app import App
# from kivy.clock import Clock
# from kivy.config import Config, ConfigParser
# from kivy.lang import Builder
# from kivy.logger import Logger
# from kivy.uix.togglebutton import ToggleButton
# from kivy.uix.behaviors.focus import FocusBehavior
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
# from kivy.properties import ObjectProperty, ConfigParserProperty
# import io
# from kivy.uix.image import Image
# from kivy.core.image import Image as CoreImage


# from functools import partial

# import os

# Hide the cursor
Config.set("graphics", "show_cursor", 0)
# Allow virtual Keyboard for Preferences
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
# Change the transition effect between screens
screen_manager = ScreenManager(transition=FadeTransition())

# FOLDER_PHOTOS = "DCIM"

# # --------- Refacto

# import pihqcam.device.CameraHelper
# import pihqcam.uix.image.MemoryImage

import pihqcam.uix.screen.quit as quit_screen
import pihqcam.uix.screen.shutdown as shutdown_screen
import pihqcam.uix.screen.main as main_screen
import pihqcam.uix.screen.splash as splash_screen
import pihqcam.app.picam as app_cam

# # --------- Refacto - END

if __name__ == '__main__':
    # register('default_font', 'fonts/iconfont_sample.ttf',
    #          join(dirname(__file__), 'fonts/iconfont_sample.fontd'))

    Builder.load_file('pihqcam/kv/main.kv')
    Builder.load_file('pihqcam/kv/quit.kv')
    Builder.load_file('pihqcam/kv/shutdown.kv')
    Builder.load_file('pihqcam/kv/splash.kv')
    
    quit_screen = quit_screen.QuitScreen(name="Quit")
    shutdown_screen = shutdown_screen.ShutdownScreen(name="Shutdown")
    main_screen = main_screen.MainScreen(name="Main")
    splash_screen = splash_screen.SplashScreen(name="Splash")
    splash_screen.setup(screen_manager, main_screen)

    screen_manager.add_widget(splash_screen) 
    app = app_cam.HandledPiCamApp()
    app.setup(screen_manager, quit_screen, shutdown_screen)
    app.run()
