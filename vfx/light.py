import pyxel
import numpy
import math
from collections import namedtuple
from enum import Enum
import sys
sys.path.append('../common')
import utils
import mouse

ColorPoint = namedtuple('ColorPoint', ['x', 'y', 'color'])
Point3D = namedtuple('Point3D', ['x', 'y', 'z'])

class LightStatus(Enum):
    LIT = 1
    SHADOW = 2
    VAGUE = 3

class Light:
    def __init__(self, position, direction):
        # position and direction is Point3D
        self.position = position
        self.direction = direction
        if numpy.linalg.norm(self.direction) > 1e-3:
            self.direction = self.direction / numpy.linalg.norm(self.direction)
        self.expand_coeff = 2
        self.max_radius = 100
        self.shadow_color = pyxel.COLOR_BLACK
        self.light_color = pyxel.COLOR_YELLOW

    def update_position(self, position):
        self.position = position

    def update_direction(self, direction):
        self.direction = direction
        if numpy.linalg.norm(self.direction) > 1e-3:
            self.direction = self.direction / numpy.linalg.norm(self.direction)

    def draw(self):
        light_radius = self.max_radius - self.expand_coeff * self.position.z
        pyxel.circ(self.position.x, self.position.y, light_radius, self.light_color)
        vague_radius = light_radius * 0.2
        radius = int(light_radius)
        fibo = 1
        while (radius >= vague_radius):
            point_radius = 1
            for j in range(0, 360, fibo):
                x = self.position.x + radius * math.cos(math.radians(j))
                y = self.position.y + radius * math.sin(math.radians(j))
                pyxel.circ(x, y, point_radius, self.shadow_color)
            fibo += fibo
            radius = light_radius - fibo

class VFX:
    def __init__(self):
        pyxel.init(160, 120, title="vfx")
        pyxel.mouse(False)

        self.light = Light(Point3D(0, 0, 1), Point3D(0, 0, -1))
        self.mouse = mouse.Mouse()
        self.center = utils.Point2D(pyxel.width/2, pyxel.height/2)
        self.light_height = 45

        # run
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_S):
            self.light_height += 1
        elif pyxel.btn(pyxel.KEY_W):
            self.light_height -= 1
        self.light_height = max(0, self.light_height)
        self.light_height = min(90, self.light_height)
        light_pos = Point3D(pyxel.mouse_x, pyxel.mouse_y, self.light_height)
        light_dir = Point3D(0, 0, -1)
        self.light.update_position(light_pos)
        self.light.update_direction(light_dir)
        self.mouse.update()

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)

        self.light.draw()
        self.mouse.draw()

VFX()
