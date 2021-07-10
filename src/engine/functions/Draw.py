from .. import game
import pygame
def draw(screen, sprite, pos):
	screen.blit(pygame.transform.scale(sprite, (game.size,game.size)), (pos[0] * game.size, pos[1] * game.size))