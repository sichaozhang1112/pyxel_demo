import pyxel
import sys
sys.path.append('../common/')
import utils

class Pendulum:
    def __init__(self, length, start_point, color=pyxel.COLOR_WHITE):
        self.length = length
        self.update(start_point, 0.0)
        self.color = color

    def update(self, new_start_point, new_angle):
        self.start_point = new_start_point
        self.angle = new_angle
        self.end_point = utils.Point2D(self.start_point.x + self.length * utils.cos(self.angle), \
                self.start_point.y + self.length * utils.sin(self.angle))

    def draw(self):
        pyxel.line(self.start_point.x, self.start_point.y, self.end_point.x, self.end_point.y, self.color)
        pyxel.circ(self.start_point.x, self.start_point.y, 2, self.color)

    def get_end_point(self):
        return self.end_point

class Chassis:
    def __init__(self, width, height, center_point, color=pyxel.COLOR_WHITE):
        self.width = width
        self.height = height
        self.update(center_point)
        self.color = color
        self.wheel_radius = self.height / 2

    def update(self, new_center_point):
        self.center_point = new_center_point
        self.left_wheel_center = utils.Point2D(self.center_point.x - self.width / 2, self.center_point.y - self.height / 2)
        self.right_wheel_center = utils.Point2D(self.center_point.x + self.width / 2, self.center_point.y - self.height / 2)

    def draw(self):
        pyxel.rect(self.center_point.x - self.width / 2, self.center_point.y + self.height / 2, self.width, self.height, self.color)
        pyxel.circ(self.left_wheel_center.x, self.left_wheel_center.y, self.wheel_radius, self.color)
        pyxel.circ(self.right_wheel_center.x, self.right_wheel_center.y, self.wheel_radius, self.color)
