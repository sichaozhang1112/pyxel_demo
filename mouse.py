import pyxel
import utils
import math

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

    def get_position(self):
        return utils.Point2D(pyxel.mouse_x, pyxel.mouse_y)

    def get_cross_line(self, radius, angle):
        return utils.LineSegment(utils.Point2D(radius*math.cos(angle+math.pi), radius*math.sin(angle+math.pi)),\
                utils.Point2D(radius*math.cos(angle), radius*math.sin(angle)))
