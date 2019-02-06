from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.properties import NumericProperty
from kivy.graphics import *


class LoadingWidget(FloatLayout):
    angle = NumericProperty(0)

    def __init__(self, diameter=150, **kwargs):
        super(LoadingWidget, self).__init__(**kwargs)
        self.diameter = diameter
        anim = Animation(angle=360, duration=1)
        anim += Animation(angle=360, duration=1)
        anim.repeat = True
        anim.start(self)
        self.draw(0)

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0
        self.draw(angle)

    def draw(self, angle):
        with self.canvas:
            self.canvas.clear()
            Color(1., 1, 1)
            w, h = self.size
            SmoothLine(ellipse=(
                w/2-self.diameter/2, h/2-self.diameter/2,
                self.diameter, self.diameter, angle, angle+90), width=10)
