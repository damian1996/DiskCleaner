from math import sin, cos, radians
from itertools import chain
from functools import lru_cache

import numpy as np
import matplotlib.colors as mplcolors

from kivy.utils import rgba
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.text import Label as CoreLabel
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics import *


class PlotWidget(RelativeLayout):
    colors = [
        ["#fce94f",	"#edd400",	"#c4a000"],
        ["#fcaf3e",	"#f57900",	"#ce5c00"],
        ["#e9b96e",	"#c17d11",	"#8f5902"],
        ["#8ae232",	"#73d216",	"#4e9a06"],
        ["#729fcf",	"#3465a4",	"#204a87"],
        ["#ad7fa8",	"#75507b",	"#5c3566"],
        ["#ef2920",	"#cc0000",	"#a40000"],
    ]

    def __init__(self, node, **kwargs):
        super(PlotWidget, self).__init__(**kwargs)
        self.node = node
        self.bind(size=self.draw)
        self.mouse_pos = None
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.segment_points_cache = {}
        self.draw()

    @lru_cache(maxsize=64)
    def get_points(self, cx, cy, r, angle_start, angle_end):
        segments = (angle_end-angle_start)//2+1
        x = -r * np.sin(-np.radians(
            np.linspace(angle_start, angle_end, segments))) + cx
        y = r * np.cos(-np.radians(
            np.linspace(angle_start, angle_end, segments))) + cy
        return x, y

    def get_polygon_points(self, cx, cy, r, segment_width,
                           angle_start, angle_end):
        x0, y0 = self.get_points(
            cx, cy, r, angle_start, angle_end)
        x1, y1 = self.get_points(
            cx, cy, r+segment_width, angle_start, angle_end)
        points = np.empty((x0.size*8,), dtype="float32")
        points[0::8] = x0
        points[1::8] = y0
        points[4::8] = x1
        points[5::8] = y1
        return points

    def get_line_points(self, cx, cy, r, segment_width,
                        angle_start, angle_end):
        x0, y0 = self.get_points(cx, cy, r, angle_start, angle_end)
        x1, y1 = self.get_points(
            cx, cy, r+segment_width, angle_start, angle_end)
        points = np.empty((x0.size*4+2,), dtype="float32")
        points[0::2] = np.concatenate([x0, x1[::-1], [x0[0]]])
        points[1::2] = np.concatenate([y0, y1[::-1], [y0[0]]])
        return list(points)

    def mouse_in_segment(self, cx, cy, r, segment_width,
                         angle_start, angle_end):
        if not self.mouse_pos:
            return False
        mouse_x, mouse_y = self.mouse_pos
        mouse_x -= cx + self.pos[0]
        mouse_y -= cy + self.pos[1]
        mouse_r = np.sqrt(mouse_x*mouse_x + mouse_y*mouse_y)
        if mouse_r < r or mouse_r > r + segment_width:
            return False
        phi = np.arctan2(-mouse_x, -mouse_y) + np.pi
        return radians(angle_start) < phi and phi < radians(angle_end)

    def get_highlighed_color(self, color):
        rgb = mplcolors.hex2color(color)
        h, s, v = mplcolors.rgb_to_hsv(
            np.array(rgb).reshape(1, 1, 3)).reshape(3)
        v += 0.4
        c = mplcolors.hsv_to_rgb((h, s, v))
        return c

    def draw_segment(self, cx, cy, r, segment_width, angle_start,
                     angle_end, color, highlighted):
        if highlighted:
            Color(*self.get_highlighed_color(color))
        else:
            Color(*rgba(color))
        vertices = self.get_polygon_points(
            cx, cy, r, segment_width, angle_start, angle_end)
        Mesh(vertices=vertices, mode="triangle_strip",
             indices=range(len(vertices)//4))
        Color(0, 0, 0)
        SmoothLine(points=self.get_line_points(
            cx, cy, r, segment_width, angle_start, angle_end), close=True)

    def on_mouse_pos(self, w, p):
        self.mouse_pos = p
        self.draw()

    def draw_plot(self, node, color=None, depth=0,
                  angle=0, parent_angle=360):
        if depth > 2:
            return None
        highlighted_node = None
        for idx, child in enumerate(node.get_children()):
            segm_color = (idx % len(self.colors)) if color is None else color
            w, h = self.size
            child_angle = child.get_size() / \
                child.get_size_parent_directory() * parent_angle
            if child_angle < 2:
                continue
            cx = w/2
            cy = h/2
            r = 100+50*depth
            segment_width = 50
            angle_start = angle
            angle_end = angle+child_angle
            mouse_in_segment = self.mouse_in_segment(
                cx, cy, r, segment_width, angle_start, angle_end)
            if mouse_in_segment:
                highlighted_node = child
            self.draw_segment(
                cx, cy, r, segment_width, angle_start,
                angle_end, self.colors[segm_color][depth], mouse_in_segment)
            highlighted_node = self.draw_plot(
                child, segm_color, depth+1, angle, child_angle) or \
                highlighted_node
            angle += child_angle
        if highlighted_node and depth == 0:
            label = CoreLabel(text=highlighted_node.get_name(), font_size=20)
            label.refresh()
            text = label.texture
            Rectangle(size=text.size, pos=(0, 0), texture=text)
        return highlighted_node

    def draw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(60/256, 62/256, 75/256)
            Rectangle(pos=(0, 0), size=self.size)
            self.draw_plot(self.node)
