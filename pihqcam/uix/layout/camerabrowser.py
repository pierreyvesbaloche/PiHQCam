# -*- coding: utf-8 -*-
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ConfigParserProperty
from pihqcam.uix.image.imagehelper import ImageHelper
import os
import sys
import PIL
import time

class PiCameraFileBrowser(BoxLayout):

    customrootpath = ConfigParserProperty('./DCIM', 'HQCam', 'picture_folder', 'app')

    def __init__(self, **kwargs):
        super(PiCameraFileBrowser, self).__init__(**kwargs)
        self.imageHelper = ImageHelper()

    def selected(self,filename):
        try:
            image_file = self.imageHelper.get_image(filename[0])
            if image_file:
                
                # If a video was shown before
                if hasattr(self.videopreviewer, 'saved_attrs'):
                    self.videopreviewer.state = "stop"
                    self.videopreviewer.height, self.videopreviewer.size_hint_y, self.videopreviewer.opacity, self.videopreviewer.disabled = 0, None, 0, True
                    self.filepreviewer.height, self.filepreviewer.size_hint_y, self.filepreviewer.opacity, self.filepreviewer.disabled = self.filepreviewer.saved_attrs

                self.filepreviewer.source = self.imageHelper.process_for_thumbnail(filename[0])        
                self.filename.text = self.imageHelper.extract_name(filename[0])
                exifData = image_file._getexif()
                if exifData:
                    self.filedate.text = image_file._getexif()[36867] # Date Picture was taken
                else:
                    self.filedate.text = time.ctime(os.path.getmtime(filename[0]))
                self.filerez.text = "{} x {}".format(image_file.size[0], image_file.size[1])

        except PIL.UnidentifiedImageError:
            try:
                Logger.warn("PiCameraFileBrowser: selected: Unsupported File support for file {} - Trying Video".format(filename[0]))
                # Hide Image File Previewer
                if not hasattr(self.filepreviewer, 'saved_attrs'):
                    self.filepreviewer.saved_attrs = self.filepreviewer.height, self.filepreviewer.size_hint_y, self.filepreviewer.opacity, self.filepreviewer.disabled
                self.filepreviewer.height, self.filepreviewer.size_hint_y, self.filepreviewer.opacity, self.filepreviewer.disabled = 0, None, 0, True
                self.filepreviewer.source = ""
                # Show Video File Previewer
                self.videopreviewer.height, self.videopreviewer.size_hint_y, self.videopreviewer.opacity, self.videopreviewer.disabled = self.filepreviewer.saved_attrs
                if not hasattr(self.videopreviewer, 'saved_attrs'):
                    self.videopreviewer.saved_attrs = self.filepreviewer.saved_attrs
                self.videopreviewer.source = filename[0]
                self.videopreviewer.state = "play"

                self.filename.text = self.imageHelper.extract_name(filename[0])
                self.filerez.text = ""
                self.filedate.text = time.ctime(os.path.getmtime(filename[0]))
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                Logger.error("PiCameraFileBrowser: selected: {} / {} / {}".format(exc_type, fname, exc_tb.tb_lineno))


    def do_delete_image(self, *args):
        if len(self.filechooser.selection)==1:
            path = self.filechooser.selection[0]
            try:
                if os.path.exists(path):
                    os.remove(path)
                self.filechooser._update_files()
                if len(self.filechooser._items) > 0:
                    self.filechooser._items[0].is_selected=True
                    self.filechooser.selection=[self.filechooser._items[0].path,]
            except:
                Logger.error("PiCameraFileBrowser: do_delete_image: {}".format(sys.exc_info()[0]))

