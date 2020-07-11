from threading import Thread

from gesture_matcher import similarity
from leap import Leap


class Recorder:

    def __init__(self):
        self.tracking_control = TrackingControl()
        self.match_control = TrackingControl()
        self.similarity = None

    def start_recording(self):
        self.tracking_control.start()

    def stop_recording(self):
        self.tracking_control.stop()

    def start_matching(self):
        self.match_control.start()

    def stop_matching(self):
        self.match_control.stop()
        self.similarity = similarity.calculate(self.tracking_control.saved_data, self.match_control.saved_data)


class TrackingControl:
    saved_data = []

    def __init__(self):
        self.keep_tracking = False
        self.listener = GestureListener()
        self.controller = Leap.Controller()

    def start(self):
        if self.keep_tracking is False:
            self.keep_tracking = True
            Thread(target=self.track).start()

    def stop(self):
        self.keep_tracking = False
        self.saved_data = self.listener.data

    def track(self):
        self.listener.data = []
        self.controller.add_listener(self.listener)
        print 'Tracking started'
        while self.keep_tracking:
            pass
        self.controller.remove_listener(self.listener)
        print 'Tracking stopped'


class GestureListener(Leap.Listener):

    def __init__(self):
        Leap.Listener.__init__(self)
        self.data = []

    def on_connect(self, controller):
        print "Connected"

    def on_exit(self, controller):
        print 'Exit'

    def on_frame(self, controller):
        frame = controller.frame()
        right_hand = frame.hands.rightmost
        position = right_hand.palm_position
        self.data.append(position)
        print position
