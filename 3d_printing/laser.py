import pyxel
import math
import random
from utils import Point, LineSegment

class Laser:
    def __init__(self, point):
        self.center_point = point

        self.laser_num = 4
        self.laser_color = []
        color_choice = [pyxel.COLOR_LIME, pyxel.COLOR_GREEN, pyxel.COLOR_WHITE]
        for i in range(self.laser_num):
            self.laser_color.append(random.choice(color_choice))

        self.laser_radius = []
        for i in range(self.laser_num):
            self.laser_radius.append(random.randint(10, 15))

        self.laser_angle = []
        for i in range(self.laser_num):
            self.laser_angle.append(random.random()*math.pi/self.laser_num+i*math.pi/self.laser_num)

        self.laser_speed = []
        for i in range(self.laser_num):
            self.laser_speed.append(random.randint(1, 2)/10)

    def update(self):
        for i in range(self.laser_num):
            self.laser_angle[i] = (self.laser_angle[i] + self.laser_speed[i]) % (2*math.pi)

    def draw(self):
        for i in range(self.laser_num):
            laser_line_1 = self.get_laser_line(self.laser_radius[i], self.laser_angle[i])
            laser_line_2 = self.get_laser_line(self.laser_radius[i], self.laser_angle[i]+math.pi)
            pyxel.line(laser_line_1.get_start().x+self.center_point.x, laser_line_1.get_start().y+self.center_point.y, laser_line_1.get_end().x+self.center_point.x, laser_line_1.get_end().y+self.center_point.y, self.laser_color[i])
            pyxel.line(laser_line_2.get_start().x+self.center_point.x, laser_line_2.get_start().y+self.center_point.y, laser_line_2.get_end().x+self.center_point.x, laser_line_2.get_end().y+self.center_point.y, self.laser_color[i])

    def get_laser_line(self, radius, angle):
        return LineSegment(Point(radius*math.cos(angle+math.pi), radius*math.sin(angle+math.pi)), Point(radius*math.cos(angle), radius*math.sin(angle)))
