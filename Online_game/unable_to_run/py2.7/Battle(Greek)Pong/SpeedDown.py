import random, os, pygame, sys, math, time
from pygame.locals import *

class SpeedDown():
	def __init__(self):
		self.imageUp = pygame.image.load(os.path.join("images", "arrows", "speeddown.jpg"))
		self.arrowrect = self.imageUp.get_rect()
		self.x = 0
		self.y = 0

	def weaponDraw(self, game, x, y):
		self.arrowrect.center = x, y

		game.screen.blit(self.imageUp, self.arrowrect)


	def use(self, attacker, defender, ball):
		if defender.speed > 3:
			defender.speed -= 1

	def collide(self, player):
		if self.arrowrect.colliderect(player.rect):
			return True
		else:
			return False
