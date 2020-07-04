# -*- coding: utf-8 -*-
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.screenmanager import Screen

class SplashScreen(Screen):

    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)

    def setup(self, manager, screen):
        self.screen_manager = manager
        self.next_screen = screen
        
    def change(self, dt):
        self.screen_manager.switch_to(self.next_screen)

    def on_enter(self, *args):
        Clock.schedule_once(self.change, 12)
        Logger.info("Displaying Splash Screen")