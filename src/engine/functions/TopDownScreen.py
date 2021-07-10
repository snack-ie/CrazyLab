from .. import game
import pygame
def topdownscreen(width, height, size):
	width = width * size
	height = height * size
	game.size = size
	return pygame.display.set_mode((width,height), 0, 32)