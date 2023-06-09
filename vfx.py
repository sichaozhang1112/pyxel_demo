import pyxel
import numpy
import random
import math
from collections import namedtuple
from enum import Enum

Point2D = namedtuple('Point2D', ['x', 'y'])
ColorPoint2D = namedtuple('ColorPoint2D', ['x', 'y', 'color'])
Point3D = namedtuple('Point3D', ['x', 'y', 'z'])

class LineSegment:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_point(self, t):
        return Point2D(self.start.x + t*(self.end.x-self.start.x), self.start.y + t*(self.end.y-self.start.y))

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

    def update_position(self, position):
        self.position = position

    def update_direction(self, direction):
        self.direction = direction
        if numpy.linalg.norm(self.direction) > 1e-3:
            self.direction = self.direction / numpy.linalg.norm(self.direction)

    def is_lit(self, point):
        # calculate cross profuct of light direction and point
        point_rel_light = numpy.array([point.x, point.y, point.z]) \
                - numpy.array([self.position.x, self.position.y, self.position.z])
        vertical_dist = numpy.linalg.norm(numpy.cross(self.direction, point_rel_light))
        horizontal_dist = numpy.linalg.norm(numpy.dot(self.direction, point_rel_light))
        light_radius = self.max_radius - self.expand_coeff * horizontal_dist
        light_radius = max(0.0, light_radius)
        vague_radius = light_radius * 0.8
        if vertical_dist > light_radius:
            if vertical_dist > vague_radius:
                return LightStatus.VAGUE
            return LightStatus.SHADOW
        return LightStatus.LIT

class CelShading:
    def __init__(self, light, dist_to_vision_disappear ,shadow_color):
        self.shadow_color = shadow_color
        self.light = light
        self.disappear_dist = dist_to_vision_disappear

    def update_light(self, light):
        self.light = light

    def shade(self, points):
        shaded_points = []
        for point in points:
            lit = self.light.is_lit(Point3D(point.x, point.y, 0))
            if lit == LightStatus.LIT:
                shaded_points.append(ColorPoint2D(point.x, point.y, point.color))
            elif lit == LightStatus.SHADOW:
                shaded_points.append(ColorPoint2D(point.x, point.y, self.shadow_color))
            elif lit == LightStatus.VAGUE:
                if (random.random() < 0.5):
                    shaded_points.append(ColorPoint2D(point.x, point.y, point.color))
                else:
                    shaded_points.append(ColorPoint2D(point.x, point.y, self.shadow_color))

        return shaded_points

class Mouse:
    def __init__(self):
        # cross
        self.cross_angle = 0
        self.cross_radius = 4
        self.cross_color = pyxel.COLOR_RED

    def update(self):
        # update cross
        self.cross_angle = (self.cross_angle + 0.1) % (2*math.pi)

    def draw(self):
        # draw cross
        cross_line_1 = self.get_cross_line(self.cross_radius, self.cross_angle)
        cross_line_2 = self.get_cross_line(self.cross_radius, self.cross_angle+math.pi/2)
        pyxel.line(cross_line_1.get_start().x+pyxel.mouse_x,\
                cross_line_1.get_start().y+pyxel.mouse_y,\
                cross_line_1.get_end().x+pyxel.mouse_x,\
                cross_line_1.get_end().y+pyxel.mouse_y, self.cross_color)
        pyxel.line(cross_line_2.get_start().x+pyxel.mouse_x,\
                cross_line_2.get_start().y+pyxel.mouse_y,\
                cross_line_2.get_end().x+pyxel.mouse_x,\
                cross_line_2.get_end().y+pyxel.mouse_y, self.cross_color)

    def get_cross_line(self, radius, angle):
        return LineSegment(Point2D(radius*math.cos(angle+math.pi), radius*math.sin(angle+math.pi)),\
                Point2D(radius*math.cos(angle), radius*math.sin(angle)))

class VFX:
    def __init__(self):
        pyxel.init(160, 120, title="vfx")
        pyxel.mouse(False)

        self.light = Light(Point3D(0, 0, 1), Point3D(0, 0, -1))
        self.cel_shading = CelShading(self.light, 1, pyxel.COLOR_NAVY)
        self.mouse = Mouse()
        self.center = Point2D(pyxel.width/2, pyxel.height/2)

        # run
        pyxel.run(self.update, self.draw)

    def update(self):
        light_pos = Point3D(pyxel.mouse_x-self.center.x, pyxel.mouse_y-self.center.y, 70)
        light_dir = Point3D(-light_pos.x, -light_pos.y, -light_pos.z)
        self.light.update_position(light_pos)
        self.light.update_direction(light_dir)
        self.mouse.update()
        self.cel_shading.update_light(self.light)

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)

        # draw a ball in the middle of screen
        points_of_ball = set()
        ball_radius = 20
        for i in range(0, 360, 1):
            for j in range(ball_radius):
                x = j * pyxel.cos(i)
                y = j * pyxel.sin(i)
                color = pyxel.COLOR_RED
                points_of_ball.add(ColorPoint2D(x, y, color))

        # use cel shading to make ball looks like 3d
        points_of_ball = self.cel_shading.shade(points_of_ball)

        # draw ball
        for point in points_of_ball:
            pyxel.pset(self.center.x+point.x, self.center.y+point.y, point.color)

        self.mouse.draw()

VFX()
