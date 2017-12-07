import random, os, sys, math, time, pygame
from pygame.locals import *
from Paddle import Paddle
from Ball import Ball
from Reverse import Reverse
from SpeedDown import SpeedDown
from SpeedUp import SpeedUp
from VerticalChange import VerticalChange
from HorizontalChange import HorizontalChange

class Game:
	# This function initializes properties of the game.
	def __init__(self):
		self.menu = True
		self.play = False
		self.width = 1250
		self.height = 750
		self.gameHeight = 675
		self.state = True
		self.screen = pygame.display.set_mode([self.width, self.height])
		self.difficultylevel = 1
		self.weaponsinit()
		self.superweaponsinit()
		
		self.superx1 = 0
		self.superx2 = 0
		self.supery = 0
		
		self.num1 = random.randint(0,4)
		self.num2 = random.randint(0,4)
		
		self.options()
	
	def weaponsinit(self):
		self.weaponsinit1()
		self.weaponsinit2()
		
	def weaponsinit1(self):
		vchange1 = VerticalChange()
		hchange1 = HorizontalChange()
		sup1 = SpeedUp()
		sdown1 = SpeedDown()
		reverse1 =  Reverse()
		self.weaponlist1 = [vchange1, hchange1, sup1, sdown1, reverse1]
		self.collide1 = False
		self.collidegreen1 = False
	
	def weaponsinit2(self):
		vchange2 = VerticalChange()
		hchange2 = HorizontalChange()
		sup2 = SpeedUp()
		sdown2 = SpeedDown()
		reverse2 = Reverse()
		self.weaponlist2 = [vchange2, hchange2, sup2, sdown2, reverse2]
		self.collide2 = False
		self.collidegreen2 = False
	
	def superweaponsinit(self):
		self.hades = [False, None, None, 0]
		self.zeus = [False, None, None, 0, 0]
		self.poseidon = [False, None, None, 0]
		
	# This function chooses the state of the game.	
	def options(self):
		pygame.init()
		while self.state == True:
			if self.menu == True:
				self.gameMenu()
			while self.play == True:
				self.run()
	
		
	def gameMenu(self):
		pygame.init()
		inumber = 2
		while self.menu == True:
			for event in pygame.event.get():
				if (event.type == QUIT):
					self.menu = False
					self.state = False
					self.play = False
			
			
			pygame.event.pump()
			mouse = pygame.mouse.get_pressed()
			doneChoice = False
			if mouse[0]:
				doneChoice = self.choice(mouse)
			if doneChoice:
				return
			
			self.menuDraw(inumber)
			inumber += 1
	
			
	def choice(self, mouse):
		mousepos = pygame.mouse.get_pos()
		if self.playrect.collidepoint(mousepos):
			return self.playerchoice()
		
		if self.instructionsrect.collidepoint(mousepos):
			self.instruction()
			return False
		
		if self.difficultyrect.collidepoint(mousepos):
			self.chooseDifficulty()
		
		if self.quitrect.collidepoint(mousepos):
			self.menu = False
			self.state = False
			self.play = False
	
	def chooseDifficulty(self):
		diff = True
		arrow = pygame.image.load(os.path.join("images", "pages", "pagearrowleft.jpg"))
		arrowrect = arrow.get_rect()
		arrowrect.center = 50, 50
		while diff:
			for event in pygame.event.get():
				if (event.type == QUIT):
					self.menu = False
					self.state = False
					self.play = False
					diff = False
				elif (event.type == pygame.MOUSEBUTTONDOWN):
					mousepos = pygame.mouse.get_pos()
					if arrowrect.collidepoint(mousepos):
						diff = False
						return False
					elif leftrect.collidepoint(mousepos):
						if self.difficultylevel > 1:
							self.difficultylevel -= 1
					elif rightrect.collidepoint(mousepos):
						if self.difficultylevel < 3:
							self.difficultylevel += 1
			
			rightrect, leftrect = self.drawDifficultyPage()
			self.screen.blit(arrow, arrowrect)
			pygame.display.update()
		
	def drawDifficultyPage(self):
		black = (0,0,0)
		self.screen.fill(black)
		rightrect, leftrect = self.drawDiffArrows()
		self.drawDiffTitle()
		self.drawNumber()
		return rightrect, leftrect
		
	def drawNumber(self):
		imageName = str(self.difficultylevel) + ".jpg"
		image = pygame.image.load(os.path.join("images", imageName))
		rect = image.get_rect()
		rect.center = self.width/2.0, self.height/2.0
		self.screen.blit(image, rect)
	
	def drawDiffTitle(self):
		diffimage = pygame.image.load(os.path.join("images", "diff.jpg"))
		diffrect = diffimage.get_rect()
		diffrect.center = self.width/2.0, 150
		self.screen.blit(diffimage, diffrect)
		
	def drawDiffArrows(self):
		right = pygame.image.load(os.path.join("images", "diffarrowright.jpg"))
		rightrect = right.get_rect()
		left = pygame.image.load(os.path.join("images", "diffarrowleft.jpg"))
		leftrect = left.get_rect()
		rightrect.center = self.width * 3.0/4, self.height/2.0
		leftrect.center = self.width * 1.0/4, self.height/2.0
		self.screen.blit(right, rightrect)
		self.screen.blit(left, leftrect)
		
		return rightrect, leftrect
	
	# This function displays the choice of paddles for the player.
	def playerchoice(self):
		playBool = True
		top = 2.0/10 * self.height
		
		arrow = pygame.image.load(os.path.join("images", "pages", "pagearrowleft.jpg"))
		arrowrect = arrow.get_rect()
		arrowrect.center = 50, 50
		
		image = pygame.image.load(os.path.join("images", "presst.jpg"))
		rectt = image.get_rect()
		rectt.left = 50
		rectt.top = self.height - 75
		
		
		player1img = pygame.image.load(os.path.join("images", "player1.jpg"))
		player2img = pygame.image.load(os.path.join("images", "player2.jpg"))
		
		player1imgrect = player1img.get_rect()
		player2imgrect = player2img.get_rect()
		
		player1imgrect.center = self.width/2 , 1.0/10 * self.height
		player2imgrect.center = self.width/2, 1.0/10 * self.height
		
		hades = pygame.image.load(os.path.join("images", "godimages", "hades.jpg"))
		hadesrect = hades.get_rect()
		hadesrect.centerx = self.width * 1.0/4
		hadesrect.top = top
		
		poseidon = pygame.image.load(os.path.join("images", "godimages", "poseidon.jpg"))
		poseidonrect = poseidon.get_rect()
		poseidonrect.centerx = self.width * 2.0/4
		poseidonrect.top = top
		
		zeus = pygame.image.load(os.path.join("images", "godimages", "zeus.jpg"))
		zeusrect = zeus.get_rect()
		zeusrect.centerx = self.width * 3.0/4
		zeusrect.top = top
		
		player = 1
		black = (0,0,0)
		
		while playBool:
			for event in pygame.event.get():
				if (event.type == QUIT):
					self.menu = False
					self.state = False
					self.play = False
					playBool = False
				
				elif (event.type == pygame.MOUSEBUTTONDOWN):
					mousepos = pygame.mouse.get_pos()
					if arrowrect.collidepoint(mousepos):
						playBool = False
						return False
						
					chose = self.initChoice(player, hadesrect,poseidonrect,zeusrect, arrowrect)
					if chose:
						player += 1
			
			
			#if playBool == False:
			#	print "i art here"
			#	return False
			
			
			if player == 3:
				self.play = True
				playBool = False
				return True
				
			self.screen.fill(black)
			self.screen.blit(arrow, arrowrect)
			self.screen.blit(hades, hadesrect)
			self.screen.blit(poseidon, poseidonrect)
			self.screen.blit(zeus, zeusrect)
			self.screen.blit(image, rectt)
			if player == 1:
				self.screen.blit(player1img, player1imgrect)
			else:
				self.screen.blit(player2img, player2imgrect)
				
			pygame.display.update()
	
	# This function initializes the paddles
	
	def initChoice(self, player, hadesrect, poseidonrect, zeusrect, arrowrect):
		mousepos = pygame.mouse.get_pos()
		margin = 50
		
			
		if hadesrect.collidepoint(mousepos):
			if player == 1:
				self.player1 = Paddle("redlightning.jpg", 1, self.gameHeight, margin, self.width, "Hades")
				return True
			elif self.player1.god != "Hades":
				self.player2 = Paddle("redlightning.jpg", 2, self.gameHeight, margin, self.width, "Hades")
				return True
		if poseidonrect.collidepoint(mousepos):
			if player == 1:
				self.player1 = Paddle("bluelightning.jpg", 1, self.gameHeight, margin, self.width, "Poseidon")
				return True
			elif self.player1.god != "Poseidon":
				self.player2 = Paddle("bluelightning.jpg", 2, self.gameHeight, margin, self.width, "Poseidon")
				return True
		if zeusrect.collidepoint(mousepos):
			if player == 1:
				self.player1 = Paddle("yellowlightning.jpg", 1, self.gameHeight, margin, self.width, "Zeus")
				return True
			elif self.player1.god != "Zeus":
				self.player2 = Paddle("yellowlightning.jpg", 2, self.gameHeight, margin, self.width, "Zeus")
				return True
		return False
	
	def instruction(self):
		page = 1
		pygame.display.set_caption("Greek Pong")
		black = (0,0,0)
		instruct = True
		while instruct:
			self.screen.fill(black)
			rightrect, leftrect = self.drawArrows(page)
			for event in pygame.event.get():
				if (event.type == QUIT):
					self.menu = False
					self.state = False
					self.play = False
					instruct = False
				
				elif (event.type == pygame.MOUSEBUTTONDOWN):
					mousepos = pygame.mouse.get_pos()
					if rightrect.collidepoint(mousepos):
						if page < 4:
							page += 1
						else:
						    page = 1
					if leftrect.collidepoint(mousepos):
						page -= 1
						if page == 0:
							instruct = False
			
			if page == 1:
				self.drawPage1()
			elif page == 2:
				self.drawPage2()
			elif page == 3:
				self.drawPage3()
			elif page == 4:
				self.drawPage4()
			pygame.display.update()
			
	def drawArrows(self, page):
		right = pygame.image.load(os.path.join("images", "pages", "pagearrowright.jpg"))
		rightrect = right.get_rect()
		left = pygame.image.load(os.path.join("images", "pages", "pagearrowleft.jpg"))
		leftrect = left.get_rect()
		
		leftrect.center = 50, self.height - 50
		rightrect.center = self.width - 50, self.height - 50
		
		#if (page == 1) or (page == 2) or (page == 3):
		self.screen.blit(left, leftrect)
		self.screen.blit(right, rightrect)
		
		# else:
		#         self.screen.blit(left, leftrect)
		
		return rightrect, leftrect
		
	def drawPage1(self):
		self.pcontrols()
		height = 150
		
		for i in xrange(8):
			centerx = 225
			inum = i + 1
			self.drawP1(inum, centerx, height)
			centerx = self.width/2.0
			self.drawNames(inum, centerx, height)
			centerx = self.width - 225
			self.drawP2(inum, centerx, height)
			height += 75
	
	def drawP1(self, inum, centerx, height):
		p1keyname = "p1" + str(inum) + ".jpg"
		p1key = pygame.image.load(os.path.join("images", "page1", p1keyname))
		p1keyrect = p1key.get_rect()
		p1keyrect.center = centerx, height
		self.screen.blit(p1key, p1keyrect)
	
	def drawNames(self, inum, centerx, height):
		keyname = "name" + str(inum) + ".jpg"
		key = pygame.image.load(os.path.join("images", "page1", keyname))
		keyrect = key.get_rect()
		keyrect.center = centerx, height
		self.screen.blit(key, keyrect)	
	
	def drawP2(self, inum, centerx, height):
		p2keyname = "p2" + str(inum) + ".jpg"
		p2key = pygame.image.load(os.path.join("images", "page1", p2keyname))
		p2keyrect = p2key.get_rect()
		p2keyrect.center = centerx, height
		self.screen.blit(p2key, p2keyrect)
			
	def pcontrols(self):
		p1 = pygame.image.load(os.path.join("images", "page1", "p1controls.jpg"))
		p1rect = p1.get_rect()
		p2 = pygame.image.load(os.path.join("images", "page1", "p2controls.jpg"))
		p2rect = p2.get_rect()
		p1rect.left = 50
		p1rect.top = 50
		p2rect.right = self.width - 50
		p2rect.top = 50
		
		self.screen.blit(p1, p1rect)
		self.screen.blit(p2, p2rect)
		
	def drawPage2(self):
		self.drawPage2Title()
		self.drawDescriptions()
		self.drawWeaponImages()
	
	def drawPage2Title(self):
		title = pygame.image.load(os.path.join("images","page2","weapons.jpg"))
		titlerect = title.get_rect()
		titlerect.top = 10
		titlerect.centerx = self.width/2.0
		self.screen.blit(title, titlerect)
	
	def drawWeaponImages(self):
		height = 110
		centerx = 150
		for i in xrange(len(self.weaponlist1)):
			self.weaponlist1[i].weaponDraw(self, centerx, height)
			height += 100
		
		greensphere = pygame.image.load(os.path.join("images", "green.jpg"))
		greenrect = greensphere.get_rect()
		greenrect.center = centerx, height
		self.screen.blit(greensphere, greenrect)
		
	def drawDescriptions(self):
		height = 80
		left = self.width * 1.0/4
		for i in xrange(6):
			inum = i + 1
			descripname = "descrip" + str(inum) + ".jpg"
			descrip = pygame.image.load(os.path.join("images", "page2", descripname))
			descriprect = descrip.get_rect()
			descriprect.top, descriprect.left = height, left
			self.screen.blit(descrip, descriprect)
			height += 100
	
	def drawPage3(self):
		self.drawPage3Title()
		height = 150
		
		for i in xrange(3):
			left = 100
			inum = i + 1
			self.drawGodNames(inum, left, height)
			left = self.width * 1.0/4
			self.drawSuperDescrip(inum, left, height)
			height += 200
	
	def drawGodNames(self, inum, left, height):
		godname = "god" + str(inum) + ".jpg"
		god = pygame.image.load(os.path.join("images", "page3", godname))
		godrect = god.get_rect()
		godrect.left, godrect.top = left, height
		self.screen.blit(god, godrect)
	
	def drawSuperDescrip(self, inum, left, height):
		supername = "super" + str(inum) + ".jpg"
		image = pygame.image.load(os.path.join("images", "page3", supername))
		superrect = image.get_rect()
		superrect.left, superrect.top = left, height
		self.screen.blit(image, superrect)
	
	def drawPage3Title(self):
		title = pygame.image.load(os.path.join("images","page3","superw.jpg"))
		titlerect = title.get_rect()
		titlerect.top = 10
		titlerect.centerx = self.width/2.0
		self.screen.blit(title, titlerect)
		
	def drawPage4(self):
		self.drawFirst()
		self.drawSecond()
		self.drawThird()
		self.drawFourth()
	
	def drawFirst(self):
		image = pygame.image.load(os.path.join("images", "page4", "pg41.jpg"))
		rect = image.get_rect()
		rect.left = 150
		rect.top = 100
		self.screen.blit(image, rect)
	
	def drawSecond(self):
		image = pygame.image.load(os.path.join("images", "page4", "pg42.jpg"))
		rect = image.get_rect()
		rect.left = 150
		rect.top = 200
		self.screen.blit(image, rect)
		self.drawInstructBars()
	
	def drawInstructBars(self):
		healthColor1 = (255, 150, 0)
		healthColor2 = (255,0,0)
		
		shadowGreen = (0, 75, 0)
		height = 15
		totalWidth = 200
		width1 = 60/100.0 * totalWidth
		width2 = 20/100.0 * totalWidth
		
		top = 300
		
		left1 = 200
		left2 = 600
		
		#initializing shadow bars
		shadowbar1 = (left1, top, totalWidth, height)
		shadowbar2 = (left2, top, totalWidth, height)
		
		#initializing health bars
		healthbar1 = (left1, top, width1, height)
		healthbar2 = (left2, top, width2, height)
		
		#drawing shadow bars
		pygame.draw.rect(self.screen, shadowGreen, shadowbar1, 0)
		pygame.draw.rect(self.screen, shadowGreen, shadowbar2, 0)
		
		#drawing health bars
		pygame.draw.rect(self.screen, healthColor1, healthbar1, 0)
		pygame.draw.rect(self.screen, healthColor2, healthbar2, 0)
		
	def drawThird(self):
		image = pygame.image.load(os.path.join("images", "page4", "pg43.jpg"))
		rect = image.get_rect()
		rect.left = 150
		rect.top = 400
		self.screen.blit(image, rect)
		self.drawInstructSuper(20, 150)
		self.drawInstructSuper(50, 400)
		self.drawInstructSuper(100, 650)
	
	def drawInstructSuper(self, demo, left):
		superbarfull = pygame.image.load(os.path.join("images", "bars", "superbarfull.jpg"))
		superbarempty = pygame.image.load(os.path.join("images", "bars", "superbarempty.jpg"))
		
		rect = superbarfull.get_rect()
		height = rect.height
		width = demo/100.0 * rect.width
		
		fullrect1 = pygame.Rect(0,0,width, height)
		emptyrect1 = superbarempty.get_rect()
		
		super1 = superbarfull.subsurface(fullrect1)
		
		superrect = super1.get_rect()
		
		superrect.left = emptyrect1.left = left
		
		superrect.top = emptyrect1.top = 500
		
		self.screen.blit(superbarempty, emptyrect1)
		self.screen.blit(super1, superrect)
	
	def drawFourth(self):
		image = pygame.image.load(os.path.join("images", "page4", "pg44.jpg"))
		rect = image.get_rect()
		rect.left = 150
		rect.top = 600
		self.screen.blit(image, rect)
		
	
	# This function draws the menu
	def menuDraw(self, inumber):
		self.screen.fill((0,0,0))
		pygame.display.set_caption("Greek Pong")
		
		xblock = self.width/2
		yblock = [2.75, 4.25, 5.75, 7.25]
		for i in xrange(len(yblock)):
			yblock[i] = yblock[i]/10 * self.height
		
		titlerect = self.drawTitle()
		
		self.drawPlay(xblock, yblock[0])
		self.drawInstructions(xblock, yblock[1])
		self.drawDifficulty(xblock, yblock[2])
		self.drawQuit(xblock, yblock[3])
		
		self.drawTorch(inumber)
		self.drawFlames(titlerect, inumber)
		pygame.display.update()
		
	def drawTitle(self):
		title = pygame.image.load(os.path.join("images", "greekpong.jpg"))
		titlerect = title.get_rect()
		titlerect.centerx = self.width/2.0
		titlerect.top = 0
		self.screen.blit(title, titlerect)
		return titlerect
	
	def drawPlay(self, x, y):
		play = pygame.image.load(os.path.join("images", "menu", "play.jpg"))
		self.playrect = play.get_rect()
		self.playrect.center = x, y
		self.screen.blit(play, self.playrect)
	
	def drawInstructions(self, x, y):
		instructions = pygame.image.load(os.path.join("images", "menu", "instructions.jpg"))
		self.instructionsrect = instructions.get_rect()
		self.instructionsrect.center = x, y
		self.screen.blit(instructions, self.instructionsrect)
		
	def drawDifficulty(self, x, y):
		difficulty = pygame.image.load(os.path.join("images", "menu", "difficulty.jpg"))
		self.difficultyrect = difficulty.get_rect()
		self.difficultyrect.center = x, y
		self.screen.blit(difficulty, self.difficultyrect)
		
	def drawQuit(self, x, y):
		quit = pygame.image.load(os.path.join("images", "menu", "quit.jpg"))
		self.quitrect = quit.get_rect()
		self.quitrect.center = x, y
		self.screen.blit(quit, self.quitrect)
	
	def drawTorch(self, inumber):
		torch = pygame.image.load(os.path.join("images", "torch.jpg"))
		torch1 = torch.get_rect()
		torch2 = torch.get_rect()
		left1 = self.width * 0.25/10
		right2 = self.width * 9.75/10
		top = self.height * 2.0/10
		torch1.topleft = left1, top
		torch2.topright = right2, top
		
		self.screen.blit(torch, torch1)
		self.screen.blit(torch, torch2)
		#self.drawFlames(torch1, torch2, inumber)
		
		
	def drawFlames(self, titlerect, inumber):
		inumber = inumber % 32
		imageNumber = inumber/2
		y = imageNumber / 4
		x = (imageNumber-(y*4))%4
		x = x*128
		y = y*128
		imageName = "flames.jpg"
		image = pygame.image.load(os.path.join("images", imageName))
		
		cropped = pygame.Rect(x,y,128,128)
		croppedimage = image.subsurface(cropped)
		
		imagerect1 = pygame.Rect(0,0,128,128)
		imagerect2 = pygame.Rect(0,0,128,128)
		
		imagerect1.right = titlerect.left - 10
		imagerect2.left = titlerect.right + 10
		self.screen.blit(croppedimage, imagerect1)
		self.screen.blit(croppedimage, imagerect2)
		
	
	# This function calls all required functions for the game to run.
	def run(self):
		pygame.init()
		pygame.display.set_caption("Greek Pong")
		margin = 50
		
		self.player1.reinit(margin, self.gameHeight, self.width)
		self.player2.reinit(margin, self.gameHeight, self.width)
		
		player1 = self.player1
		player2 = self.player2
		
		ball = Ball(self.width, self.gameHeight, self.screen, self)
		
		black = pygame.Color(0,0,0)
		counter = 0
		runGame = True
		while runGame and self.play:
			for event in pygame.event.get():
				if (event.type == QUIT):
					self.play = False
					self.state = False
					runGame = False
					break
				
			pygame.event.pump()
			keys = pygame.key.get_pressed()
			mouse = pygame.mouse.get_pressed()
			
			ball.moveBall(self.width, self.gameHeight, player1, player2, self)
				
			player1.movePaddle(keys, self.gameHeight, self.width, ball, self)
			player2.movePaddle(keys, self.gameHeight, self.width, ball, self)
			
			player1.useWeaponRack(keys, ball, player2, self)
			player2.useWeaponRack(keys, ball, player1, self)
			self.checkInstruction(keys)
			
			if counter == 400:
				counter = 0
			
			self.redrawAll(player1, player2, ball, counter)
			counter += 1
			
					
			if (self.checkWin(player1, player2)):
				runGame = False
				break
	
	def checkInstruction(self, keys):
		if keys[pygame.K_t]:
			self.instruction()
		
	
	def weapons(self, counter, player1, player2, ball):
		if counter == 0:
			self.num1 = random.randint(0,4)
			self.num2 = random.randint(0,4)
			self.collide1 = False
			self.collide2 = False
			
		weapon1 = self.weaponlist1[self.num1]
		weapon2 = self.weaponlist2[self.num2]
		if counter == 0:
			weapon1.x = random.randint(50, self.width/2 - 50)
			weapon2.x = random.randint(self.width/2 + 50, self.width - 50)

			weapon1.y = random.randint(50, self.gameHeight-50)
			weapon2.y = random.randint(50, self.gameHeight-50)
		
		if self.collide1 == False:
			weapon1.weaponDraw(self, weapon1.x, weapon1.y)
		if self.collide2 == False:
			weapon2.weaponDraw(self, weapon2.x, weapon2.y)
		
		if self.collide1 == False:
			if weapon1.collide(player1):
				self.collide1 = True
				for i in xrange(3):
					if player1.weaponrack[i] == 0:
						player1.weaponrack[i] = weapon1
						break
		
		if self.collide2 == False:
			if weapon2.collide(player2):
				self.collide2 = True
				for i in xrange(3):
					if player2.weaponrack[i] == 0:
						player2.weaponrack[i] = weapon2
						break
						
		self.drawWeaponRack(player1, player2)
	
	def drawWeaponRack(self, player1, player2):
		outer = 40
		colorouter1 = player1.checkColor()
		colorouter2 = player2.checkColor()
		
		colorinner = (0,0,0)
		inner = 38
		
		outerrect = pygame.Rect(0,0,outer,outer)
		innerrect = pygame.Rect(0,0,inner,inner)
		
		outerrect.center = self.width*2.0/10, self.gameHeight + 40
		innerrect.center = self.width*2.0/10, self.gameHeight + 40
		
		distance = 670
		
		for i in xrange(3):
			pygame.draw.rect(self.screen, colorouter1, outerrect, 0)
			pygame.draw.rect(self.screen, colorinner, innerrect, 0)
			if player1.weaponrack[i] != 0:
				x = outerrect.centerx
				y = outerrect.centery
				player1.weaponrack[i].weaponDraw(self, x, y) 
			
			
			outerrect.centerx += distance
			innerrect.centerx += distance
			
			pygame.draw.rect(self.screen, colorouter2, outerrect, 0)
			pygame.draw.rect(self.screen, colorinner, innerrect, 0)
			
			if player2.weaponrack[i] != 0:
				x = outerrect.centerx
				y = outerrect.centery
				player2.weaponrack[i].weaponDraw(self, x, y)
				
			outerrect.centerx -= distance
			innerrect.centerx -= distance
			
			outerrect.centerx += (outer+2)
			innerrect.centerx += (inner+4)
			
		
		
	def superWeapons(self, counter, player1, player2):
		greenSphere = pygame.image.load(os.path.join("images", "green.jpg"))
		greenrect1 = greenSphere.get_rect()
		greenrect2 = greenSphere.get_rect()
		if counter == 0:
			self.superx1 = random.randint(50, self.width/2 - 50)
			self.superx2 = random.randint(self.width/2 + 50, self.width - 50)

			self.supery = random.randint(50, self.gameHeight - 50)
			self.collidegreen1 = False
			self.collidegreen2 = False
		
		greenrect1.center = self.superx1, self.supery
		greenrect2.center = self.superx2, self.supery
		
		if self.collidegreen1 == False:
			self.screen.blit(greenSphere, greenrect1)
		
		if self.collidegreen2 == False:
			self.screen.blit(greenSphere, greenrect2)
			
		if self.collidegreen1 == False:
			if greenrect1.colliderect(player1.rect):
				self.collidegreen1 = True
				if player1.superbar < 100:
					player1.superbar += 20
		
		if self.collidegreen2 == False:
			if greenrect2.colliderect(player2.rect):
				self.collidegreen2 = True
				if player2.superbar < 100:
					player2.superbar += 20
				
		self.drawSuperBar(player1, player2)
	
	# This function draws the superbars.			
	def drawSuperBar(self, player1, player2):
		superbarfull = pygame.image.load(os.path.join("images", "bars", "superbarfull.jpg"))
		superbarempty = pygame.image.load(os.path.join("images", "bars", "superbarempty.jpg"))
		
		rect = superbarfull.get_rect()
		height = rect.height
		width1 = player1.superbar/100.0 * rect.width
		width2 = player2.superbar/100.0 * rect.width
		
		fullrect1 = pygame.Rect(0,0,width1, height)
		emptyrect1 = superbarempty.get_rect()
		
		fullrect2 = pygame.Rect(0,0,width2, height)
		emptyrect2 = superbarempty.get_rect()
		
		super1 = superbarfull.subsurface(fullrect1)
		super2 = superbarfull.subsurface(fullrect2)
		
		super1rect = super1.get_rect()
		super2rect = super2.get_rect()
		
		super1rect.right = emptyrect1.right = self.width/2.0 - 25
		super2rect.left = emptyrect2.left = self.width/2.0 + 25
		
		super1rect.top = emptyrect1.top = self.gameHeight+20
		super2rect.top = emptyrect2.top = self.gameHeight+20
		
		self.screen.blit(superbarempty, emptyrect1)
		self.screen.blit(superbarempty, emptyrect2)
		self.screen.blit(super1, super1rect)
		self.screen.blit(super2, super2rect)
		
		
			
		
	# This function checks whether any player has won by killing the other.
	def checkWin(self, player1, player2):
		if (player1.health <= 0):
			player2.score += 1
			self.hades[0] = False
			self.zeus[0] = False
			self.poseidon[0] = False
			return True
		elif (player2.health <= 0):
			player1.score += 1
			self.hades[0] = False
			self.zeus[0] = False
			self.poseidon[0] = False
			return True
		else:
			return False
	
		
	# This function	calls all the draw functions to display the game.
	def redrawAll(self,player1,player2,ball,counter):
		black = (0,0,0)
		self.screen.fill(black)
		
		self.weapons(counter, player1, player2, ball)
		self.superWeapons(counter, player1, player2)
		self.drawBoard()
		self.drawBall(ball)
		self.drawPaddle(player1, player2)
		self.drawText(player1, player2)
		self.drawHealth(player1, player2)
		self.drawScore(player1, player2)
		if self.zeus[0] == True:
			self.drawLightning(player1, player2)
		
		
		pygame.display.update()
	
	# This function draws the board.	
	def drawBoard(self):
		pygame.draw.line(self.screen, (255,255,255), (self.width/2, 0), (self.width/2, self.height))
		pygame.draw.line(self.screen, (255,255,255), (0,self.gameHeight), (self.width, self.gameHeight))
	
	# This function draws the ball.
	def drawBall(self, ball):
		if self.hades[3] == 3:
			self.hades[0] = False
			
		if self.hades[0] == True:
			if self.hades[1].player == 1:
				if ball.horizontalspeed < 0:
					self.screen.blit(ball.image, ball.rect)
				else:
					if ball.rect.right >= (self.width/10.0 * 2):
						pass
					else:
						self.screen.blit(ball.image, ball.rect)
			if self.hades[1].player == 2:
				if ball.horizontalspeed > 0:
					self.screen.blit(ball.image, ball.rect)
				else:
					if ball.rect.right <= (self.width/10.0 * 8):
						pass
					else:
						self.screen.blit(ball.image, ball.rect)
				
		else:	
			self.screen.blit(ball.image, ball.rect)
	
	# This function draws both the paddles.	
	def drawPaddle(self, player1, player2):
		self.screen.blit(player1.image, player1.rect)
		self.screen.blit(player2.image, player2.rect)
	
	# This function writes any text required to be written.	
	def drawText(self, player1, player2):
		player1Color = player1.checkColor()
		player2Color = player2.checkColor()
		
		message1 = "Player 1"
		message2 = "Player 2"
		
		size = 35
		font = pygame.font.Font(None, size)
		
		text1 = font.render(message1, 1, player1Color)
		text2 = font.render(message2, 1, player2Color)
		
		player1text = text1.get_rect()
		player1text.topleft = 1, (self.gameHeight+1)
		player2text = text2.get_rect()
		player2text.topright = self.width-1, (self.gameHeight+1)
		
		
		self.screen.blit(text1, player1text)
		self.screen.blit(text2, player2text)
	
	# This function draws the health bars of both the paddles.
	def drawHealth(self, player1, player2):
		healthColor1 = self.getHealthColor(player1)
		healthColor2 = self.getHealthColor(player2)
		
		shadowGreen = (0, 75, 0)
		height = 15
		totalWidth = 200
		width1 = player1.health/100.0 * totalWidth
		width2 = player2.health/100.0 * totalWidth
		
		top = self.height * 9.5/10
		
		left1 = 1
		left2 = self.width -totalWidth - 1
		
		#initializing shadow bars
		shadowbar1 = (left1, top, totalWidth, height)
		shadowbar2 = (left2, top, totalWidth, height)
		
		#initializing health bars
		healthbar1 = (left1, top, width1, height)
		healthbar2 = (left2, top, width2, height)
		
		#drawing shadow bars
		pygame.draw.rect(self.screen, shadowGreen, shadowbar1, 0)
		pygame.draw.rect(self.screen, shadowGreen, shadowbar2, 0)
		
		#drawing health bars
		pygame.draw.rect(self.screen, healthColor1, healthbar1, 0)
		pygame.draw.rect(self.screen, healthColor2, healthbar2, 0)
	
	# This function draws the score of the player
	def drawScore(self, player1, player2):
		size = 50
		font = pygame.font.Font(None, size)
		color1 = player1.checkColor()
		color2 = player2.checkColor()
		
		text1 = font.render(str(player1.score), 1, color1)
		text2 = font.render(str(player2.score), 1, color2)
		
		score1 = text1.get_rect()
		score1.topright = self.width/2 - 3, self.gameHeight + 1
		
		score2 = text2.get_rect()
		score2.topleft = self.width/2 + 3, self.gameHeight + 1
		
		self.screen.blit(text1, score1)
		self.screen.blit(text2, score2)
	
	def drawLightning(self, player1, player2):
		light = pygame.image.load(os.path.join("images", "light.jpg"))
		lightrect = light.get_rect()
		
		lightrect.centery = self.zeus[4]
		
		if self.zeus[1] == player1:
			self.zeus[3] += 6
			lightrect.left = self.zeus[3]
		else:
			self.zeus[3] -= 6
			lightrect.right = self.zeus[3]
		
		if self.zeus[2].rect.centery > self.zeus[4]:
			self.zeus[4] += 4
			lightrect.centery = self.zeus[4]
		elif self.zeus[2].rect.centery < self.zeus[4]:
			self.zeus[4] -= 4
			lightrect.centery = self.zeus[4]
		
		if self.zeus[2] == player1:
			if lightrect.colliderect(player1.rect):
				self.zeus[0] = False
				player1.health -= 30
			if lightrect.left <= 0:
				self.zeus[0] = False
		
		if self.zeus[2] == player2:
			if lightrect.colliderect(player2.rect):
				self.zeus[0] = False
				player2.health -= 30
			if lightrect.left >= self.width:
				self.zeus[0] = False
		
		self.screen.blit(light, lightrect)
		
		
		
	# This function returns the color that the health bar should be.	
	def getHealthColor(self, player):
		green = (0, 200, 0)
		orange = (255, 150, 0)
		red = (255, 0, 0)
		
		if player.health >= 70:
			return green
		elif player.health >= 40:
			return orange
		else:
			return red

game = Game()
