# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ConfigParserProperty
from os.path import sep
from picamera import PiCamera

import itertools
import io
import time
import threading
import sys
import os

class HandledPiCameraView(BoxLayout):
    MODE_STILL = 1
    MODE_TIMER = 2
    MODE_VIDEO = 3
    DEF_REZ = "640x480"

    SHOOT_MODE_VIEWER = 1
    SHOOT_MODE_FILE = 2
    SHOOT_MODE_VIDEO = 3
    SHOOT_MODE_VIDEO_DONE = 4
    SHOOT_MODE_PROCESSING = 0

    capture1 = io.BytesIO()
    capture2 = io.BytesIO()
    still_resolution = ConfigParserProperty("640x480", 'HQCam', 'picture_res', 'app')
    video_resolution = ConfigParserProperty("1080p30", 'HQCam', 'video_res', 'app')

    def __init__(self, **kwargs):
        super(HandledPiCameraView, self).__init__(**kwargs)
        self._shoot_mode = HandledPiCameraView.SHOOT_MODE_VIEWER
        self.mode = HandledPiCameraView.MODE_STILL
        self.camera = PiCamera(resolution=self.still_resolution)
        time.sleep(2)
        self.record_thread = threading.Thread(target=self.record)
        # TODO Include clean shutdown
        self.record_thread.daemon = True
        self.record_thread.start()
        self.is_recording = False

    def set_mode_camera_still(self, *args):
        Logger.info("Setting camera for STILL mode")
        self.mode = HandledPiCameraView.MODE_STILL

    def set_mode_camera_timer(self, *args):
        Logger.info("Setting camera for TIMER mode")
        self.mode = HandledPiCameraView.MODE_TIMER

    def set_mode_camera_video(self, *args):
        Logger.info("Setting camera for VIDEO mode")
        self.mode = HandledPiCameraView.MODE_VIDEO

    def process(self, data):
        if not self._shoot_mode == HandledPiCameraView.SHOOT_MODE_VIEWER:
            return True
        if self.cameraimage is not None:
            try:
                self.cameraimage.memory_data = data
            except:
                Logger.warn("Skipping Image")
                # Logger.error(sys.exc_info()[0])
        return False

    def record(self, *largs):
        analyse = None
        Logger.info("Processing from PiCamera STARTED")
        runnig = True
        try:
            while runnig:
                # Process Viewer
                if self._shoot_mode == HandledPiCameraView.SHOOT_MODE_VIEWER:
                    Logger.info("Rendering Viewer")
                    for stream in self.camera.record_sequence(itertools.cycle((io.BytesIO(), io.BytesIO())), format='mjpeg'):
                        if analyse is not None:
                            if self.process(analyse):
                                break
                            analyse.seek(0)
                            analyse.truncate()
                        self.camera.wait_recording(1 / 30.) #.25)
                        if self.cameraeffect:
                            effect = self.cameraeffect.get_effect()
                            if "black & white"==effect:
                                self.camera.image_effect = "none"
                                self.camera.color_effects = (128,128)
                            elif "sepia"==effect:
                                self.camera.image_effect = "none"
                                self.camera.color_effects = (100,150)
                            else:
                                self.camera.color_effects = None
                                self.camera.image_effect = effect
                        analyse = stream
                    Logger.info("DONE Rendering Viewer")          

                # Process Still
                if self.mode == HandledPiCameraView.MODE_STILL:
                    try:
                        self.cameraimage.memory_data = io.BytesIO(open("pihqcam/resources/camera.png", "rb").read())
                    except:
                        Logger.info("Skipping Still Camera Image")                    
                    self._shoot_mode = HandledPiCameraView.SHOOT_MODE_PROCESSING
                    self.camerashutter.trackball.click_blue_trackball()
                    Logger.info("Requesting Shooting Picture from {}".format(threading.current_thread().name))
                    # Clock.schedule_once(partial(self.shoot), -1)
                    self._thread_shoot = threading.Thread(target=self.shoot)
                    self._thread_shoot.start()
                    Logger.info("Requesting Shooting Done OK {}".format(threading.current_thread().name))
                    self._thread_shoot.join()
                    self.camerashutter.trackball.click_green_trackball()
                    time.sleep(1)
                    self.camerashutter.trackball.clear_trackball()
                    Logger.info("Done waiting capture {}".format(threading.current_thread().name))

                elif self.mode == HandledPiCameraView.MODE_TIMER:
                    try:
                        self.cameraimage.memory_data = io.BytesIO(open("pihqcam/resources/camera-retro.png", "rb").read())
                    except:
                        Logger.info("Skipping Camera Image")                    
                    self._shoot_mode = HandledPiCameraView.SHOOT_MODE_PROCESSING
                    Logger.info("Requesting Timed Shooting Picture from {}".format(threading.current_thread().name))
                    self.camerashutter.trackball.timer_still()
                    self.camerashutter.trackball.click_blue_trackball()
                    # Clock.schedule_once(partial(self.shoot), -1)
                    self._thread_shoot = threading.Thread(target=self.shoot)
                    self._thread_shoot.start()
                    Logger.info("Requesting Timed Shooting Done OK {}".format(threading.current_thread().name))
                    self._thread_shoot.join()
                    self.camerashutter.trackball.click_green_trackball()
                    time.sleep(1)
                    self.camerashutter.trackball.clear_trackball()
                    Logger.info("Done waiting timed capture {}".format(threading.current_thread().name))

                elif self.mode == HandledPiCameraView.MODE_VIDEO:

                    # Process Video End
                    if self._shoot_mode == HandledPiCameraView.SHOOT_MODE_VIDEO_DONE:
                        Logger.info("In Mode VIDEO_MODE {} with recording at ".format(self._shoot_mode, self.is_recording))       
                        if self.is_recording:
                            Logger.info("Stopping Video Shooting from {}".format(threading.current_thread().name))
                            self.camera.stop_recording()
                            Logger.info("Stopped Video Shooting")
                            self.camerashutter.trackball.deactivate_video()
                            self.camerashutter.trackball.click_green_trackball()
                            time.sleep(1)
                            self.camerashutter.trackball.clear_trackball()
                            self.is_recording = False

                            Logger.info("Resetting Video Mode {}".format(threading.current_thread().name))
                            self.camera.resolution=HandledPiCameraView.DEF_REZ
                            self.camera.image_effect = "none"
                            self._shoot_mode = HandledPiCameraView.SHOOT_MODE_VIEWER
                            self.myroot.ids["filechooser"]._update_files()
                            Logger.info("Shooting Done OK {}".format(threading.current_thread().name))
                        else:
                            Logger.error("Should not be in SHOOT_MODE_VIDEO_DONE while not recording")                    

                    # Process Video
                    elif self._shoot_mode == HandledPiCameraView.MODE_VIDEO:
    # ---------------------------
                        if not self.is_recording:
                            # self._shoot_mode = HandledPiCameraView.SHOOT_MODE_PROCESSING
                            Logger.info("Requesting Video Shooting from {}".format(threading.current_thread().name))
                            try:
                                self.cameraimage.memory_data = io.BytesIO(open("pihqcam/resources/video-camera.png", "rb").read())
                            except:
                                Logger.info("Skipping Video Camera Image")                    
                            self.is_recording = True
                            self.camerashutter.trackball.activate_video()
                            self._thread_video = threading.Thread(target=self.record_video)
                            self._thread_video.start()
                            Logger.info("Waiting video shooting thread")
                            self._thread_video.join()
                            Logger.info("Done waiting video shooting thread")
                            self._thread_video = None
                else:
                    time.sleep(0.5)

