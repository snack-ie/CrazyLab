import pygame
def hue(sprite, hue):
	newsprite = sprite.convert_alpha()
	color = pygame.Color(0)
	color.hsla = (hue, 100, 50, 100)
	colouredImage = pygame.Surface(newsprite.get_size())
	colouredImage.fill(color)
	
	huesprite = newsprite.copy()
	huesprite.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
	return huesprite