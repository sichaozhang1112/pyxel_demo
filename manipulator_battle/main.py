import pyxel
import random
import math
import manipulator

import sys
sys.path.append("../common/")
import mouse
import utils

class ManipulatorInterface:
    def __init__(self, control_set, color, scree_boundary, chassis_center):
        self.move_left = control_set[0]
        self.move_right = control_set[1]
        self.attack = control_set[2]
        self.select_forward = control_set[3]
        self.select_backward = control_set[4]
        self.target_idx = random.randint(0, 2)
        self.pendulum_num = 3
        self.manipulator = manipulator.Manipulator(\
                self.pendulum_num, color, scree_boundary, chassis_center)
        self.is_dead = False
        self.dead_count = []
        for i in range(self.pendulum_num):
            self.dead_count.append(3+i)

    def check_dead(self):
        return self.is_dead

    def update(self, raw_target_points, opponent_end_point):
        all_link_points = self.manipulator.get_all_link_points()
        for i in range(len(all_link_points)):
            point = all_link_points[i]
            if utils.get_distance(point, opponent_end_point) < 1:
                if self.dead_count[i] > 0:
                    self.dead_count[i] -= 1
                else:
                    self.manipulator.remove_pendulum(i)
                break
        if self.manipulator.pendulum_num() <= 0:
            self.is_dead = True
            return

        move_direction = 0
        if pyxel.btn(self.move_left):
            move_direction = -1
        elif pyxel.btn(self.move_right):
            move_direction = 1

        if pyxel.btnp(self.select_forward):
            self.target_idx += 1
        elif pyxel.btnp(self.select_backward):
            self.target_idx -= 1

        end_point = self.manipulator.get_end_point()
        target_points = self.get_target_points(end_point, raw_target_points)
        gain = 1.0 * (self.pendulum_num+1-self.manipulator.pendulum_num())
        if pyxel.btn(self.attack):
            target_points = raw_target_points
            gain = 5.0

        self.target_idx += len(target_points)
        self.target_idx %= len(target_points)

        self.manipulator.update(target_points[self.target_idx], move_direction, gain)

    def draw(self):
        if self.is_dead:
            return
        self.manipulator.draw()
        all_link_points = self.manipulator.get_all_link_points()
        for i in range(len(all_link_points)):
            point = all_link_points[i]
            if self.dead_count[i] == 2:
                pyxel.circb(point.x, point.y, 2, pyxel.COLOR_RED)
            elif self.dead_count[i] <= 1:
                pyxel.circb(point.x, point.y, 2, pyxel.COLOR_RED)
                pyxel.circ(point.x, point.y, 1, pyxel.COLOR_RED)

    def get_target_points(self, end_point, target_points):
        points = []
        defense_dist = 30
        for point in target_points:
            line = utils.LineSegment(point, end_point)
            t = defense_dist / line.get_length()
            points.append(line.get_point(t))
        return points

class PlayGround:
    def __init__(self):
        self.width = 240
        self.height = 180
        self.mouse = mouse.Mouse()
        pyxel.init(self.width, self.height, title="manipulator battle")
        self.manipulators = []
        self.manipulators.append(ManipulatorInterface( \
                [pyxel.KEY_A, pyxel.KEY_D, pyxel.MOUSE_BUTTON_LEFT, pyxel.KEY_W, pyxel.KEY_S], pyxel.COLOR_GREEN, [0, self.width], utils.Point2D(30, 120)))
        pyxel.mouse(False)
        pyxel.run(self.update, self.draw)


    def update(self):
        self.mouse.update()
        for manipulator in self.manipulators:
            manipulator.update([self.mouse.get_position()], self.mouse.get_position())
            if manipulator.check_dead():
                return

    def draw(self):
        pyxel.cls(0)
        # print mouse position on screen
        pyxel.text(0, 0, "mouse x: " + str(pyxel.mouse_x) + " mouse y: " + str(pyxel.mouse_y), 7)
        self.mouse.draw()
        for manipulator in self.manipulators:
            if manipulator.check_dead():
                return
            manipulator.draw()
class Game:
    def __init__(self):
        self.width = 240
        self.height = 180
        self.mouse = mouse.Mouse()
        pyxel.init(self.width, self.height, title="manipulator battle")
        self.manipulators = []
        self.manipulators.append(ManipulatorInterface( \
                [pyxel.KEY_A, pyxel.KEY_D, pyxel.KEY_Q, pyxel.KEY_W, pyxel.KEY_S], pyxel.COLOR_GREEN, [0, self.width], utils.Point2D(30, 120)))
        self.manipulators.append(ManipulatorInterface( \
                [pyxel.KEY_LEFT, pyxel.KEY_RIGHT, pyxel.KEY_K, pyxel.KEY_UP, pyxel.KEY_DOWN], pyxel.COLOR_NAVY, [0, self.width], utils.Point2D(210, 120)))
        pyxel.mouse(False)
        pyxel.run(self.update, self.draw)


    def check_dead(self):
        for manipulator in self.manipulators:
            if manipulator.check_dead():
                return True
        return False

    def update(self):
        self.mouse.update()

        if self.check_dead():
            return
        target_points = self.manipulators[0].manipulator.get_all_link_points()
        opponent_end_point = self.manipulators[0].manipulator.get_end_point()
        self.manipulators[1].update(target_points, opponent_end_point)
        if self.check_dead():
            return
        target_points = self.manipulators[1].manipulator.get_all_link_points()
        opponent_end_point = self.manipulators[1].manipulator.get_end_point()
        self.manipulators[0].update(target_points, opponent_end_point)
        if self.check_dead():
            return

    def draw(self):
        pyxel.cls(0)
        # print mouse position on screen
        self.mouse.draw()
        for i in range(len(self.manipulators)):
            manipulator = self.manipulators[i]
            if manipulator.check_dead():
                pyxel.text(0, 0, "game over", 7)
                if i == 0:
                    pyxel.text(0, 10, "navy win", 7)
                else:
                    pyxel.text(0, 10, "green win", 7)
                return
            manipulator.draw()

PlayGround()
