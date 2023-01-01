import pygame
from settings import *

class Platform():
	def __init__(self, x, y, w, h):
	    self.rect = pygame.Rect(0, 0, w, h)
	    self.rect.x = x
	    self.rect.y = y
	    self.hits = False

	def update(self, surface, player):
		#pygame.draw.rect(surface, (255, 255, 255), self.rect)
		if not player.go_down:
			self.hits = self.rect.colliderect(player.rect)
		else:
			self.hits = False
		if self.hits:
			player.rect.bottom = self.rect.y
			player.vel_y = 0
			player.jump = False
			player.go_down = False