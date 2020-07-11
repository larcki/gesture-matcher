import kivy

kivy.require('1.11.0')
import numpy as np

from threading import Thread
from fastdtw import fastdtw
from scipy.spatial.distance import cosine
from leap import Leap
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App


class SampleListener(Leap.Listener):

    def __init__(self):
        Leap.Listener.__init__(self)
        self.data = []
        print '__init__ed'

    def on_device_failure(self, arg0):
        print 'asddsadsa'

    def on_connect(self, controller):
        print "Connected"

    def on_exit(self, controller):
        print 'on_exit'
        file = open('data.txt', 'w')
        for vector in self.data:
            file.write(str(vector.to_tuple()) + '\n')
        file.close()
        print "Saved"

    def on_frame(self, controller):
        print 'on_frame'
        frame = controller.frame()
        right_hand = frame.hands.rightmost
        position = right_hand.palm_position
        self.data.append(position)
        print position


class TrackingControl:
    saved_data = []

    def __init__(self):
        self.keep_tracking = False
        self.listener = SampleListener()
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


def calculate_similarity(saved_data, data_to_match):
    x1 = np.array([(1, 1, 4), (3, 3, 4), (0, 0, 0)])
    x2 = np.array([(1, 1, 4), (3, 3, 4), (0, 0, 0)])

    r1 = []
    for vector in saved_data:
        tuple = vector.to_tuple()
        r1.append((tuple[0] + 1, tuple[1] + 1, tuple[2] + 1))

    r2 = []
    for vector in data_to_match:
        tuple = vector.to_tuple()
        r2.append((tuple[0] + 1, tuple[1] + 1, tuple[2] + 1))

    distance, path = fastdtw(np.array(r1), np.array(r2), dist=cosine)
    print(distance)

    print 'Comparing similarity....'
    return 0.3


class TrackingControlWithMatching(TrackingControl):

    def __init__(self):
        TrackingControl.__init__(self)
        self.similarity = None

    def stop_and_match(self, data_to_match):
        TrackingControl.stop(self)
        self.similarity = calculate_similarity(self.saved_data, data_to_match)


class GesturePassApp(App):

    def build(self):
        recordGesture = TrackingControl()

        def stop_tracking(instance):
            recordGesture.stop()

        def start_tracking(instance):
            recordGesture.start()

        start = Button(text='Start', on_press=start_tracking)
        stop = Button(text='Stop', on_press=stop_tracking)
        layout = BoxLayout(size_hint=(1, None), height=50)
        layout.add_widget(start)
        layout.add_widget(stop)

        layout2 = BoxLayout(size_hint=(1, None), height=50)
        layout2.add_widget(Label(text='Record gesture'))

        matchGesture = TrackingControlWithMatching()

        def stop_tracking2(instance):
            matchGesture.stop_and_match(recordGesture.saved_data)

        def start_tracking2(instance):
            matchGesture.start()

        layout3 = BoxLayout(size_hint=(1, None), height=50)
        layout3.add_widget(Label(text='Test match'))
        layout3.add_widget(Button(text='Start', on_press=start_tracking2))
        layout3.add_widget(Button(text='Stop', on_press=stop_tracking2))
        root = BoxLayout(orientation='vertical')
        root.add_widget(layout2)
        root.add_widget(layout)
        root.add_widget(BoxLayout(size_hint=(1, None), height=100))
        root.add_widget(layout3)

        return root


if __name__ == '__main__':
    GesturePassApp().run()
