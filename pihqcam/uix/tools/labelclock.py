# -*- coding: utf-8 -*-
from kivy.clock import Clock
from kivy.uix.label import Label

import time

class LabelClock(Label):

    def __init__(self, **kwargs):
        super(LabelClock, self).__init__(**kwargs)
        self.handle = Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        self.text = time.strftime("%A, %d %b %Y %H:%M:%S", time.localtime())