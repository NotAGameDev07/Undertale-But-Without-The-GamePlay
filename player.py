import os

import pygame

from entity import Entity


class Player(Entity):
	def __init__(self, screen, px, py):
		self.ivd = 0
		self.hp = len(os.listdir('player'))
		self.states = ['player/' + i for i in sorted(os.listdir('player'), key=lambda x: int(x[5]))]
		super().__init__(screen, px, py, self.states[self.hp - 1], self.bounds)
		self.canMove = True
	
	#* Stops player from moving if trying to move out of bounds
	def bounds(self):
		#*Moves the player inside the box if player tries to move out of bounds
		if self.px < 0:
			self.px += self.image.get_width()
		elif self.py < 0:
			self.py += self.image.get_height()
		elif self.px > self.windowX:
			self.px = self.windowX - self.image.get_width()
		elif self.py > self.windowY:
			self.py = self.windowY - self.image.get_height()
	
	#* Player dies on collision
	def collides(self, other):
		if self.ivd > 0:
			return False
		hasCollided = super(Player, self).collides(other)
		if hasCollided[0] == False:
			return False
		if hasCollided == True or hasCollided != None:
			if self.hp == 0:
				self.kill()
			self.hp -= 1
			self.set_image(self.states[self.hp - 1])
			self.set_angle(self.angle)
			self.ivd = 2
		return hasCollided
	
	#* Update function for invincibility
	def update(self, dt):
		if self.ivd >= 0:
			self.ivd -= dt
	
	#* Handles keypresses and movements
	def __call__(self, key):
		yscale = -(key == pygame.K_UP) + (key == pygame.K_DOWN)
		xscale = -(key == pygame.K_LEFT) + (key == pygame.K_RIGHT)
		self.move(5 * xscale, 5 * yscale)