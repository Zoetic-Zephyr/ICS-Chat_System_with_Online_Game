import random, os, pygame, sys, math, time
from pygame.locals import *

class HorizontalChange():
	def __init__(self):
		self.imageBall = pygame.image.load(os.path.join("images", "ball.jpg"))
		self.imageHarrow = pygame.image.load(os.path.join("images", "arrows", "harrow.jpg"))
		self.ballrect = self.imageBall.get_rect()
		self.arrowrect = self.imageHarrow.get_rect()
		self.x = 0
		self.y = 0

	def weaponDraw(self, game, x, y):
		self.ballrect.center = x, y
		self.arrowrect.center = x, y

		game.screen.blit(self.imageBall, self.ballrect)
		game.screen.blit(self.imageHarrow, self.arrowrect)


	def use(self, player1, player2, ball):
		ball.horizontalspeed = -ball.horizontalspeed
		
	def collide(self, player):
		if self.ballrect.colliderect(player.rect):
			return True
		else:
			return False