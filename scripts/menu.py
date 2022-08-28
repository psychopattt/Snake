import sys
from pygame import display, time, Rect, image, event as events, mouse, joystick
from pygame.constants import USEREVENT, QUIT, KEYDOWN, K_ESCAPE, JOYBUTTONDOWN, JOYDEVICEADDED
from pygame._sdl2.video import Window
from pygame_gui import UIManager, elements, UI_BUTTON_PRESSED
from constants import DEFAULT_GAME_WIDTH, DEFAULT_GAME_HEIGHT, DEFAULT_BLOCK_SIZE, DEFAULT_GAME_FRAMETIME, DEFAULT_NB_PLAYERS, DEFAULT_NB_SNACKS, SIZE_X, SIZE_Y, MENU_INPUT_FRAMETIME, MENU_FPS, MENU_BG
from game import Game

class Menu:
    def __init__(self):
        try: # PyInstaller stores data in sys._MEIPASS
            self.basePath = sys._MEIPASS
        except:
            self.basePath = "./data"

        display.set_caption("Snake - Menu")
        screen = display.set_mode((SIZE_X, SIZE_Y))
        display.set_icon(image.load(self.basePath + "/icon.jpg"))
        screen.set_alpha(None)
        
        self.window = Window.from_display_module()
        self.screenWidth, self.screenHeight = display.get_desktop_sizes()[0]
        uiManager = UIManager((SIZE_X, SIZE_Y), self.basePath + "/theme.json", False)
        
        clock = time.Clock()

        self.loopAround = False
        self.spawnWalls = False
        self.teleportHead = False
        self.increaseSpeed = False
        self.useAI = False

        self.CreateControls(uiManager)
        self.Run(screen, uiManager, clock)
        
    def CreateControls(self, uiManager):
        self.btnStart = elements.UIButton(relative_rect=Rect((SIZE_X / 2 - 100, 20), (200, 50)), text="Start Game", manager=uiManager)
        
        self.lblError = elements.UILabel(relative_rect=Rect((SIZE_X / 2 - 76, 80), (152, 20)), text="Invalid Parameters", manager=uiManager, visible=False)
        self.lblError.disable() # Apply different colors

        elements.UILabel(relative_rect=Rect((50, 110), (200, 20)), text="Width", manager=uiManager)
        self.txtWidth = elements.UITextEntryLine(relative_rect=Rect((50, 130), (200, 30)), manager=uiManager)
        self.txtWidth.set_text(str(DEFAULT_GAME_WIDTH))
        self.txtWidth.set_allowed_characters("numbers")

        elements.UILabel(relative_rect=Rect((SIZE_X - 250, 110), (200, 20)), text="Height", manager=uiManager)
        self.txtHeight = elements.UITextEntryLine(relative_rect=Rect((SIZE_X - 250, 130), (200, 30)), manager=uiManager)
        self.txtHeight.set_text(str(DEFAULT_GAME_HEIGHT))
        self.txtHeight.set_allowed_characters("numbers")

        elements.UILabel(relative_rect=Rect((50, 200), (200, 20)), text="Block Size", manager=uiManager)
        self.txtBlockSize = elements.UITextEntryLine(relative_rect=Rect((50, 220), (150, 30)), manager=uiManager)
        self.txtBlockSize.set_text(str(DEFAULT_BLOCK_SIZE))
        self.txtBlockSize.set_allowed_characters("numbers")
        self.btnFitBlockSize = elements.UIButton(relative_rect=Rect((200, 220), (50, 30)), text="Fit", manager=uiManager)

        elements.UILabel(relative_rect=Rect((SIZE_X - 250, 200), (200, 20)), text="Time Per Update (MS)", manager=uiManager)
        self.txtFPS = elements.UITextEntryLine(relative_rect=Rect((SIZE_X - 250, 220), (200, 30)), manager=uiManager)
        self.txtFPS.set_text(str(DEFAULT_GAME_FRAMETIME))
        self.txtFPS.set_allowed_characters("numbers")

        elements.UILabel(relative_rect=Rect((50, 290), (200, 20)), text="Number Of Snacks", manager=uiManager)
        self.txtNbSnacks = elements.UITextEntryLine(relative_rect=Rect((50, 310), (200, 30)), manager=uiManager)
        self.txtNbSnacks.set_text(str(DEFAULT_NB_SNACKS))
        self.txtNbSnacks.set_allowed_characters("numbers")

        elements.UILabel(relative_rect=Rect((SIZE_X - 250, 290), (200, 20)), text="Players (1 - 16)", manager=uiManager)
        self.txtNbPlayers = elements.UITextEntryLine(relative_rect=Rect((SIZE_X - 250, 310), (200, 30)), manager=uiManager)
        self.txtNbPlayers.set_text(str(DEFAULT_NB_PLAYERS))
        self.txtNbPlayers.set_allowed_characters("numbers")

        self.chkWalls = elements.UIButton(relative_rect=Rect((50, 380), (200, 50)), text="Spawn Walls - No", manager=uiManager)

        self.chkLoop = elements.UIButton(relative_rect=Rect((SIZE_X - 250, 380), (200, 50)), text="Loop Around - No", manager=uiManager)

        self.chkIncreaseSpeed = elements.UIButton(relative_rect=Rect((50, 470), (200, 50)), text="Increase Speed - No", manager=uiManager)

        self.chkTeleport = elements.UIButton(relative_rect=Rect((SIZE_X - 250, 470), (200, 50)), text="Teleport Head - No", manager=uiManager)

        self.chkUseAI = elements.UIButton(relative_rect=Rect((SIZE_X / 2 - 100, 560), (200, 50)), text="(Very Bad) AI - No", manager=uiManager)

    def CenterWindow(self):
        self.window.position = (
            (self.screenWidth / 2) - (SIZE_X / 2),
            (self.screenHeight / 2) - (SIZE_Y / 2)
        )

    def RestoreMenu(self):
        self.lblError.hide()
        display.set_caption("Snake - Menu")
        display.set_mode((SIZE_X, SIZE_Y)) # Restore screen size
        mouse.set_visible(True)
        self.CenterWindow()

    def StartGame(self):
        try:
            Game(
                int(self.txtWidth.get_text()), 
                int(self.txtHeight.get_text()), 
                int(self.txtBlockSize.get_text()), 
                int(self.txtFPS.get_text()), 
                int(self.txtNbSnacks.get_text()), 
                int(self.txtNbPlayers.get_text()), 
                self.loopAround, 
                self.spawnWalls, 
                self.teleportHead, 
                self.increaseSpeed, 
                self.useAI, 
                self.basePath, 
                self.window
            )
            self.RestoreMenu() # Called after the game loop has ended
        except:
            self.lblError.show()

    def GetNewControllers(self, controllers):
        for i in range(len(controllers), joystick.get_count()):
            controllers.append(joystick.Joystick(i))

        return controllers

    def Run(self, screen, uiManager, clock):
        menuRunning = True
        controllers = []

        while menuRunning:
            for event in events.get():
                if event.type == QUIT:
                    menuRunning = False

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        menuRunning = False

                elif event.type == JOYDEVICEADDED:
                    controllers = self.GetNewControllers(controllers)

                elif event.type == JOYBUTTONDOWN:
                    for controller in controllers:
                        if (controller.get_init() and controller.get_button(0)): # A
                            self.StartGame()
                    
                elif event.type == USEREVENT:
                    if event.user_type == UI_BUTTON_PRESSED:
                        match event.ui_element:
                            case self.btnStart:
                                self.StartGame()

                            case self.chkLoop:
                                self.loopAround = not self.loopAround
                                self.chkLoop.set_text("Loop Around - Yes") if self.loopAround else self.chkLoop.set_text("Loop Around - No")

                            case self.chkWalls:
                                self.spawnWalls = not self.spawnWalls
                                self.chkWalls.set_text("Spawn Walls - Yes") if self.spawnWalls else self.chkWalls.set_text("Spawn Walls - No")

                            case self.chkTeleport:
                                self.teleportHead = not self.teleportHead
                                self.chkTeleport.set_text("Teleport Head - Yes") if self.teleportHead else self.chkTeleport.set_text("Teleport Head - No")

                            case self.chkIncreaseSpeed:
                                self.increaseSpeed = not self.increaseSpeed
                                self.chkIncreaseSpeed.set_text("Increase Speed - Yes") if self.increaseSpeed else self.chkIncreaseSpeed.set_text("Increase Speed - No")

                            case self.chkUseAI:
                                self.useAI = not self.useAI
                                self.chkUseAI.set_text("(Very Bad) AI - Yes") if self.useAI else self.chkUseAI.set_text("(Very Bad) AI - No")

                            case self.btnFitBlockSize:
                                try:
                                    maxBlockWidth = int(self.screenWidth / (int(self.txtWidth.get_text()) + 1))
                                    maxBlockHeight = int(self.screenHeight / (int(self.txtHeight.get_text()) + 1))
                                    maxBlockSize = min(maxBlockWidth, maxBlockHeight)
                                    self.txtBlockSize.set_text(str(maxBlockSize))
                                    self.lblError.hide()
                                except:
                                    self.lblError.show()                                

                uiManager.process_events(event)
            
            uiManager.update(MENU_INPUT_FRAMETIME)

            screen.fill(MENU_BG)
            uiManager.draw_ui(screen)

            display.update()

            clock.tick(MENU_FPS)