# ---------------------------                    
                # Process Wait
                while self._shoot_mode == HandledPiCameraView.SHOOT_MODE_PROCESSING:
                    time.sleep(1)
                    Logger.info("Waiting {}".format(threading.current_thread().name))
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            Logger.error("HandledPiCameraView: record: {} / {} / {}".format(exc_type, fname, exc_tb.tb_lineno))
        finally:
            Logger.info("Processing from PiCamera STOPPED")

    def record_video(self, *largs):
        try:
            timestr = time.strftime("%Y%m%d_%H%M%S")
            target = App.get_running_app().config.get('HQCam','picture_folder')
            if not target:
                Logger.warn("Unable to get path from config.")
                target = os.getcwd() + sep + FOLDER_PHOTOS
            else:
                Logger.info("Got path from config: {}".format(target))

            name = target+sep+"VID_{}.h264".format(timestr)

            config = self.video_resolution.split("p")
            if config[0].find('x')==-1:
                vid_res = config[0]+"p"
            else:
                vid_res = config[0]
            Logger.info("Resolution is {}".format(vid_res))
            self.camera.resolution=vid_res
            Logger.info("Framerate is {}".format(config[1]))
            self.camera.framerate=int(config[1])
            # self.camera.resolution=self.video_resolution
            if self.cameraeffect:
                effect = self.cameraeffect.get_effect()
                Logger.info("Effect is {}".format(effect))
                if "black & white"==effect:
                    self.camera.image_effect = "none"
                    self.camera.color_effects = (128,128)
                elif "sepia"==effect:
                    self.camera.image_effect = "none"
                    self.camera.color_effects = (100,150)
                else:
                    self.camera.color_effects = None
                    self.camera.image_effect = effect
            Logger.info("Recording to {} from {}".format(name, threading.current_thread().name))
            self.camera.start_recording(name)
        except:
            Logger.error("HandledPiCameraView: record: {}".format(sys.exc_info()[0]))
        finally:
            pass

    def shoot(self, *largs):
        try:
            timestr = time.strftime("%Y%m%d_%H%M%S")

            target = App.get_running_app().config.get('HQCam','picture_folder')
            if not target:
                Logger.warn("Unable to get path from config.")
                target = os.getcwd() + sep + FOLDER_PHOTOS
            else:
                Logger.info("Got path from config: {}".format(target))

            name = target+sep+"IMG_{}.jpg".format(timestr)
            Logger.info("MAX Resolution is {}".format(PiCamera.MAX_RESOLUTION))
            Logger.info("Resolution is {}".format(self.still_resolution))
            self.camera.resolution=self.still_resolution

            if self.cameraeffect:
                effect = self.cameraeffect.get_effect()
                if "black & white"==effect:
                    self.camera.image_effect = "none"
                    self.camera.color_effects = (128,128)
                elif "sepia"==effect:
                    self.camera.image_effect = "none"
                    self.camera.color_effects = (100,150)
                else:
                    self.camera.color_effects = None
                    self.camera.image_effect = effect
            Logger.info("Capturing to {} from {}".format(name, threading.current_thread().name))
            self.camera.capture(name)
        except:
            Logger.error("HandledPiCameraView: shoot: {}".format(sys.exc_info()[0]))
        finally:
            Logger.info("Finalizing Shooting Still {}".format(threading.current_thread().name))
            self.camera.resolution=HandledPiCameraView.DEF_REZ
            self.camera.image_effect = "none"
            self._shoot_mode = HandledPiCameraView.SHOOT_MODE_VIEWER
            self.myroot.ids["filechooser"]._update_files()
            Logger.info("Shooting Done OK {}".format(threading.current_thread().name))
            
    def capture(self, *largs):
        Logger.info("New Shoot Mode > FILE")
        # Change Action Mode
        self._shoot_mode = HandledPiCameraView.SHOOT_MODE_FILE

    def capture_video(self, *largs):
        # Change Action Mode
        if self.is_recording:
            Logger.info("New Shoot Mode > VIDEO_DONE")
            self._shoot_mode = HandledPiCameraView.SHOOT_MODE_VIDEO_DONE
        else:
            Logger.info("New Shoot Mode > VIDEO")
            self._shoot_mode = HandledPiCameraView.SHOOT_MODE_VIDEO