import pyxel
import random
from mouse import Mouse
from laser import Laser
from utils import Point
from painter import Painter

class ThreeDPrinting:
    def __init__(self):
        self.win_width = 480
        self.win_height = 320
        pyxel.init(self.win_width, self.win_height, title="3D Printing")

        # mouse and laser
        pyxel.mouse(False)
        self.mouse_num = 2
        self.mouse = []
        self.laser = []
        self.laser_points = []
        for i in range(self.mouse_num):
            if random.random() >= 0.0:
                laser_point = Point(random.randint(0, self.win_width), 0)
            elif random.random() >= 0.5:
                laser_point = Point(0, random.randint(0, self.win_height))
            elif random.random() >= 0.25:
                laser_point = Point(random.randint(0, self.win_width), self.win_height)
            else:
                laser_point = Point(self.win_width, random.randint(0, self.win_height))
            self.laser_points.append(laser_point)
            self.mouse.append(Mouse(laser_point))
            self.laser.append(Laser(laser_point))

        self.hide_mouse = False

        # painter
        self.painters = []
        self.ready_to_paint = True
        self.painter_color = 1

        pyxel.run(self.update, self.draw)

    def update(self):
        # monitor button status
        if pyxel.btnp(pyxel.KEY_A):
            self.painter_color = (self.painter_color + 1) % 16
            if self.painter_color <= 1:
                self.painter_color = 1
        elif pyxel.btnp(pyxel.KEY_D):
            self.painter_color = (self.painter_color - 1) % 16
            if self.painter_color <= 1:
                self.painter_color = 15

        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            if len(self.painters) == 0:
                self.painters.append(Painter(self.painter_color))
            else:
                if self.painters[-1].get_finish_status():
                    self.painters.append(Painter(self.painter_color))
        else:
            if len(self.painters) > 0:
                if not self.painters[-1].get_finish_status():
                    self.painters.pop(-1)

        if pyxel.btnp(pyxel.KEY_H):
            self.hide_mouse = not self.hide_mouse
            
        if pyxel.btnp(pyxel.KEY_R):
            if len(self.painters) > 0:
                self.painters.pop(-1)

        if pyxel.btnp(pyxel.KEY_C):
            self.painters = []

        # update
        for i in range(self.mouse_num):
            self.mouse[i].update(self.painter_color)
            self.laser[i].update()

        for painter in self.painters:
            painter.update(Point(pyxel.mouse_x, pyxel.mouse_y), self.laser_points)

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)

        for painter in self.painters:
            painter.draw()

        if not self.hide_mouse:
            for i in range(self.mouse_num):
                self.mouse[i].draw()
                self.laser[i].draw()

ThreeDPrinting()
