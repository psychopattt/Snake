# Snake
A Snake game programmed in python. I made this to get used to pygame before the [GMTK game jam 2021](https://github.com/itsseraphii/Transgenesis).

## Features
- Customizeable settings
  - Board width and height as well as tile size
  - Time between snake movements
  - Number of snacks (pieces of food)
  - Number of players
- A few game modifiers
  - Spawn walls: each time a snake eats a piece of food, a wall is placed somewhere
  - Loop around: snakes can use the sides to wrap around the board
  - Increase speed: each time a snake eats a piece of food, the time between snake movements is reduced
  - Teleport head: each time a snake eats a piece of food, it's head is teleported somewhere on the board
- Local multiplayer
  - Up to 16 players
  - Support for Xbox and Playstation controllers

## Download
A Windows executable (exe) is available on [Itch.io](https://psycho-pattt.itch.io/snake)

## Project setup
To set up the project, you need `Python 3` as well as `pip`.

1. Install the required packages
```cmd
pip install -r requirements.txt
```

2. Run the project
```cmd
py scripts/main.py
```
