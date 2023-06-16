import pyxel
import math

import sys
sys.path.append('../common/')
import utils

class Pendulum:
    def __init__(self, length, start_point, color=pyxel.COLOR_WHITE):
        self.length = length
        self.update(start_point, -math.pi/2)
        self.color = color

    def update(self, new_start_point, new_angle):
        self.start_point = new_start_point
        self.angle = new_angle
        self.end_point = utils.Point2D(self.start_point.x + self.length * math.cos(self.angle), \
                self.start_point.y + self.length * math.sin(self.angle))

    def draw(self):
        pyxel.line(self.start_point.x, self.start_point.y, self.end_point.x, self.end_point.y, self.color)
        pyxel.circ(self.start_point.x, self.start_point.y, 2, self.color)

    def get_end_point(self):
        return self.end_point

    def get_start_point(self):
        return self.start_point

    def get_angle(self):
        return self.angle

class Chassis:
    def __init__(self, width, height, center_point, screen_boundary, color=pyxel.COLOR_WHITE):
        self.left_boundary = screen_boundary[0]
        self.right_boundary = screen_boundary[1]
        self.width = width
        self.height = height
        self.center_point = center_point
        self.velocity = 1.0
        self.color = color
        self.wheel_radius = self.height / 2
        self.update(0)

    def update(self, move_direction):
        center_x = self.center_point.x + self.velocity * move_direction
        if center_x < self.left_boundary:
            center_x = self.left_boundary
        elif center_x > self.right_boundary:
            center_x = self.right_boundary
        self.center_point = utils.Point2D(center_x, self.center_point.y)
        self.left_wheel_center = utils.Point2D(self.center_point.x - self.width / 2, self.center_point.y + self.height / 2)
        self.right_wheel_center = utils.Point2D(self.center_point.x + self.width / 2, self.center_point.y + self.height / 2)

    def draw(self):
        pyxel.rectb(self.center_point.x - self.width / 2, self.center_point.y - self.height / 2, self.width, self.height, self.color)
        pyxel.circ(self.left_wheel_center.x, self.left_wheel_center.y, self.wheel_radius, self.color)
        pyxel.circ(self.right_wheel_center.x, self.right_wheel_center.y, self.wheel_radius, self.color)

    def get_link_point(self):
        return utils.Point2D(self.center_point.x, self.center_point.y - self.height / 2)

class Manipulator:
    def __init__(self, pendulum_num, color, screen_boundary, chassis_center):
        self.chassis = Chassis(20, 10, chassis_center, screen_boundary, color)
        self.pendulums = []
        link_point = self.chassis.get_link_point()
        for i in range(pendulum_num):
            self.pendulums.append(Pendulum(20, link_point, color))
            link_point = self.pendulums[i].get_end_point()
        self.angular_velocity = 0.1

    def update(self, target_point, move_direction, gain):
        self.chassis.update(move_direction)
        self.angles = self.get_angles()
        self.dist_to_target = utils.get_distance(self.get_end_point(), target_point)

        all_angles = []
        for i in range(len(self.pendulums)):
            to_pick_angle = [-self.angular_velocity*gain, 0.0, self.angular_velocity*gain]
            to_pick_angle = [angle + self.pendulums[i].get_angle() for angle in to_pick_angle]
            all_angles.append(to_pick_angle)

        self.calc_optimal_pendulun(self.pendulums, all_angles, 0, target_point)
        self.update_pendulum(self.angles)

    def draw(self):
        self.chassis.draw()
        for pendulum in self.pendulums:
            pendulum.draw()
        end_point = self.get_end_point()
        pyxel.circ(end_point.x, end_point.y, 2, pyxel.COLOR_RED)

    def remove_pendulum(self, index):
        for i in range(index, len(self.pendulums)):
            self.pendulums.pop()

    def get_angles(self):
        return [pendulum.get_angle() for pendulum in self.pendulums]

    def get_end_point(self):
        return self.pendulums[-1].get_end_point()

    def get_all_link_points(self):
        points = []
        for i in range(len(self.pendulums)):
            points.append(self.pendulums[i].get_start_point())
        return points

    def pendulum_num(self):
        return len(self.pendulums)

    def update_pendulum(self, angles):
        link_point = self.chassis.get_link_point()
        for i in range(len(self.pendulums)):
            self.pendulums[i].update(link_point, angles[i])
            link_point = self.pendulums[i].get_end_point()
        self.end_point = self.pendulums[-1].get_end_point()

    def calc_optimal_pendulun(self, pendulums, all_angles, pend_idx, target_point):
        if pend_idx == len(pendulums):
            end_point = pendulums[-1].get_end_point()
            dist = utils.get_distance(end_point, target_point)
            if dist < self.dist_to_target:
                self.dist_to_target = dist
                self.angles = [pendulum.get_angle() for pendulum in pendulums]
            return
        if pend_idx == 0:
            link_point = self.chassis.get_link_point()
        else:
            link_point = pendulums[pend_idx - 1].get_end_point()

        for angle in all_angles[pend_idx]:
            pendulums[pend_idx].update(link_point, angle)
            self.calc_optimal_pendulun(pendulums, all_angles, pend_idx + 1, target_point)
