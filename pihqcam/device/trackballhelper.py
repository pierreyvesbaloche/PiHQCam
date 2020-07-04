# -*- coding: utf-8 -*-
from functools import partial
from kivy.clock import Clock
from kivy.logger import Logger
from trackball import TrackBall

import threading
import time

class TrackballHelper():
    """
    Helper class for Pimoroni's Trackball processing.
    """
    DEFAULT_I2C_BUS_ID = 3
    DEFAULT_INTERRUPT_ID = 4
    DEFAULT_INTERVAL = 0.5
    DEFAULT_THRESHOLD = 15
    DEFAULT_FLASH_DURATION = 5

    NOTIFY_LEFT = 1
    NOTIFY_RIGHT = 2
    NOTIFY_UP = 3
    NOTIFY_DOWN = 4
    NOTIFY_CLICK = 5

    ERR_MSG_NO_SETUP = "No trackball setup"
    ERR_MSG_ALREADY_STARTED = "Already started"
    ERR_MSG_NOT_STARTED = "Not started"
    ERR_MSG_ALREADY_RECORDING= "Already Recording"
    ERR_MSG_NOT_RECORDING= "Not Recording"

    def __init__(self, **kwargs):
        super(TrackballHelper, self).__init__(**kwargs)
        self.trackball = None
        self.trackball_event = None
        self.duration = TrackballHelper.DEFAULT_FLASH_DURATION
        self._video_lock = threading.Lock()

    def setup(self, bus_id=DEFAULT_I2C_BUS_ID, interrupt=DEFAULT_INTERRUPT_ID, flash_duration=DEFAULT_FLASH_DURATION):
        self.trackball = TrackBall(i2c_bus=bus_id, interrupt_pin=interrupt)
        self.duration = flash_duration
        self.recording_video = False

    def start(self, callback):
        if self.trackball_event:
            Logger.error(TrackballHelper.ERR_MSG_ALREADY_STARTED)
            return
        self.trackball_event = Clock.schedule_interval(partial(self.on_read_trackball, callback), TrackballHelper.DEFAULT_INTERVAL)

    def stop(self):
        if not self.trackball_event:
            Logger.error(TrackballHelper.ERR_MSG_NOT_STARTED)
            return
        self.trackball_event.cancel()
        self.trackball_event = None

    def on_read_trackball(self, callback, delta_time):
        up, down, left, right, switch, state = self.trackball.read()
        if left > TrackballHelper.DEFAULT_THRESHOLD:
            callback(TrackballHelper.NOTIFY_LEFT)
        elif right > TrackballHelper.DEFAULT_THRESHOLD:
            callback(TrackballHelper.NOTIFY_RIGHT)
        if up > TrackballHelper.DEFAULT_THRESHOLD:
            callback(TrackballHelper.NOTIFY_UP)
        elif down > TrackballHelper.DEFAULT_THRESHOLD:
            callback(TrackballHelper.NOTIFY_DOWN)
        if state:
            callback(TrackballHelper.NOTIFY_CLICK)

    def clear_trackball(self):
        if self.trackball:
            self.trackball.set_rgbw(0, 0, 0, 0)
        else:
            Logger.error(TrackballHelper.ERR_MSG_NO_SETUP)

    def click_red_trackball(self):
        if self.trackball:
            self.trackball.set_rgbw(255, 0, 0, 0)
        else:
            Logger.error(TrackballHelper.ERR_MSG_NO_SETUP)

    def click_green_trackball(self):
        if self.trackball:
            self.trackball.set_rgbw(0, 255, 0, 0)
        else:
            Logger.error(TrackballHelper.ERR_MSG_NO_SETUP)

    def click_blue_trackball(self):
        if self.trackball:
            self.trackball.set_rgbw(0, 0, 255, 0)
        else:
            Logger.error(TrackballHelper.ERR_MSG_NO_SETUP)

    def timer_still(self):
        if self.trackball:
            for i in range(int(self.duration)):
                self.click_red_trackball()
                time.sleep(0.5)
                self.clear_trackball()
                time.sleep(0.5)
        else:
            Logger.error(TrackballHelper.ERR_MSG_NO_SETUP)

    def activate_video(self):
        if self.trackball:
            if self.recording_video:
                Logger.warn(TrackballHelper.ERR_MSG_ALREADY_RECORDING)
            else:
                with self._video_lock:
                    self.recording_video = True
                self.video_thread = threading.Thread(target=self.flash_video_recording)
                self.video_thread.start()
        else:
            Logger.error(TrackballHelper.ERR_MSG_NO_SETUP)

    def deactivate_video(self):
        if self.trackball:
            if not self.recording_video:
                Logger.warn(TrackballHelper.ERR_MSG_NOT_RECORDING)
            else:
                with self._video_lock:                
                    self.recording_video = False
                self.video_thread.join()
                self.video_thread = None
        else:
            Logger.error(TrackballHelper.ERR_MSG_NO_SETUP)

    def flash_video_recording(self):
        if self.trackball:
            while self.recording_video:
                self.click_red_trackball()
                time.sleep(0.5)
                self.clear_trackball()
                time.sleep(0.5)
        else:
            Logger.error(TrackballHelper.ERR_MSG_NO_SETUP)

