import pyxel
import random
from printer import *
from utils import *

class Painter:
    def __init__(self):
        self.painting = []
        self.painting_finished = False
        self.min_painting_num = 5
        self.printers = []
        self.painting_color = random.randint(1, 15)
        self.printing_cnt = 0
        self.printing_finished = False

    def get_finish_status(self):
        if len(self.painting) < self.min_painting_num:
            return False
        return self.painting_finished

    def update_painting(self, point):
        min_interval = 1
        if len(self.painting) >= 1:
            if self.painting[-1].x == point.x and self.painting[-1].y == point.y:
                return
            if len(self.painting) > self.min_painting_num and get_distance(self.painting[0], point) < 5:
                self.painting_finished = True
                self.painting.sort(key=lambda p: p.y, reverse=True)
                return
            if abs(self.painting[-1].y - point.y) > min_interval:
                if (self.painting[-1].y - point.y) > 0:
                    lower_point = point
                    higher_point = self.painting[-1]
                else:
                    lower_point = self.painting[-1]
                    higher_point = point
                for i in range(lower_point.y, higher_point.y, min_interval):
                    line = LineSegment(lower_point, higher_point)
                    ratio = (i-lower_point.y) / (higher_point.y-lower_point.y)
                    self.painting.append(line.get_point(ratio))
        self.painting.append(point)

    def update_printers(self, laser_points):
            if self.printing_cnt < len(self.painting) - 1:
                if self.painting[self.printing_cnt].y == self.painting[self.printing_cnt+1].y:
                    circle_center_point = Point((self.painting[self.printing_cnt].x+self.painting[self.printing_cnt+1].x)/2,self.painting[self.printing_cnt].y)
                    circle_radius = get_distance(self.painting[self.printing_cnt], self.painting[self.printing_cnt+1])/2.0
                    self.printers.append(Printer(circle_center_point, laser_points, circle_radius, self.painting_color))
                    self.printing_cnt += 2
                else:
                    self.printing_cnt += 1

            for printer in self.printers:
                printer.update()

            if self.printing_cnt >= len(self.painting) - 1:
                for printer in self.printers:
                    if not printer.get_finish_status():
                        return
                self.printing_finished = True

    def update(self, point, laser_points):
        if not self.painting_finished:
            self.update_painting(point)
        elif not self.printing_finished:
            self.update_printers(laser_points)
        else:
            return

    def draw(self):
        if not self.printing_finished:
            for point in self.painting:
                pyxel.pset(point.x, point.y, self.painting_color)

        for printer in self.printers:
            printer.draw()
