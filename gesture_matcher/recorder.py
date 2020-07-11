from threading import Thread

from gesture_matcher import similarity
from leap import Leap
from leap.Leap import Vector


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
        self.similarity = similarity.calculate_2(self.tracking_control.saved_data, self.match_control.saved_data)


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


class GestureFrame:

    def __init__(self, thumb=Vector(), index=Vector(), middle=Vector(), ring=Vector(), pinky=Vector(), palm=Vector(), palm_position=Vector()):
        self.thumb = thumb
        self.index = index
        self.middle = middle
        self.ring = ring
        self.pinky = pinky
        self.palm = palm
        self.palm_direction = palm_position


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

        fingers = frame.fingers
        gesture_frame = GestureFrame()
        if fingers:
            gesture_frame.thumb = fingers[0].tip_position
            gesture_frame.index = fingers[1].tip_position
            gesture_frame.middle = fingers[2].tip_position
            gesture_frame.ring = fingers[3].tip_position
            gesture_frame.pinky = fingers[4].tip_position

        right_hand = frame.hands.rightmost
        direction = right_hand.palm_normal
        position = right_hand.palm_position
        gesture_frame.palm = position
        gesture_frame.palm_direction = direction
        print position
        self.data.append(gesture_frame)
