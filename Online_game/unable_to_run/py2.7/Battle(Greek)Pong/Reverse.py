import random, os, pygame, sys, math, time
from pygame.locals import *

class Reverse():
	def __init__(self):
		self.image = pygame.image.load(os.path.join("images", "doublearrow.jpg"))
		self.imagerect = self.image.get_rect()
	
	def weaponDraw(self, game, x, y):
		self.imagerect.center = x, y
		
		game.screen.blit(self.image, self.imagerect)
		
	def use(self, attacker, defender, ball):
		if attacker.isReversed == True:
			attacker.isReversed = False
		else:
			defender.isReversed = True
	
	def collide(self, player):
		if self.imagerect.colliderect(player.rect):
			return True
		else:
			return False