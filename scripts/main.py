from pygame import display, font, joystick, freetype, quit as pygameQuit
from menu import Menu

if __name__ == "__main__":
    display.init()
    font.init()
    freetype.init()
    joystick.init()
    
    menu = Menu() # Start game loop

    pygameQuit()