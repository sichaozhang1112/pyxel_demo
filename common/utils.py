import math
import random
from collections import namedtuple

Point2D = namedtuple('Point2D', ['x', 'y'])
Circle = namedtuple('Circle', ['center', 'radius'])

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

    def get_length(self):
        return get_distance(self.start, self.end)

def get_distance(point1, point2):
    return math.sqrt((point1.x-point2.x)**2 + (point1.y-point2.y)**2)
