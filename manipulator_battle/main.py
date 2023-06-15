import pyxel

class Main:
    def __init__(self):
        self.length = 160
        self.height = 120
        pyxel.init(self.length, self.height, title="manipulator battle")
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)

Main()
