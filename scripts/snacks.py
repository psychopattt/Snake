from pygame import draw
from random import randrange
from constants import SNACK_COLOR

class Snacks:
    def __init__(self, game, blockSize, blockGap, nbSnacks):
        self.game = game
        self.blockSize = blockSize
        self.fullRadius = blockSize / 2
        self.radius = (blockSize - blockGap) / 2
        
        self.snackPos = [[-1, -1]] * nbSnacks
        self.PlaceAll()

    def PlaceAll(self):
        availablePos = self.game.GetAvailablePos()

        for i in range(len(self.snackPos)):
            availablePosCount = len(availablePos)

            if (availablePosCount > 0):
                selectedPos = list(availablePos[randrange(0, availablePosCount)])
                self.snackPos[i] = selectedPos
                availablePos.remove(selectedPos)
            else:
                break

    def Place(self, snackIndex):
        availablePos = self.game.GetAvailablePos()
        availablePosCount = len(availablePos)

        if (availablePosCount > 0):
            selectedPos = list(availablePos[randrange(0, availablePosCount)])
            self.snackPos[snackIndex] = selectedPos
            self.game.RemoveAvailablePos(selectedPos)
        else:
            self.snackPos.pop(snackIndex)

    def GetPositions(self):
        return self.snackPos

    def Draw(self, screen):
        for snack in self.snackPos:
            # screen, color(r, g, b), (centerX, centerY), radius
            draw.circle(screen, SNACK_COLOR, (snack[0] * self.blockSize + self.fullRadius, snack[1] * self.blockSize + self.fullRadius), self.radius)