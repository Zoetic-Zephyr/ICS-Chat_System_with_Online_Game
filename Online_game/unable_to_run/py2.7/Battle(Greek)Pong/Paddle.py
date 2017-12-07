import random, os, pygame, sys, math, time
from pygame.locals import *

class Paddle:
	# This function initialized properties of the paddle.
	def __init__(self, imageName, player, height, margin, width, god):
		self.imageName = imageName
		self.image = pygame.image.load(os.path.join("images", "paddles", self.imageName))
		self.rect = self.image.get_rect()
		self.speed = 6
		self.player = player
		self.rect.centery = height/2
		self.health = 100
		self.superbar = 100
		self.score = 0
		self.weaponrack = [0,0,0]
		self.god = god
		self.isReversed = False
		
		if self.player == 1:
			self.rect.left = 0
		elif self.player == 2:
			self.rect.right = width

	def reinit(self, margin, height, width):
		margin = 50
		self.speed = 7
		self.rect.centery = height/2
		self.weaponrack = [0,0,0]
		
		if self.player == 1:
			self.rect.left = 0
		elif self.player == 2:
			self.rect.right = width
			
		self.health = 100
		self.superbar = 100
		self.isReversed = False
	
	# This function moves the paddle in the desired direction.
	def movePaddle(self, keys, height, width, ball, game):
		widthMargin = 0#50
		heightMargin = 0#20

		selfMove = self.rect
		leftLine = width/2 - (ball.rect.width/2) - 10
		rightLine = width/2 + (ball.rect.width/2) + 10
		
		if game.poseidon[0] == True:
			if game.poseidon[3] == 3:
				game.poseidon[0] = False
		
		if self.player == 1:
			self.moveVertical1(keys, height, width, ball, game)
			self.moveHorizontal1(keys, height, width, ball, game)
			
		else:
			self.moveVertical2(keys, height, width, ball, game)
			self.moveHorizontal2(keys, height, width, ball, game)
			
		if self.rect.colliderect(ball.rect):
			self.rect = selfMove
	
	def moveVertical1(self, keys, height, width, ball, game):
		selfMove = self.rect
		widthMargin = 0
		heightMargin = 0
		if (game.poseidon[0] == True) and (game.poseidon[2] == self):
			pass
		elif keys[pygame.K_s] and not(keys[pygame.K_w]) :
			if self.isReversed == False:
				self.rect = self.rect.move([0,self.speed])
			else:
				self.rect = self.rect.move([0,-self.speed])
		elif keys[pygame.K_w] and not(keys[pygame.K_s]):
			if self.isReversed == False:
				self.rect = self.rect.move([0,-self.speed])
			else:
				self.rect = self.rect.move([0,self.speed])
		
		if (self.rect.top < 0+heightMargin)or(self.rect.bottom > height-heightMargin):
			self.rect = selfMove
		
		selfMove = self.rect
		
	def moveHorizontal1(self, keys, height, width, ball, game):
		selfMove = self.rect
		leftLine = width/2 - (ball.rect.width/2) - 10
		rightLine = width/2 + (ball.rect.width/2) + 10
		widthMargin = 0
		heightMargin = 0
		if keys[pygame.K_a] and not(keys[pygame.K_d]):
			self.rect = self.rect.move([-self.speed,0])
		elif keys[pygame.K_d] and not(keys[pygame.K_a]):
			self.rect = self.rect.move([self.speed,0])
	
		if (self.rect.left<widthMargin) or(self.rect.right > leftLine):
			self.rect = selfMove
			
	def moveVertical2(self, keys, height, width, ball, game):
		widthMargin = 0#50
		heightMargin = 0#20
		selfMove = self.rect
		if (game.poseidon[0] == True) and (game.poseidon[2] == self):
			pass
		elif keys[pygame.K_DOWN] and not(keys[pygame.K_UP]) :
			if self.isReversed == False:
				self.rect = self.rect.move([0,self.speed])
			else:
				self.rect = self.rect.move([0,-self.speed])
		elif keys[pygame.K_UP] and not(keys[pygame.K_DOWN]):
			if self.isReversed == False:
				self.rect = self.rect.move([0,-self.speed])
			else:
				self.rect = self.rect.move([0, self.speed])
		
		if (self.rect.top < 0+heightMargin)or(self.rect.bottom > height-heightMargin):
			self.rect = selfMove
		
		selfMove = self.rect
		
	def moveHorizontal2(self, keys, height, width, ball, game):
		widthMargin = 0#50
		heightMargin = 0#20
		selfMove = self.rect
		leftLine = width/2 - (ball.rect.width/2) - 10
		rightLine = width/2 + (ball.rect.width/2) + 10
		if keys[pygame.K_LEFT] and not(keys[pygame.K_RIGHT]) :
			self.rect = self.rect.move([-self.speed,0])
		elif keys[pygame.K_RIGHT] and not(keys[pygame.K_LEFT]):
			self.rect = self.rect.move([self.speed,0])
	
		if (self.rect.right>width-widthMargin)or(self.rect.left<rightLine):
			self.rect = selfMove
	
	def useWeaponRack(self, keys, ball, player, game):
		if self.player == 1:
			self.weaponRack1(keys, ball, player, game)
		else:
			self.weaponRack2(keys, ball, player, game)
		
	def weaponRack1(self, keys, ball, player, game):
		if keys[pygame.K_c]:
			if self.weaponrack[0] != 0:
				self.weaponrack[0].use(self, player, ball)
				self.weaponrack[0] = 0

		if keys[pygame.K_v]:
			if self.weaponrack[1] != 0:
				self.weaponrack[1].use(self, player, ball)
				self.weaponrack[1] = 0
			
		if keys[pygame.K_b]:
			if self.weaponrack[2] != 0:
				self.weaponrack[2].use(self, player, ball)
				self.weaponrack[2] = 0
		
		if keys[pygame.K_x]:
			if self.superbar == 100:
				self.superbar = 0
				if self.god == "Hades":
					game.hades = [True, self, player, 0]
				if self.god == "Zeus":
					game.zeus = [True, self, player, self.rect.right, self.rect.centery]
				if self.god == "Poseidon":
					game.poseidon = [True, self, player, 0]
	
	def weaponRack2(self, keys, ball, player, game):
		if keys[pygame.K_i]:
			if self.weaponrack[0] != 0:
				self.weaponrack[0].use(self, player, ball)
				self.weaponrack[0] = 0

		if keys[pygame.K_o]:
			if self.weaponrack[1] != 0:
				self.weaponrack[1].use(self, player, ball)
				self.weaponrack[1] = 0
			
		if keys[pygame.K_p]:
			if self.weaponrack[2] != 0:
				self.weaponrack[2].use(self, player, ball)
				self.weaponrack[2] = 0
				
		if keys[pygame.K_u]:
			if self.superbar == 100:
				self.superbar = 0
				if self.god == "Hades":
					game.hades = [True, self, player, 0]
				if self.god == "Zeus":
					game.zeus = [True, self, player, self.rect.left, self.rect.centery]
				if self.god == "Poseidon":
					game.poseidon = [True, self, player, 0]
					
	# This function returns the color that the paddle is.	
	def checkColor(self):
		red = (255,0,0)
		yellow = (255,255,0)
		blue = (0,0,255)

		if self.imageName == "yellowlightning.jpg":
			return yellow
		elif self.imageName == "bluelightning.jpg":
			return blue
		else:
			return red