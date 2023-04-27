import pyxel
import math
import random
from utils import Point, LineSegment

class Mouse:
    def __init__(self, point):
        self.center_point = point

        # cross
        self.cross_angle = 0
        self.cross_radius = 4
        self.cross_color = pyxel.COLOR_RED

        # thunder
        self.thunder_num = 5
        self.thunder_seg = []
        self.thunder_color = pyxel.COLOR_WHITE
        self.thunder_update_cnt = 3

    def update(self, color):
        # update cross
        self.cross_angle = (self.cross_angle + 0.1) % (2*math.pi)
        self.thunder_color = color

        # update thunder
        self.thunder_update_cnt -= 1
        if self.thunder_update_cnt > 0:
            return
        self.thunder_update_cnt = 3
        noise = 3
        mouse_point = Point(pyxel.mouse_x, pyxel.mouse_y)
        self.thunder_seg = [mouse_point]
        mouse_line = LineSegment(mouse_point, self.center_point)
        for i in range(self.thunder_num):
            point_on_line = mouse_line.get_point(random.random()/3+i/3)
            self.thunder_seg.append(Point(point_on_line.x+random.randint(-noise, noise), point_on_line.y+random.randint(-noise, noise)))
        self.thunder_seg.append(self.center_point)

    def draw(self):
        # draw thunder
        for i in range(len(self.thunder_seg)-1):
            pyxel.line(self.thunder_seg[i].x, self.thunder_seg[i].y, self.thunder_seg[i+1].x, self.thunder_seg[i+1].y, self.thunder_color)

        # draw cross
        cross_line_1 = self.get_cross_line(self.cross_radius, self.cross_angle)
        cross_line_2 = self.get_cross_line(self.cross_radius, self.cross_angle+math.pi/2)
        pyxel.line(cross_line_1.get_start().x+pyxel.mouse_x, cross_line_1.get_start().y+pyxel.mouse_y, cross_line_1.get_end().x+pyxel.mouse_x, cross_line_1.get_end().y+pyxel.mouse_y, self.cross_color)
        pyxel.line(cross_line_2.get_start().x+pyxel.mouse_x, cross_line_2.get_start().y+pyxel.mouse_y, cross_line_2.get_end().x+pyxel.mouse_x, cross_line_2.get_end().y+pyxel.mouse_y, self.cross_color)

    def get_cross_line(self, radius, angle):
        return LineSegment(Point(radius*math.cos(angle+math.pi), radius*math.sin(angle+math.pi)), Point(radius*math.cos(angle), radius*math.sin(angle)))
