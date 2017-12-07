import random, os, pygame, sys, math, time
from pygame.locals import *

class Ball:
	# This function initializes properties of the ball.
	def __init__(self, width, height, screen, game):
		self.ballcolor = pygame.Color(255,0,0)
		self.image = pygame.image.load(os.path.join("images", "fireball.png"))
		self.rect = self.image.get_rect()
		self.rect.left = (width/2) - (self.rect.width/2)
		self.rect.top = (height/2) - (self.rect.height/2)
		direction = random.randint(1,2)
		if game.difficultylevel == 1:
			self.horizontalspeed = 10
		elif game.difficultylevel == 2:
			self.horizontalspeed = 13
		else:
			self.horizontalspeed = 16
		if direction == 2:
			self.horizontalspeed = -self.horizontalspeed
		self.verticalspeed = 0
		
	
	# This function moves the ball.	
	def moveBall(self, width, height, player1, player2, game):
		oldRect = self.rect
		
		newRect = self.rect.move([self.horizontalspeed,self.verticalspeed])
		
		if (newRect.right >= width):
			if game.hades[0] == True:
				if game.hades[2] == player2:
					game.hades[3] += 1
					
			if game.poseidon[0] == True:
				if game.poseidon[2] == player2:
					game.poseidon[3] += 1
							
			self.horizontalspeed = -self.horizontalspeed
			player2.health -= 10
		
		if (newRect.left <= 0):
			if game.hades[0] == True:
				if game.hades[2] == player1:
					game.hades[3] += 1
			
			if game.poseidon[0] == True:
				if game.poseidon[2] == player1:
					game.poseidon[3] += 1
							
			self.horizontalspeed = -self.horizontalspeed
			player1.health -= 10
			
		if (newRect.top < 0) or (newRect.bottom > height):
			self.verticalspeed = -self.verticalspeed
		
		
		if newRect.colliderect(player1.rect):
			if game.hades[0] == True:
				if game.hades[2] == player1:
					game.hades[3] += 1
					
			if game.poseidon[0] == True:
				if game.poseidon[2] == player1:
					game.poseidon[3] += 1
					
			self.changeDirection(newRect, oldRect, width, height, player1)
			
		elif newRect.colliderect(player2.rect):
			if game.hades[0] == True:
				if game.hades[2] == player2:
					game.hades[3] += 1
					
			if game.poseidon[0] == True:
				if game.poseidon[2] == player2:
					game.poseidon[3] += 1
					
			self.changeDirection(newRect, oldRect, width, height, player2)
		
		
		self.rect = newRect
		
	# This function changes the direction of the ball.	
	def changeDirection(self, newRect, oldRect, width, height, player):
		horizontalOffset = False
		if(oldRect.right <= player.rect.left) or (oldRect.left >= player.rect.right):
			horizontalOffset = True
			
		
		if horizontalOffset:
			self.horizontalspeed = -self.horizontalspeed
			self.changeVertical(player)
		
		else:
			self.verticalspeed = -self.verticalspeed
			
	# This function changes the vertical direction of the ball.	
	def changeVertical(self, player):
		if self.verticalspeed == 0:
			self.verticalspeed += 0.000001
		sign = 0
		maxDegrees = 70
		if self.rect.centery > player.rect.centery:
			sign = 1
		else:
			sign = -1
		
		totalDistance = (player.rect.height/2.0) + (self.rect.height/2.0)
		distanceMid = abs(self.rect.centery-player.rect.centery)
		
		
		degreeChange = maxDegrees*(distanceMid/totalDistance)
		radianChange = math.radians(degreeChange)
		
		maxRadianChange = math.radians(maxDegrees)
		maxAngle = math.tan(maxRadianChange)
		maxVerticalSpeed = (maxAngle * abs(self.horizontalspeed))*sign
		
		angle = math.tan(radianChange)
		
		self.verticalspeed = (angle * abs(self.horizontalspeed))*sign
		
		if abs(self.verticalspeed) > abs(maxVerticalSpeed):
			self.verticalspeed = maxVerticalSpeed