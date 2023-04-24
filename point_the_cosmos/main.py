import pyxel

class PointCosmos:
    def __init__(self):
        pyxel.init(160, 120, title="Point Cosmos")
        pyxel.mouse(False)

        pyxel.load("assets/pointer.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        # get mouse position
        mouse_x = pyxel.mouse_x
        mouse_y = pyxel.mouse_y

        # monitor the mouse button state
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            print("Left button pressed")

        # draw pointer
        pyxel.blt(mouse_x, mouse_y, 0, 0, 0, 16, 16, 0)

PointCosmos()
