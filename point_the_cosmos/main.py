import pyxel
import math
import random
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
Circle = namedtuple('Circle', ['center', 'radius'])
LineSegment = namedtuple('LineSegment', ['start', 'end'])

class Star:
    def __init__(self):
        self.x = random.randint(0, pyxel.width-10)
        self.y = random.randint(0, pyxel.height-10)
        self.r = 1
        self.c = random.randint(1, 15)
        self.destroy_cnt = self.r
        self.is_destroying = False
        self.create_cnt = 0
        self.is_creating = True
        self.is_dead = False
        self.is_selected = False

    def check_point(self, point):
        return (point.x-self.x)**2 + (point.y-self.y)**2 <= (self.r+5)**2

    def update(self):
        if (self.is_creating):
            self.create_cnt += random.random() * 0.5
            if (self.create_cnt >= self.r):
                self.is_creating = False
        else:
            self.is_selected = self.check_point(Point(pyxel.mouse_x, pyxel.mouse_y))
            if (self.is_destroying):
                self.destroy_cnt -= 0.5
                if (self.destroy_cnt <= 0):
                    self.is_dead = True
            else:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    self.is_destroying = self.is_selected
        return self.is_dead

    def draw(self):
        if (self.is_creating):
            pyxel.circ(self.x, self.y, int(self.create_cnt), self.c)
        elif (self.is_destroying):
            pyxel.circ(self.x, self.y, int(self.destroy_cnt), self.c)
        else:
            pyxel.circ(self.x, self.y, self.r, self.c)
