from pygame import draw
from random import randrange
from constants import WALL_COLOR

class Walls:
    def __init__(self, game, blockSize, blockGap):
        self.game = game
        self.blockSize = blockSize
        self.blockGap = blockGap
        self.wallPos = []

    def GetPositions(self):
        return self.wallPos

    def Place(self):
        availablePos = self.game.GetAvailablePos()
        availablePosCount = len(availablePos)

        if (availablePosCount > 0):
            selectedPos = list(availablePos[randrange(0, availablePosCount)])
            self.wallPos.append(selectedPos)
            self.game.RemoveAvailablePos(selectedPos)

    def Draw(self, screen):
        for wall in self.wallPos:
            # screen, color(r, g, b), rect(posX, posY, width, height)
            draw.rect(screen, WALL_COLOR, (wall[0] * self.blockSize + self.blockGap, wall[1] * self.blockSize + self.blockGap, self.blockSize - (self.blockGap * 2), self.blockSize - (self.blockGap * 2)))