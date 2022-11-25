from pygame import display, time, font, event as events, joystick, mouse
from pygame.constants import QUIT, JOYBUTTONDOWN, KEYDOWN, K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, K_p
from constants import BG_COLOR, TEXT_COLOR, SNAKE_DIRECTION_INPUTS, GAME_INPUT_FPS
from math import floor
from background import Background
from snake import Snake
from snacks import Snacks
from walls import Walls

class Game:
    def __init__(self, gridWidth, gridHeight, blockSize, frametime, nbSnacks, nbPlayers, loopAround, spawnWalls, teleportHead, increaseSpeed, useAI, basePath, window):
        self.frametime = frametime
        self.usingAI = useAI
        self.window = window

        if (useAI):
            nbPlayers = 1
            spawnWalls = False
            teleportHead = False
            gridWidth = gridWidth if (gridWidth > 3) else 4
            gridWidth = gridWidth if (gridWidth % 2 == 0) else gridWidth + 1
        else:
            if (nbPlayers < 1):
                nbPlayers = 1
            elif (nbPlayers > 16):
                nbPlayers = 16

        if (nbPlayers > 1):
            self.gridWidth = gridWidth if (gridWidth > 9) else 10
            self.gridHeight = gridHeight if (gridHeight > 9) else 10
        else:
            self.gridWidth = gridWidth if (gridWidth > 2) else 3
            self.gridHeight = gridHeight if (gridHeight > 2) else 3

        if (blockSize < 1):
            blockSize = 1

        self.width = self.gridWidth * blockSize
        self.height = self.gridHeight * blockSize

        self.gameOver = False
        self.InitAvailablePos()

        blockGap = 0 if (blockSize < 8) else 1
        maxNbSnacks = self.gridWidth * self.gridHeight - 1

        if (nbSnacks > maxNbSnacks):
            nbSnacks = maxNbSnacks
        elif (nbSnacks < 1):
            nbSnacks = 1

        if (spawnWalls):
            self.walls = Walls(self, blockSize, blockGap)
        else:
            self.walls = None

        if (increaseSpeed):
            self.minFrametime = round(frametime / 8)

        self.controllers = []

        for i in range(joystick.get_count()): # Register new controllers
            self.controllers.append(joystick.Joystick(i))

        mouse.set_visible(False)
        display.set_caption("Snake - Game")
        screen = display.set_mode((self.width, self.height))
        screen.set_alpha(None)
        clock = time.Clock()
        self.CenterWindow()

        self.fontName = basePath + "/FreeSansBold.ttf"
        self.fontH1 = font.Font(self.fontName, 55)

        self.nbSnakes = nbPlayers
        self.snakes = []
        self.aliveSnakes = []

        if (self.nbSnakes == 1):
            self.aliveSnakes.append(0)
            snakeStartPos = [floor(self.gridWidth / 2) - 1, floor(self.gridHeight / 2)] # Head starts centered
            self.snakes.append(Snake(self, 0, self.width, self.height, self.gridWidth, self.gridHeight, snakeStartPos, blockSize, blockGap, False, loopAround, self.walls, teleportHead, increaseSpeed, useAI))
        else:
            incrementX = floor(self.gridWidth / 4)
            incrementY = floor(self.gridHeight / 4)

            for i in range(self.nbSnakes):
                self.aliveSnakes.append(i)
                snakeStartPos = [floor(i / 4) * incrementX, i % 4 * incrementY + 1]
                self.snakes.append(Snake(self, i, self.width, self.height, self.gridWidth, self.gridHeight, snakeStartPos, blockSize, blockGap, True, loopAround, self.walls, teleportHead, increaseSpeed, useAI))

        snacks = Snacks(self, blockSize, blockGap, nbSnacks)
        self.background = Background(self.gridWidth, self.gridHeight, blockSize)

        self.Run(screen, clock, self.snakes, snacks, self.walls)

    def CenterWindow(self):
        screenWidth, screenHeight = display.get_desktop_sizes()[0]
        windowWidth, windowHeight = display.get_window_size()

        self.window.position = (
            (screenWidth / 2) - (windowWidth / 2),
            (screenHeight / 2) - (windowHeight / 2)
        )

    def CheckVictory(self): # Everything is snake and/or walls
        nbOccupiedPos = 0
        
        for i in range(self.nbSnakes):
            nbOccupiedPos += len(self.snakes[i].GetPositions())

        if (self.walls is not None):
            nbOccupiedPos += len(self.walls.GetPositions())

        if (nbOccupiedPos == self.gridWidth * self.gridHeight):
            self.TriggerGameOver(True)
            return True
        
        return False

    def TriggerGameOver(self, victory):
        for i in range(self.nbSnakes):
            self.snakes[i].NotifyGameOver()

        self.victory = victory
        self.gameOver = True

    def ShowGameOver(self, screen, snakes):
        windowSize = display.get_window_size()

        if (windowSize[0] < 290 or windowSize[1] < 170):
            self.width = 300
            self.height = 200
            display.set_mode((self.width, self.height))
            screen.fill(BG_COLOR)

        if (self.victory):
            text = self.fontH1.render("Victory!", True, TEXT_COLOR, BG_COLOR)
            textRect = text.get_rect(center = (self.width / 2, self.height / 2 - 30))
            screen.blit(text, textRect)
        else:
            text = self.fontH1.render("Game Over", True, TEXT_COLOR, BG_COLOR)
            textRect = text.get_rect(center = (self.width / 2, self.height / 2 - 30))
            screen.blit(text, textRect)

        score = 0
        
        for i in range(self.nbSnakes):
            score += len(snakes[i].GetPositions())

        text = font.Font(self.fontName, 45).render("Score: " + str(score), True, TEXT_COLOR, BG_COLOR)
        textRect = text.get_rect(center = (self.width / 2, self.height / 2 + 30))
        screen.blit(text, textRect)

        if (self.width > 349):
            screen.blit(font.Font(self.fontName, 20).render("Press ESC to go back to the menu", True, TEXT_COLOR, BG_COLOR), (7, self.height - 30))
        else:
            screen.blit(font.Font(self.fontName, 20).render("Press ESC", True, TEXT_COLOR, BG_COLOR), (7, self.height - 30))

        display.set_caption("Snake - Game Over")
        display.update()
        self.paused = True

    def InitAvailablePos(self):
        self.availablePos = [[i, j] for i in range(self.gridWidth) for j in range(self.gridHeight)]

    def RemoveAvailablePos(self, pos):
        if (pos in self.availablePos):
            self.availablePos.remove(pos)

    def AddAvailablePos(self, pos):
        if (pos not in self.availablePos):
            self.availablePos.append(pos)

    def GetAvailablePos(self):
        return self.availablePos

    def CheckSnakesCollisions(self):
        checkedPos = []
        deadPos = []

        for i in range(self.nbSnakes):
            currentSnake = self.snakes[i]

            for pos in currentSnake.GetPositions():
                if pos in checkedPos:
                    deadPos.append(pos)
                    self.KillSnake(currentSnake, False)
                else:
                    checkedPos.append(pos)

        for i in range(len(self.aliveSnakes)):
            if (i < len(self.aliveSnakes)):
                currentSnake = self.snakes[self.aliveSnakes[i]]

                for pos in currentSnake.GetPositions():
                    if (pos in deadPos):
                        self.KillSnake(currentSnake, False)
                        break

    def KillSnake(self, snake, objectCollision):
        if (snake.id in self.aliveSnakes):
            self.aliveSnakes.remove(snake.id)

            if (objectCollision):
                snake.SetNextSegmentPosAvailable()
            
            if (len(self.aliveSnakes) == 0):
                self.TriggerGameOver(False)

    def MakeSnakesEat(self, snakes, snacks):
        snakeHeadsPositions = []

        for i in range(len(self.aliveSnakes)):
            snakeHeadsPositions.append(snakes[self.aliveSnakes[i]].GetHeadPosition())

        for i in range(len(self.aliveSnakes)):
            snakes[self.aliveSnakes[i]].EatAvailableSnack(snacks, snakeHeadsPositions)

    def IncreaseSpeed(self): # Goes up to 8x faster
        self.frametime = max(self.minFrametime, self.frametime - max(1, round(self.frametime / 50)))
        
    def Run(self, screen, clock, snakes, snacks, walls):
        self.playing = True
        self.paused = False
        lastGameUpdate = 0

        while self.playing:
            for event in events.get():
                if event.type == QUIT:
                    self.playing = False

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                       self.playing = False

                    elif event.key == K_p and not self.gameOver:
                        self.paused = not self.paused

                        if (self.paused):
                            screen.blit(self.fontH1.render("Pause", True, TEXT_COLOR, BG_COLOR), (10, 0))
                        else:
                            screen.blit(self.fontH1.render("Pause", True, BG_COLOR, BG_COLOR), (10, 0))
                        
                        display.update()

                    elif event.key in SNAKE_DIRECTION_INPUTS and not self.paused and not self.usingAI:
                        snakes[0].SetDirection(event.key)

                elif event.type == JOYBUTTONDOWN and not self.paused and not self.usingAI:
                    for i in range(len(self.controllers)):
                        if (self.controllers[i].get_init() and i < self.nbSnakes):
                            if (self.controllers[i].get_button(0)): # A
                                snakes[i].SetDirection(K_DOWN)
                            elif (self.controllers[i].get_button(1)): # B
                                snakes[i].SetDirection(K_RIGHT)
                            elif (self.controllers[i].get_button(2)): # X
                                snakes[i].SetDirection(K_LEFT)
                            elif (self.controllers[i].get_button(3)): # Y
                                snakes[i].SetDirection(K_UP)

                elif (event.type == JOYBUTTONDOWN and self.gameOver and self.paused and
                      time.get_ticks() >= lastGameUpdate + 1000): # Wait 1 second
                    for controller in self.controllers:
                        if (controller.get_init() and controller.get_button(1)): # (1) == B
                            self.playing = False

            if (not self.paused and time.get_ticks() >= lastGameUpdate + self.frametime): # Game updated at specified fps
                lastGameUpdate = time.get_ticks()

                self.background.Draw(screen)
                
                for i in range(len(self.aliveSnakes)):
                    if (i < len(self.aliveSnakes)): # Dead snakes might change the max index
                        snakes[self.aliveSnakes[i]].Move()

                self.MakeSnakesEat(snakes, snacks)

                if (self.nbSnakes > 1):
                    self.CheckSnakesCollisions()
                
                snacks.Draw(screen)

                for i in range(self.nbSnakes):
                    snakes[i].Draw(screen)

                if (walls is not None):
                    walls.Draw(screen)

                display.update()

            if (self.gameOver and not self.paused):
                self.ShowGameOver(screen, snakes)

            clock.tick(GAME_INPUT_FPS) # Game inputs checked at 200fps