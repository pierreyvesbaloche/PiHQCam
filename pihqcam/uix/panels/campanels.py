from kivy.logger import Logger
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import ConfigParserProperty
from kivy.uix.scrollview import ScrollView

from pihqcam.device.trackballhelper import TrackballHelper
from pihqcam.uix.image.imagehelper import ImageHelper
from pihqcam.uix.layout.cameraview import HandledPiCameraView

import sys

class HandledPiCamPanels(TabbedPanel):

    LIVE_TAB = 2
    BROWSER_TAB = 1
    INFO_TAB = 0

    duration = ConfigParserProperty('5', 'HQCam', 'timers_duration', 'app')

    def __init__(self, **kwargs):
        super(HandledPiCamPanels, self).__init__(**kwargs)
        # Define Trackball call
        self.trackball = TrackballHelper()
        self.trackball.setup()
        self.trackball.clear_trackball()
        self.trackball.start(self.on_read_trackball)
        self.myroot = None # Injected from KV TODO Change

    def on_read_trackball(self, trackball_value):
        tb_group = self.tab_list
        tb = next( (t for t in tb_group if t.state=='down'), None)
        if tb:
            position = tb_group.index(tb)
            new_pos = position
            max = len(tb_group) - 1

            if TrackballHelper.NOTIFY_LEFT == trackball_value:
                new_pos = position + 1
                if new_pos > max:
                    new_pos = max
            elif TrackballHelper.NOTIFY_RIGHT == trackball_value:
                new_pos = position - 1
                if new_pos < 0:
                    new_pos = 0

            if position != new_pos:
                tb_group[new_pos].state = "down"
                tb_group[position].state = "normal"
                tb_group[new_pos].dispatch('on_release')

                if new_pos==1: # Browser
                    filechooser = self.myroot.ids["filechooser"]
                    if len(filechooser.selection)<1:
                        Logger.info("Updating selection")
                        if len(filechooser._items) > 0:
                            filechooser._items[0].is_selected=True
                            filechooser.selection=[filechooser._items[0].path,]
                            filepreviewer = self.myroot.ids["filepreviewer"]
                            filepreviewer.source = ImageHelper().process_for_thumbnail(filechooser._items[0].path)
                            Logger.info("Updating viewer source to {}".format(filepreviewer.source))
                    Logger.info("Done with Browser")
                            
            elif TrackballHelper.NOTIFY_CLICK == trackball_value:
                if position==HandledPiCamPanels.LIVE_TAB:
                    try:
                        cameraview = self.myroot.ids["cameraview"]
                        if HandledPiCameraView.MODE_STILL == cameraview.mode:
                            Logger.info("Taking Picture")
                            self.myroot.ids["cameraview"].capture()
                        elif HandledPiCameraView.MODE_TIMER == cameraview.mode:
                            Logger.info("Taking Picture with Timer")
                            self.myroot.ids["cameraview"].capture()
                        elif HandledPiCameraView.MODE_VIDEO == cameraview.mode:
                            Logger.info("Taking Video")
                            self.myroot.ids["cameraview"].capture_video()
                        else:
                            Logger.error("Invalid Mode {}".format(cameraview.mode))
                    except AttributeError as ae:
                        Logger.error("===== AttributeError")
                        Logger.error(ae)
                    except:
                        Logger.error("HandledPiCamPanels: on_read_trackball: {}".format(sys.exc_info()[0]))
            else:
                if position==HandledPiCamPanels.BROWSER_TAB: # Browser
                    filechooser = self.myroot.ids["filechooser"]
                    if len(filechooser.selection)<1:
                        print(filechooser._items[0].path)
                        if len(filechooser._items) > 0:
                            filechooser._items[0].is_selected=True
                            filechooser.selection=[filechooser._items[0].path,]
                        return
                    cur=filechooser.selection[0]
                    sfiles=[entry.path for entry in filechooser._items]
                    fcount=len(sfiles)
                    if fcount<1:
                        return
                    if cur in sfiles:
                        idx=sfiles.index(cur)
                        orig = idx
                        if TrackballHelper.NOTIFY_UP == trackball_value:
                            offset = -1
                        elif TrackballHelper.NOTIFY_DOWN == trackball_value:
                            offset = 1
                        idx+=offset
                        if idx>=fcount:
                            idx-=fcount
                        new=sfiles[idx]
                        filechooser._items[orig].is_selected=False
                        filechooser._items[idx].is_selected=True
                        filechooser.selection=[new,]
                        # Access the kivy.uix.filechooser.FileChooserListLayout
                        for fileChooserListLayout in filechooser.children:   
                            # Access the kivy.uix.boxlayout.BoxLayout
                            for boxLayout in fileChooserListLayout.children: 
                                # Scroll to reach the ScrollView  
                                for child in boxLayout.children:   
                                    if isinstance(child, ScrollView): #kivy.uix.scrollview.ScrollView):
                                        child.scroll_to(filechooser._items[idx])