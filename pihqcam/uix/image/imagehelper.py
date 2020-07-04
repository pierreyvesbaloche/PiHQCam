# -*- coding: utf-8 -*-

from kivy.logger import Logger
import ntpath
import os
import PIL
import sys


class ImageHelper():
    """
    Helper class for image processing.
    """

    # Default location to store the thumbnail
    DEFAULT_THUMB_DIR = "/tmp"

    # Default prefix for the thumbnail's name
    DEFAULT_THUMB_NAME = "thumb_"

    # Default format for the thumbnails
    DEFAULT_THUMB_FORMAT = "JPEG"

    # Default image quality for the thumbnails
    DEFAULT_THUMB_QUALITY = 90

    # Default image resolution for the thumbnails
    DEFAULT_THUMB_RESOLUTION = (640, 480)

    def __init__(self, **kwargs):
        """
        Init method.
        @:return None
        """
        super(ImageHelper, self).__init__(**kwargs)

    def extract_name(self, path):
        """[summary]

        Args:
            path (string): The full path of a file.

        Returns:
            [string]: The end part of the path (usually the filename).
        """
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def get_image(self, path):
        """
        Retrieve a PIL.Image from the path

        Args:
            file_path ([type]): [description]

        Returns:
            [PIL.Image]: The PIL.Image if the path leads to a valid file, None otherwise.
        """
        pil_image = None
        if os.path.exists(path):
            try:
                if os.path.isdir(path):  
                    Logger.info("Ignoring directory {}".format(path))
                else:
                    pil_image = PIL.Image.open(path)
                    Logger.info("Accessing {}".format(path))
            except PIL.UnidentifiedImageError:
                raise
            except:
                Logger.error("ImageHelper: get_image: {}".format(sys.exc_info()[0]))
        return pil_image

    def process_for_thumbnail(self, path, temp_dir=DEFAULT_THUMB_DIR):
        filename = self.extract_name(path)
        thumb = "{}/{}{}".format(temp_dir,
                                      ImageHelper.DEFAULT_THUMB_NAME, filename)

        # No need to re-create the thumbnail if it exists already
        if not os.path.exists(thumb):
            try:
                pil_image = self.get_image(path)
                if pil_image:
                    Logger.info("Opening {}".format(path))
                    pil_image.thumbnail(ImageHelper.DEFAULT_THUMB_RESOLUTION)
                    Logger.info("Converting {}".format(filename))
                    converted = pil_image.convert('RGB')
                    Logger.info("Saving {}".format(thumb))
                    converted.save(thumb, format=ImageHelper.DEFAULT_THUMB_FORMAT,
                                optimize=True, quality=ImageHelper.DEFAULT_THUMB_QUALITY)
            except:
                Logger.error("ImageHelper: process_for_thumbnail: {}".format(sys.exc_info()[0]))
        return thumb
