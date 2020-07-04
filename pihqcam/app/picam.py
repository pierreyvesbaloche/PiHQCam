# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.screenmanager import Screen
import os

class HandledPiCamApp(App):

    SECTION_NAME = 'HQCam'
    SETTINGS = 'pihqcam/settings.json'

    def setup(self, manager, quit_screen, shutdown_screen):
        self.screen_manager = manager
        self.quit_screen = quit_screen
        self.shutdown_screen = shutdown_screen
        
    def build(self):
        self.screen_manager.current = "Splash"
        return self.screen_manager

    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults(HandledPiCamApp.SECTION_NAME, {'picture_folder': './DCIM', 'thumb_folder': '/tmp/', 'picture_res': '640x480', 'timers_duration':10})

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # We use the string defined above for our JSON, but it could also be
        # loaded from a file as follows:
        settings.add_json_panel(HandledPiCamApp.SECTION_NAME, self.config, HandledPiCamApp.SETTINGS)

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info("App.on_config_change: {0}, {1}, {2}, {3}".format(
            config, section, key, value))

        if section == HandledPiCamApp.SECTION_NAME:
            if key == "picture_folder" or key == "thumb_folder":
                if os.path.isdir(value):
                  Logger.info("'{}' exists".format(value))
                else:
                    try:
                        os.makedirs(value)
                        Logger.info("'{}' created successfully!".format(value))
                    except OSError as ose:
                        Logger.error("Unable to create '{}' - {}".format(value, ose))
                        print ("Creation of the directory %s failed" % path)
            elif key=="timers_duration":
                Logger.info("New Timer is '{}'".format(value))
            elif key=="picture_res":
                Logger.info("New still resolution is '{}'".format(value))
            elif key=="video_res":
                Logger.info("New video resolution is '{}'".format(value))

    def close_settings(self, settings=None):
        super(HandledPiCamApp, self).close_settings(settings)

    def do_quit(self, *args):
        self.screen_manager.switch_to(self.quit_screen)

    def do_switchoff(self, *args):
        self.screen_manager.switch_to(self.shutdown_screen)
        