import math
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.clock import Clock
from plyer import tts

# Deep Sleek Dark Background
Window.clearcolor = (0.01, 0.02, 0.03, 1)

class GradientOrb(Widget):
    def __init__(self, **kwargs):
        super(GradientOrb, self).__init__(**kwargs)
        self.state = "idle"  # idle, listening, speaking
        self.pulse = 1.0
        self.glow_shift = 0.0
        
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.start_idle_pulse()

    def start_idle_pulse(self):
        Animation.stop_all(self)
        anim = (Animation(pulse=1.06, duration=2.2, t='in_out_sine') +
                Animation(pulse=0.96, duration=2.2, t='in_out_sine'))
        anim.repeat = True
        anim.bind(on_progress=lambda *args: self.update_canvas())
        anim.start(self)

    def set_state(self, state):
        self.state = state
        Animation.stop_all(self)
        
        if state == "listening":
            # Tez energetic listening pulse
            anim = (Animation(pulse=1.14, duration=0.8, t='in_out_quad') +
                    Animation(pulse=0.92, duration=0.8, t='in_out_quad'))
            anim.repeat = True
            anim.bind(on_progress=lambda *args: self.update_canvas())
            anim.start(self)
        elif state == "speaking":
            # Smooth voice vibration rhythm
            anim = (Animation(pulse=1.18, duration=0.5, t='in_out_sine') +
                    Animation(pulse=0.95, duration=0.5, t='in_out_sine'))
            anim.repeat = True
            anim.bind(on_progress=lambda *args: self.update_canvas())
            anim.start(self)
        else:
            self.start_idle_pulse()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            cx, cy = self.center_x, self.center_y
            base_r = min(self.width, self.height) * 0.42 * self.pulse

            # 1. Soft Ambient Halo (Faint background glow)
            Color(0.0, 0.4, 0.6, 0.12)
            Ellipse(pos=(cx - base_r * 1.5, cy - base_r * 1.5), size=(base_r * 3.0, base_r * 3.0))

            Color(0.0, 0.5, 0.7, 0.18)
            Ellipse(pos=(cx - base_r * 1.25, cy - base_r * 1.25), size=(base_r * 2.5, base_r * 2.5))

            # 2. Smooth Gradient Layers (Video jaisa blend)
            layers = 45
            for i in range(layers):
                fraction = 1.0 - (i / float(layers))
                r_size = base_r * fraction

                if self.state == "listening":
                    # Listening mode: Bright Neon Aqua/Green blend
                    r = 0.05 + 0.90 * (1.0 - fraction)
                    g = 0.90 + 0.10 * (1.0 - fraction)
                    b = 0.65 + 0.35 * (1.0 - fraction)
                    a = 0.22 + 0.78 * fraction
                elif self.state == "speaking":
                    # Speaking mode: Electric Sky Blue & Violet tone
                    r = 0.15 + 0.85 * (1.0 - fraction)
                    g = 0.45 + 0.55 * (1.0 - fraction)
                    b = 1.00
                    a = 0.25 + 0.75 * fraction
                else:
                    # Idle Mode (Jaisa aapke video me tha): Turquoise & Royal Cyan blend
                    r = 0.05 + 0.92 * (1.0 - fraction)
                    g = 0.70 + 0.28 * (1.0 - fraction)
                    b = 0.95 + 0.05 * (1.0 - fraction)
                    a = 0.22 + 0.78 * fraction

                Color(min(r, 1.0), min(g, 1.0), min(b, 1.0), min(a, 1.0))
                Ellipse(pos=(cx - r_size, cy - r_size), size=(r_size * 2, r_size * 2))

            # 3. Brilliant White Core Hotspot
            Color(1, 1, 1, 0.88)
            hotspot = base_r * 0.24
            Ellipse(pos=(cx - hotspot, cy - hotspot), size=(hotspot * 2, hotspot * 2))


class CyrasApp(App):
    def build(self):
        self.root = FloatLayout()
        self.is_active = False

        # Futuristic Centered Glowing Orb
        self.orb = GradientOrb(
            size_hint=(0.85, 0.55),
            pos_hint={'center_x': 0.5, 'center_y': 0.58}
        )
        self.root.add_widget(self.orb)

        # Status text (Same font & positioning as video)
        self.status_label = Label(
            text="Tap orb to talk, Boss...",
            font_size='17sp',
            color=(0.85, 0.85, 0.85, 0.9),
            size_hint=(1, None),
            height=45,
            pos_hint={'center_x': 0.5, 'y': 0.25}
        )
        self.root.add_widget(self.status_label)

        # Bottom Connection indicator
        self.conn_label = Label(
            text="VOICE CONNECTED",
            font_size='12sp',
            color=(0.35, 0.45, 0.5, 0.9),
            bold=True,
            size_hint=(1, None),
            height=30,
            pos_hint={'center_x': 0.5, 'y': 0.20}
        )
        self.root.add_widget(self.conn_label)

        return self.root

    def on_touch_down(self, touch):
        if self.orb.collide_point(*touch.pos):
            if not self.is_active:
                self.start_cyras_cycle()
            return True
        return super(CyrasApp, self).on_touch_down(touch)

    def start_cyras_cycle(self):
        self.is_active = True
        self.speak_reply("Welcome Boss! Cyras is ready, batayiye aaj kya plan hai?")

    def speak_reply(self, message):
        self.status_label.text = "Cyras bol raha hai..."
        self.conn_label.text = "SPEAKING..."
        self.orb.set_state("speaking")

        try:
            tts.speak(message)
        except Exception:
            pass

        # Reply length ke hisaab se speaking duration calculate
        words = len(message.split())
        est_duration = max(3.0, words * 0.42)

        # Aawaz poori hote hi AUTOMATICALLY mic open hoga bina dobara touch kiye!
        Clock.schedule_once(self.enter_listening_loop, est_duration)

    def enter_listening_loop(self, dt):
        self.status_label.text = "Sun raha hoon Boss, boliye..."
        self.conn_label.text = "LISTENING..."
        self.orb.set_state("listening")
        
        # Listening window simulation (is stage par hum speech-to-text hook karenge)
        # Jab aap bolna band karenge, ye wapas auto reply loop me jayega
        Clock.schedule_once(self.process_boss_input, 5.0)

    def process_boss_input(self, dt):
        # Demo continuous loop test
        if self.is_active:
            self.status_label.text = "Soch raha hoon..."
            self.conn_label.text = "PROCESSING..."
            self.orb.set_state("idle")
            
            # Continuous response back
            Clock.schedule_once(
                lambda d: self.speak_reply("Bilkul samajh gaya Boss. Agla instruction boliye, main sun raha hoon!"),
                1.5
            )

if __name__ == '__main__':
    CyrasApp().run()
