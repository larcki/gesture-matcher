import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

from gesture_matcher.countdown import countdown
from gesture_matcher.recorder import Recorder

kivy.require('1.11.0')


class MainGrid(Widget):
    record_text = ObjectProperty(None)
    match_text = ObjectProperty(None)
    recorder = Recorder()

    def on_record_button_click(self):
        self.record_text.text = 'Get ready... 3'
        Clock.schedule_interval(self.get_ready_countdown, 1)

    def on_match_button_click(self):
        self.match_text.text = 'Get ready... 3'
        Clock.schedule_interval(self.match_get_ready_countdown, 1)

    def get_ready_countdown(self, instance):
        return countdown(
            self.record_text,
            self.schedule_recording_countdown,
            lambda: 'Recording... 5',
            'Get ready... '
        )

    def match_get_ready_countdown(self, instance):
        return countdown(
            self.match_text,
            self.schedule_matching_countdown,
            lambda: 'Recording... 5',
            'Get ready... '
        )

    def schedule_recording_countdown(self):
        self.recorder.start_recording()
        Clock.schedule_interval(self.recording_countdown, 1)

    def schedule_matching_countdown(self):
        self.recorder.start_matching()
        Clock.schedule_interval(self.matching_countdown, 1)

    def recording_countdown(self, instance):
        return countdown(
            self.record_text,
            self.recorder.stop_recording,
            lambda: 'Saved',
            'Recording... '
        )

    def matching_countdown(self, instance):
        return countdown(
            self.match_text,
            self.recorder.stop_matching,
            lambda: str(self.recorder.similarity),
            'Recording... '
        )


class GestureMatcherApp(App):

    def build(self):
        return MainGrid()


if __name__ == '__main__':
    GestureMatcherApp().run()
