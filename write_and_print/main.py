# write and print in pyxel
import pyxel
from terminal import Terminal

class WriteAndPrint:
    def __init__(self):
        # set font size
        pyxel.FONT_WIDTH = 7
        pyxel.FONT_HEIGHT = 7
        window_width = 200
        window_height = 200
        pyxel.init(window_width, window_height, fps=60)

        self.terminal = Terminal()
        self.nav = self.terminal.pwd() + '$ '
        self.cmd = ''
        self.line = self.nav+self.cmd
        self.cached_line = []
        self.max_line_num = window_height//pyxel.FONT_HEIGHT-1

        pyxel.run(self.update, self.draw)

    def draw(self):
        pyxel.cls(0)

        # print lines on screen
        for i in range(len(self.cached_line)):
            pyxel.text(0, i*pyxel.FONT_HEIGHT, self.cached_line[i], 7)
        pyxel.text(0, len(self.cached_line)*pyxel.FONT_HEIGHT, self.line, 7)

    def update(self):
        # update texts that keyboard input
        # monitor the keyboard input
        if self.check_input() == 'enter':
            self.cached_line.append(self.line)

            # get the output from terminal
            curr_root, output = self.terminal.input(self.cmd)

            self.nav = curr_root + '$ '
            if len(output) > 0:
                self.cached_line.append(output)
            self.cmd = ''
        elif self.check_input() == 'back':
            if len(self.cmd) > 0:
                self.cmd = self.cmd[:-1]
        else:
            self.cmd += self.check_input()
        self.line = self.nav+self.cmd
        if len(self.cached_line) > self.max_line_num:
            exceed_num = len(self.cached_line) - self.max_line_num
            self.cached_line = self.cached_line[exceed_num:]

    def check_input(self):
        # check if the key is pressed
        for key in range(0, 255):
            if pyxel.btnp(key):
                if key == 13:
                    return 'enter'
                elif key == 8:
                    return 'back'
                return chr(key)
        return ''

WriteAndPrint()
