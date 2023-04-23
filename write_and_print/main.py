# write and print in pyxel
import pyxel
from utils import Point

class WriteAndPrint:
    def __init__(self):
        # set font size
        pyxel.FONT_WIDTH = 5
        pyxel.FONT_HEIGHT = 5
        pyxel.init(100, 100)
        self.line = '$'
        self.cached_line = []
        self.line_start = Point(0, 0)

        pyxel.run(self.update, self.draw)

    def draw(self):
        pyxel.cls(0)

        # print self.line on screen
        for i in range(len(self.cached_line)):
            pyxel.text(0, i * pyxel.FONT_HEIGHT, self.cached_line[i], 7)
        pyxel.text(self.line_start.x, self.line_start.y, self.line, 7)

    def update(self):
        # update texts that keyboard input
        # monitor the keyboard input
        if self.check_input() == 'enter':
            self.line_start.y += pyxel.FONT_HEIGHT
            self.line_start.x = 0
            self.cached_line.append(self.line)
            self.line = '$'
        else:
            self.line += self.check_input()

    def check_input(self):
        # check if the key is pressed
        for key in range(0, 255):
            if pyxel.btnp(key):
                print(key)
                if key == 13:
                    return 'enter'
                return chr(key)
        return ''

WriteAndPrint()
