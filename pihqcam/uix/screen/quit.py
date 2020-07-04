# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.screenmanager import Screen

class QuitScreen(Screen):

    def __init__(self, **kwargs):
        super(QuitScreen, self).__init__(**kwargs)
        
    def quit(self, dt):
        App.get_running_app().stop()

    def on_enter(self, *args):
        Clock.schedule_once(self.quit, 4)
        Logger.info("Quitting...")