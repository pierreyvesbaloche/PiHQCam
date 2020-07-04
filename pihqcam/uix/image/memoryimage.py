# -*- coding: utf-8 -*-

from kivy.clock import Clock
from kivy.core.image import Image as CoreImage
from kivy.properties import ObjectProperty
from kivy.logger import Logger
from kivy.uix.image import Image
import threading

class MemoryImage(Image):
    """
    Class to handle images in memory.
    """
    # Image memory data
    memory_data = ObjectProperty(None)

    # Default refresh rate
    DEFEAULT_REFRESH_RATE = 1 / 30.

    # Default image format
    DEFAULT_TYPE = "jpeg"

    def __init__(self, **kwargs):
        """
        Init method.
        @:return None
        """
        super(MemoryImage, self).__init__(**kwargs)
        self._image_lock = threading.Lock()
        self._image_buffer = None
        self.clock_event = Clock.schedule_interval(self.update_image, MemoryImage.DEFEAULT_REFRESH_RATE)

    def on_memory_data(self, *args):
        """
        Triggered when the memory_data property is updated.
        @:return None        
        """
        self.memory_data.seek(0)                    # Position to the right location in memory
        im = CoreImage(self.memory_data, ext=MemoryImage.DEFAULT_TYPE, nocache=True)
        with self._image_lock:                      # Ensure to have the required access prior to updating
            self._image_buffer = im

    def update_image(self, *args):
        """
        Update of the image content from the memory buffer.
        """
        im = None
        with self._image_lock:                      # Ensure to have the required access prior to updating
            im = self._image_buffer                 # Safe the data
            self._image_buffer = None               # Clear the buffer
        if im:                                      # If there is a valid image     (is not None:     ) TODO 
            self.texture = im.texture               # Update the image's content
            self.texture_size = im.texture.size     # Update the image's size

    def deactivate_update(self):
        """
        Deactivate the refreshing process.
        """
        if self.clock_event:
            self.clock_event.cancel()
