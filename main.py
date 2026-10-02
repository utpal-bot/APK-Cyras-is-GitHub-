import math
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.clock import Clock
from plyer import tts

# Pure Deep Black Background
Window.clearcolor = (0.02, 0.02, 0.04, 1)

class GlowingOrb(Widget):
    def __init__(self, **kwargs):
        super(GlowingOrb, self).__init__(**kwargs)
        self.state = "idle" # idle, listening, speaking
        self.pulse_scale = 1.0
        self.ring_opacity = 0.3
        
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.start_idle_animation()

    def start_idle_animation(self):
        Animation.stop_all(self)
        anim = (Animation(pulse_scale=1.12, ring_opacity=0.6, duration=1.8, t='in_out_sine') +
                Animation(pulse_scale=0.95, ring_opacity=0.2, duration=1.8, t='in_out_sine'))
        anim.repeat = True
        anim.bind(on_progress=lambda *args: self.update_canvas())
        anim.start(self)

    def set_state(self, new_state):
        self.state = new_state
        Animation.stop_all(self)
        
        if new_state == "listening":
            # Tez aur energetic pulse
            anim = (Animation(pulse_scale=1.2, ring_opacity=0.8, duration=0.8, t='in_out_quad') +
                    Animation(pulse_scale=0.9, ring_opacity=0.3, duration=0.8, t='in_out_quad'))
            anim.repeat = True
            anim.bind(on_progress=lambda *args: self.update_canvas())
            anim.start(self)
        elif new_state == "speaking":
            # Rapid wave-like pulse
            anim = (Animation(pulse_scale=1.25, ring_opacity=0.9, duration=0.5, t='in_out_sine') +
                    Animation(pulse_scale=0.95, ring_opacity=0.4, duration=0.5, t='in_out_sine'))
            anim.repeat = True
            anim.bind(on_progress=lambda *args: self.update_canvas())
            anim.start(self)
        else:
            self.start_idle_animation()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            center_x, center_y = self.center_x, self.center_y
            base_radius = min(self.width, self.height) * 0.32 * self.pulse_scale

            # State ke mutabiq color choose karein
            if self.state == "listening":
                core_color = (0.0, 1.0, 0.6)      # Neon Cyber Green
                outer_color = (0.0, 0.9, 0.7)
            elif self.state == "speaking":
                core_color = (1.0, 0.2, 0.4)      # Neon Red / Crimson
                outer_color = (1.0, 0.4, 0.6)
            else:
                core_color = (0.0, 0.75, 1.0)     # Arc Reactor Cyan Blue
                outer_color = (0.1, 0.5, 0.9)

            # Outer Glow Ring 2
            Color(outer_color[0], outer_color[1], outer_color[2], self.ring_opacity * 0.4)
            Line(circle=(center_x, center_y, base_radius * 1.55), width=2.0)

            # Outer Glow Ring 1
            Color(outer_color[0], outer_color[1], outer_color[2], self.ring_opacity)
            Line(circle=(center_x, center_y, base_radius * 1.25), width=3.0)

            # Outer Halo
            Color(core_color[0], core_color[1], core_color[2], 0.25)
            Ellipse(pos=(center_x - base_radius * 1.15, center_y - base_radius * 1.15),
                    size=(base_radius * 2.3, base_radius * 2.3))

            # Main Glowing Core
            Color(core_color[0], core_color[1], core_color[2], 0.85)
            Ellipse(pos=(center_x - base_radius, center_y - base_radius),
                    size=(base_radius * 2, base_radius * 2))

            # Bright Inner Hotspot
            Color(1, 1, 1, 0.75)
            hotspot = base_radius * 0.45
            Ellipse(pos=(center_x - hotspot, center_y - hotspot),
                    size=(hotspot * 2, hotspot * 2))


class CyrasApp(App):
    def build(self):
        root = FloatLayout()

        # Top Header Title
        self.title_label = Label(
            text="CYRAS SOVEREIGN CORE",
            font_size='18sp',
            bold=True,
            color=(0.3, 0.7, 1.0, 0.9),
            size_hint=(1, None),
            height=60,
            pos_hint={'top': 0.95, 'center_x': 0.5}
        )
        root.add_widget(self.title_label)

        # Center Glowing Orb Widget
        self.orb = GlowingOrb(size_hint=(0.8, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.55})
        root.add_widget(self.orb)

        # Status / Subtitle Text
        self.status_label = Label(
            text="TAP ORB TO ACTIVATE",
            font_size='15sp',
            color=(0.7, 0.7, 0.7, 0.8),
            size_hint=(0.9, None),
            height=50,
            pos_hint={'center_x': 0.5, 'y': 0.18},
            halign='center'
        )
        root.add_widget(self.status_label)

        # Bottom System Info
        self.footer_label = Label(
            text="AUTONOMOUS DUPLEX ENGINE",
            font_size='11sp',
            color=(0.3, 0.3, 0.35, 1),
            size_hint=(1, None),
            height=30,
            pos_hint={'bottom': 0.03, 'center_x': 0.5}
        )
        root.add_widget(self.footer_label)

        return root

    def on_touch_down(self, touch):
        # Orb area me tap check
        if self.orb.collide_point(*touch.pos):
            self.trigger_interaction()
            return True
        return super(CyrasApp, self).on_touch_down(touch)

    def trigger_interaction(self):
        self.status_label.text = "Cyras Speaking..."
        self.orb.set_state("speaking")
        
        try:
            tts.speak("Welcome Boss! Cyras core is active and ready.")
        except Exception:
            pass

        # 3.5 seconds ke baad automatic wapas idle mode
        Clock.schedule_once(self.reset_to_idle, 3.5)

    def reset_to_idle(self, dt):
        self.status_label.text = "TAP ORB TO COMMUNICATE"
        self.orb.set_state("idle")


if __name__ == '__main__':
    CyrasApp().run()
