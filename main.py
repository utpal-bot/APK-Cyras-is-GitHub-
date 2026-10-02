import json
import urllib.request
import urllib.parse
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock
from plyer import tts

# Screen styling
Window.clearcolor = (0, 0, 0, 1)

class CyrasApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        self.title_label = Label(
            text="CYRAS NATIVE CORE",
            font_size='22sp',
            color=(0, 0.95, 1, 1),
            size_hint=(1, 0.2)
        )
        self.layout.add_widget(self.title_label)

        self.status_label = Label(
            text="Press button to initialize Cyras",
            font_size='16sp',
            color=(0.8, 0.8, 0.8, 1),
            size_hint=(1, 0.4),
            text_size=(Window.width - 80, None),
            halign='center'
        )
        self.layout.add_widget(self.status_label)

        self.action_btn = Button(
            text="ACTIVATE CYRAS",
            font_size='18sp',
            size_hint=(1, 0.2),
            background_color=(0, 0.6, 1, 1)
        )
        self.action_btn.bind(on_press=self.on_activate)
        self.layout.add_widget(self.action_btn)

        return self.layout

    def on_activate(self, instance):
        self.status_label.text = "Welcome Boss! Cyras Native Online."
        try:
            tts.speak("Welcome Boss! Cyras is ready.")
        except Exception:
            pass

if __name__ == '__main__':
    CyrasApp().run()
