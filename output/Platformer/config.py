# import for extras
import pygame as p
import random as r
from os import path
# game options/settings
TITLE      = 'Platformer!'
WIDTH      = 480
HEIGHT     = 600
FPS        = 60
FONT       = 'ariel'
SCORE_DEF  = 0
SURPMODE   = False
# define colors
WHITE      = (255, 255, 255)
BLACK      = (0, 0, 0)
RED        = (255, 0, 0)
GREEN      = (0, 255, 0)
BLUE       = (0, 0, 255)
YELLOW     = (255, 255, 0)
# define extras
vec        = p.math.Vector2
PLAYER_ACC = 0.5
PLAYER_FRI = 0.09
PLAYER_GRA = 0.8
player_jmp = 23
START_Y    = 480
START_X    = WIDTH/2
# Define Init List of Platforms
PLATFORM_LIST = [
                 (0, HEIGHT - 40, WIDTH, 40),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 25),
                 (125, HEIGHT - 350, 100, 25),
                 (350, 200, 100, 25),
                 (175, 100, 50, 25)
                ]
# Create Image and Sound Directories
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
p.init()
p.mixer.init()
