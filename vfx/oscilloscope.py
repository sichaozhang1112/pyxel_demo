import pyxel
import random
import math
from collections import namedtuple
from enum import Enum

Point2D = namedtuple('Point2D', ['x', 'y'])

class OscilloscopeType(Enum):
    TYPE_1 = 1
    TYPE_2 = 2

class CoordTransform:
    def __init__(self, angle):
        self.angle_ = angle

    def Trans(self, point):
        x = point.x * math.cos(self.angle_) - point.y * math.sin(self.angle_)
        y = point.x * math.sin(self.angle_) + point.y * math.cos(self.angle_)
        return Point2D(x, y)

class Oscilloscope:
    def __init__(self):
        self.center_x = 80
        self.center_y = 60

        pyxel.init(2*self.center_x, 2*self.center_y, title="Oscilloscope")
        pyxel.mouse(False)

        self.x_freq = 1
        self.y_freq = 1
        self.points = set()
        self.color = pyxel.COLOR_GREEN
        self.angle = 0.0

        self.is_pause = False
        self.type = OscilloscopeType.TYPE_2

        pyxel.run(self.update, self.draw)

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        for point in self.points:
            pyxel.pset(self.center_x + point.x, self.center_y + point.y, self.color)

        if self.is_pause:
            color = pyxel.COLOR_RED
        else:
            color = pyxel.COLOR_GREEN
        if self.type is OscilloscopeType.TYPE_1:
            pyxel.line(self.center_x-30, self.center_y-30, self.center_x+30, self.center_y-30, color)
            pyxel.line(self.center_x+30, self.center_y-30, self.center_x+30, self.center_y+30, color)
            pyxel.line(self.center_x+30, self.center_y+30, self.center_x-30, self.center_y+30, color)
            pyxel.line(self.center_x-30, self.center_y+30, self.center_x-30, self.center_y-30, color)
        elif self.type is OscilloscopeType.TYPE_2:
            pyxel.circb(self.center_x, self.center_y, 30, color)

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.is_pause = not self.is_pause

        if pyxel.btnp(pyxel.KEY_1):
            self.type = OscilloscopeType.TYPE_1
        elif pyxel.btnp(pyxel.KEY_2):
            self.type = OscilloscopeType.TYPE_2

        if not self.is_pause:
            self.x_freq = random.randint(1, 10)
            self.y_freq = random.randint(1, 10)

        self.points = set()

        if self.type is OscilloscopeType.TYPE_1:
            for i in range(0, 0+360):
                radius = i * math.pi / 180
                x = 30 * math.cos(self.x_freq * radius)
                y = 30 * math.sin(self.y_freq * radius)
                self.points.add(Point2D(x, y))
        elif self.type is OscilloscopeType.TYPE_2:
            for i in range(0, 0+360, int(self.y_freq)):
                radius = i * math.pi / 180
                length = 30 * math.cos(self.x_freq * radius)
                x = length * math.cos(radius)
                y = length * math.sin(radius)
                self.points.add(Point2D(x, y))


Oscilloscope()
