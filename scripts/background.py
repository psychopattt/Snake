from pygame import draw
from constants import BG_COLOR, BG_COLOR_LIGHT

class Background:
    def __init__(self, gridWidth, gridHeight, blockSize):
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.blockSize = blockSize

    def DrawSquare(self, screen, posX, posY, color):
        # screen, color(r, g, b), rect(posX, posY, width, height)
        draw.rect(screen, color, (posX * self.blockSize, posY * self.blockSize, self.blockSize, self.blockSize))

    def Draw(self, screen):
        for y in range(self.gridHeight):
            if (y % 2 == 0):
                for x in range(self.gridWidth):
                    if (x % 2 == 0):
                        self.DrawSquare(screen, x, y, BG_COLOR)
                    else:
                        self.DrawSquare(screen, x, y, BG_COLOR_LIGHT)
            else:
                for x in range(self.gridWidth):
                    if (x % 2 == 0):
                        self.DrawSquare(screen, x, y, BG_COLOR_LIGHT)
                    else:
                        self.DrawSquare(screen, x, y, BG_COLOR)