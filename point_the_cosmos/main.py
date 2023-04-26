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
        if (self.is_selected):
            pyxel.rectb(self.x-self.r*3, self.y-self.r*3, self.r*7, self.r*7, pyxel.COLOR_RED)

class PointCosmos:
    def __init__(self):
        pyxel.init(160, 120, title="Point Cosmos")

        # mouse
        pyxel.mouse(False)
        self.mouse_radius_1 = 4
        self.mouse_radius_2 = 4
        self.mouse_angle_1 = 0
        self.mouse_angle_2 = 0
        self.mouse_color_1 = pyxel.COLOR_LIME
        self.mouse_color_2 = pyxel.COLOR_GREEN

        # stars
        self.stars = []
        for i in range(random.randint(50, 100)):
            self.stars.append(Star())

        # run
        pyxel.run(self.update, self.draw)

    def get_mouse_line(self, radius, angle):
        return LineSegment(Point(radius*math.cos(angle+math.pi), radius*math.sin(angle+math.pi)), Point(radius*math.cos(angle), radius*math.sin(angle)))

    def update(self):
        # update mouse pointer line
        self.mouse_angle_1  = (self.mouse_angle_1 + 0.09) % (2*math.pi)
        self.mouse_angle_2  = (self.mouse_angle_2 + 0.13) % (2*math.pi)
        
        # update stars
        for star in self.stars:
            if (star.update()):
                self.stars.remove(star)
                if random.random() > 0.7:
                    self.stars.append(Star())
        if random.random() > 0.7:
            self.stars.append(Star())
           
    def draw(self):
        pyxel.cls(0)

        # draw stars
        for star in self.stars:
            star.draw()

        # draw mouse
        mouse_line_1 = self.get_mouse_line(self.mouse_radius_1, self.mouse_angle_1)
        mouse_line_2 = self.get_mouse_line(self.mouse_radius_2, self.mouse_angle_2)
        pyxel.line(mouse_line_1.start.x+pyxel.mouse_x, mouse_line_1.start.y+pyxel.mouse_y, mouse_line_1.end.x+pyxel.mouse_x, mouse_line_1.end.y+pyxel.mouse_y, int(self.mouse_color_1))
        pyxel.line(mouse_line_2.start.x+pyxel.mouse_x, mouse_line_2.start.y+pyxel.mouse_y, mouse_line_2.end.x+pyxel.mouse_x, mouse_line_2.end.y+pyxel.mouse_y, int(self.mouse_color_2))

PointCosmos()
