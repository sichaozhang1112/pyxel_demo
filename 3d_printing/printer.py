import pyxel
import random
from utils import *

class Printer:
    def __init__(self, circle_center_point, laser_points, circle_radius, circle_color):
        self.circle_center_point = circle_center_point
        self.screen_center_point = Point(pyxel.width/2, pyxel.height/2)
        self.laser_points = laser_points
        self.laser_point = circle_center_point
        self.circle_radius = circle_radius
        self.circle_color = circle_color

        # circle
        self.circle = []
        self.circle_angle = 0.0
        self.circle_finish = False

        # laser line
        self.laser_line_color = pyxel.COLOR_WHITE
        self.laser_line = []

    def get_finish_status(self):
        return self.circle_finish

    def update(self):
        draw_speed = 0.1
        screen_dist = 100
        to_center = LineSegment(Point(self.circle_center_point.x+self.circle_radius*math.cos(self.circle_angle), self.circle_center_point.y), self.screen_center_point)
        circle_point = to_center.get_point(self.circle_radius*math.sin(self.circle_angle)/screen_dist)
        self.circle.append(circle_point)
        self.laser_point = circle_point
        self.circle_angle += draw_speed
        if self.circle_angle > 2*math.pi:
            self.circle_angle = 0.0
            self.circle_finish = True

    def draw(self):
        if not self.circle_finish:
            for laser_point in self.laser_points:
                pyxel.line(laser_point.x, laser_point.y, self.laser_point.x, self.laser_point.y, self.laser_line_color)
        for point in self.circle:
            pyxel.pset(point.x, point.y, self.circle_color)
