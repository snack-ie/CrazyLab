import pygame
pygame.init()

char        = pygame.image.load(       'assets/images/char.png')
floor       = pygame.image.load(      'assets/images/floor.png')
wall        = pygame.image.load(       'assets/images/wall.png')
portal      = pygame.image.load(     'assets/images/portal.png')
box         = pygame.image.load(        'assets/images/box.png')
door1       = pygame.image.load(      'assets/images/door1.png')
door2       = pygame.image.load(      'assets/images/door2.png')
on          = pygame.image.load(         'assets/images/on.png')
off         = pygame.image.load(        'assets/images/off.png')
door_color  = pygame.image.load( 'assets/images/door-color.png')
conveyor    = pygame.image.load(   'assets/images/conveyor.png')
teleporter  = pygame.image.load( 'assets/images/teleporter.png')
passthrough = pygame.image.load('assets/images/passthrough.png')
huechar     = pygame.image.load(    'assets/images/huechar.png')
charface    = pygame.image.load(   'assets/images/charface.png')
paintpass   = pygame.image.load(  'assets/images/paintpass.png')
painter     = pygame.image.load(    'assets/images/painter.png')

gameboy = pygame.font.Font('assets/fonts/gameboy.ttf', 50)

crazy = 'assets/music/crazy.wav'