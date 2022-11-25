from pygame import draw
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP
from constants import HEAD_COLORS, DIRECTION_TOP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT
from colorsys import hsv_to_rgb
from random import randrange

class Snake:
    def __init__(self, game, id, width, height, gridWidth, gridHeight, startPos, blockSize, blockGap, multipleSnakes, loopAround, walls, teleportHead, increaseSpeed, useAI):
        self.game = game
        self.id = id
        self.width = width
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.height = height
        self.blockSize = blockSize
        self.blockGap = blockGap
        self.multipleSnakes = multipleSnakes
        self.loopAround = loopAround
        self.walls = walls
        self.teleportHead = teleportHead
        self.increaseSpeed = increaseSpeed
        self.usingAI = useAI

        self.gameOver = False

        if (teleportHead and not multipleSnakes):
            HEAD_COLORS[0] = (111, 17, 17)
        else:
            HEAD_COLORS[0] = (40, 111, 17)

        self.direction = K_RIGHT
        self.nextDirection = K_RIGHT
        
        self.segments = [startPos]
        self.SetHeadPositionUnavailable()
        self.nextSegmentPos = [] # If the snake grows, a segment will be added at that position

    def SetDirection(self, direction):
        self.nextDirection = direction

    def NotifyGameOver(self):
        self.gameOver = True

    def GetPositions(self):
        return self.segments

    def GetHeadPosition(self):
        return self.segments[0]

    def SetHeadPositionUnavailable(self):
        self.game.RemoveAvailablePos(self.GetHeadPosition())

    def SetNextSegmentPosAvailable(self):
        self.game.AddAvailablePos(self.nextSegmentPos)

    def Grow(self):
        self.segments.append(self.nextSegmentPos)

        if (self.walls is not None):
            self.walls.Place()

        if (self.increaseSpeed):
            self.game.IncreaseSpeed()

        self.game.CheckVictory() # Check if everything is snake and walls

    def EatAvailableSnack(self, snacks, snakeHeadsPositions):
        snacksPos = snacks.GetPositions()

        try:
            indexOfEatenSnack = snacksPos.index(self.GetHeadPosition())
            self.Grow()

            if (not self.gameOver):
                if (self.teleportHead):
                    availablePos = self.game.GetAvailablePos()
                    availablePosCount = len(availablePos)
                    
                    if (availablePosCount > 5):
                        self.game.AddAvailablePos(self.GetHeadPosition())
                        selectedPos = list(availablePos[randrange(0, availablePosCount)])
                        self.segments[0] = selectedPos
                        self.SetHeadPositionUnavailable()

                snacks.Place(indexOfEatenSnack)

        except ValueError: # No snack was eaten
            # If the tail is not replaced by a snake head
            if (self.nextSegmentPos not in snakeHeadsPositions):
                # No snack eaten, the position reserved for it's next segment is freed
                self.SetNextSegmentPosAvailable()

    def MoveBody(self):
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i] = list(self.segments[i - 1])

    def MoveHead(self):
        if (self.usingAI):
            if (self.nextDirection is not None):
                self.direction = self.nextDirection
                self.nextDirection = None
            else:
                if (self.segments[0][1] == 0): # Upper tile is border
                    self.direction = K_LEFT
                    self.nextDirection = K_DOWN
                elif (self.segments[0][0] + 1 >= self.gridWidth): # Right tile is border
                    self.direction = K_UP
                elif (self.segments[0][1] + 2 == self.gridHeight): # Down down tile is border
                    if (self.segments[0][0] == 0): # Left tile is border
                        self.nextDirection = K_RIGHT
                    else:
                        self.direction = K_LEFT
                        self.nextDirection = K_UP

        # Keep current direction if next direction is invalid
        elif (self.nextDirection in DIRECTION_TOP and self.direction not in DIRECTION_DOWN or 
            self.nextDirection in DIRECTION_RIGHT and self.direction not in DIRECTION_LEFT or 
            self.nextDirection in DIRECTION_DOWN and self.direction not in DIRECTION_TOP or 
            self.nextDirection in DIRECTION_LEFT and self.direction not in DIRECTION_RIGHT):
            self.direction = self.nextDirection

        if (self.direction in DIRECTION_TOP):
            self.segments[0][1] -= 1
        elif (self.direction in DIRECTION_RIGHT):
            self.segments[0][0] += 1
        elif (self.direction in DIRECTION_DOWN):
            self.segments[0][1] += 1
        elif (self.direction in DIRECTION_LEFT):
            self.segments[0][0] -= 1

        self.SetHeadPositionUnavailable()

    def CheckBorderCollide(self):
        if (self.loopAround):
            if (self.segments[0][0] < 0):
                self.segments[0][0] = self.gridWidth - 1
                self.SetHeadPositionUnavailable()
            elif (self.segments[0][0] >= self.gridWidth):
                self.segments[0][0] = 0
                self.SetHeadPositionUnavailable()
            elif (self.segments[0][1] < 0):
                self.segments[0][1] = self.gridHeight - 1
                self.SetHeadPositionUnavailable()
            elif (self.segments[0][1] >= self.gridHeight):
                self.segments[0][1] = 0
                self.SetHeadPositionUnavailable()

        elif (self.segments[0][0] < 0 or self.segments[0][0] >= self.gridWidth or self.segments[0][1] < 0 or self.segments[0][1] >= self.gridHeight):
            if (self.multipleSnakes):
                self.game.KillSnake(self, True)
            else:
                self.game.TriggerGameOver(False)

    def CheckBodyCollide(self):
        try:
            self.segments.index(self.GetHeadPosition(), 1)
            self.game.TriggerGameOver(False)
        except ValueError:
            pass # No collision

    def CheckWallCollide(self):
        if (self.GetHeadPosition() in self.walls.GetPositions()):
            if (self.multipleSnakes):
                self.game.KillSnake(self, True)
            else:
                self.game.TriggerGameOver(False)

    def Move(self):
        self.nextSegmentPos = list(self.segments[-1])
        self.MoveBody()
        self.MoveHead()
        self.CheckBorderCollide()
        
        if (not self.multipleSnakes):
            self.CheckBodyCollide()

        if (self.walls is not None):
            self.CheckWallCollide()

    def ComputeDrawPos(self, index):
        posY = self.blockGap
        gapX = self.blockGap * 2
        gapY = self.blockGap * 2
        posX = self.blockGap
        
        if (self.blockGap == 1):
            gapX = self.blockGap * 2
            if (self.segments[index - 1][1] + 1 == self.segments[index][1]): # Previous segment is over
                posY = -1
                gapY = 0
            elif (self.segments[index - 1][0] + 1 == self.segments[index][0]): # Previous segment is right
                posX = -1
                gapX = 0
            elif (self.segments[index - 1][1] - 1 == self.segments[index][1]): # Previous segment is under
                posY = 1
                gapY = 0
            elif (self.segments[index - 1][0] - 1 == self.segments[index][0]): # Previous segment is left
                posX = 1
                gapX = 0

        return [posX, posY, gapX, gapY]

    def DrawHead(self, screen):
        # screen, color(r, g, b), rect(posX, posY, width, height)
        draw.rect(screen, HEAD_COLORS[self.id], (self.segments[0][0] * self.blockSize + self.blockGap, self.segments[0][1] * self.blockSize + self.blockGap, self.blockSize - (self.blockGap * 2), self.blockSize - (self.blockGap * 2)))

    def DrawBodySegment(self, screen, color, posX, posY, segmentOffsets):
        draw.rect(screen, color, (posX * self.blockSize + segmentOffsets[0], posY * self.blockSize + segmentOffsets[1], self.blockSize - segmentOffsets[2], self.blockSize - segmentOffsets[3]))

    def DrawBody(self, screen):
        if (self.multipleSnakes):
            for i in range(1, len(self.segments)):
                segmentOffsets = self.ComputeDrawPos(i)
                self.DrawBodySegment(screen, HEAD_COLORS[self.id], self.segments[i][0], self.segments[i][1], segmentOffsets)
        else:
            for i in range(1, len(self.segments)):
                segmentOffsets = self.ComputeDrawPos(i)
                color = [channel * 255 for channel in hsv_to_rgb(i / 1440 + 0.291666, 0.85, 0.44)]
                self.DrawBodySegment(screen, color, self.segments[i][0], self.segments[i][1], segmentOffsets)

    def Draw(self, screen):
        self.DrawHead(screen)
        self.DrawBody(screen)