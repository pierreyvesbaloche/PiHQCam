# -*- coding: utf-8 -*-
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.uix.screenmanager import Screen

import subprocess

class ShutdownScreen(Screen):

    CMD_SHUTDOWN = "/usr/bin/sudo /sbin/shutdown -h now"

    def __init__(self, **kwargs):
        super(ShutdownScreen, self).__init__(**kwargs)
        
    def switchoff(self, dt):
        process = subprocess.Popen(ShutdownScreen.CMD_SHUTDOWN.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        Logger.info(output)

    def on_enter(self, *args):
        Clock.schedule_once(self.switchoff, 4)
        Logger.info("Quitting...")
