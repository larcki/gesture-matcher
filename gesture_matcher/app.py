import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from gesture_matcher.recorder import Recorder

kivy.require('1.11.0')


class GestureMatcherApp(App):

    def build(self):
        recorder = Recorder()

        def record(instance):
            recorder.start_recording()

        def stop(instance):
            recorder.stop_recording()

        def match(instance):
            recorder.start_matching()

        def stop_match(instance):
            recorder.stop_matching()

        layout = BoxLayout(size_hint=(1, None), height=50)
        startButton = Button(text='Start', on_press=record)
        stopButton = Button(text='Stop', on_press=stop)
        layout.add_widget(startButton)
        layout.add_widget(stopButton)

        layout2 = BoxLayout(size_hint=(1, None), height=50)
        layout2.add_widget(Label(text='Record gesture'))

        layout3 = BoxLayout(size_hint=(1, None), height=50)
        layout3.add_widget(Label(text='Test match'))
        layout3.add_widget(Button(text='Start', on_press=match))
        layout3.add_widget(Button(text='Stop', on_press=stop_match))
        root = BoxLayout(orientation='vertical')
        root.add_widget(layout2)
        root.add_widget(layout)
        root.add_widget(BoxLayout(size_hint=(1, None), height=100))
        root.add_widget(layout3)

        return root


if __name__ == '__main__':
    GestureMatcherApp().run()
