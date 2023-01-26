import math

import pygame


class Entity(pygame.sprite.Sprite):
	def __init__(self, screen, px, py, imagepath, boundscheck=None):
		super().__init__()
		self.windowX, self.windowY = screen.get_size()
		self.px = px
		self.py = py
		self.angle = 0
		self.og_image = pygame.image.load(imagepath).convert_alpha()
		self.og_image = pygame.transform.scale(self.og_image, (self.og_image.get_width() * 2, self.og_image.get_height() * 2))
		self.image = self.og_image
		self.rect = self.image.get_rect()
		self.rect.center = (px, py)

		#* Checks for if there has been a different bounds implementation for entities or child classes that inherit from this class
		if boundscheck == None:
			self.boundscheck = self.CIOOB
		else:
			self.boundscheck = boundscheck
	
	#* Sets image path for the Entity
	def set_image(self, imagepath):
		self.og_image = pygame.image.load(imagepath).convert_alpha()
		self.og_image = pygame.transform.scale(self.og_image, (self.og_image.get_width() * 2, self.og_image.get_height() * 2))
		self.useless_angle()
	
	#* This function checks if the entity is out of bounds, this can be overridden just in case
	def CIOOB(self):
		if self.px < 0 or self.px > self.windowX:
			self.kill()
		if self.py < 0 or self.py > self.windowY:
			self.kill()
	
	#* Rotates entity by angle in degrees relative to the current angle of the entity
	def rotate(self, angle):
		self.angle += angle
		self.image = pygame.transform.rotate(self.og_image, self.angle)
		self.rect = self.image.get_rect()
		self.rect.center = (self.px, self.py)
	
	#* Sets the angle of the entity in degrees
	def set_angle(self, angle):
		self.angle = angle
		self.image = pygame.transform.rotate(self.og_image, self.angle)
		self.rect = self.image.get_rect()
		self.rect.center = (self.px, self.py)
	
	#* Sets the angle of the entity in degrees, self.forward unaffected by angle
	def set_angle_mu(self, angle):
		self.image = pygame.transform.rotate(self.og_image, angle)
		self.rect = self.image.get_rect()
		self.rect.center = (self.px, self.py)
	
	#* Sets the angle of the entity in degrees
	#* Does not affect the direction it moves
	def useless_angle(self):
		self.image = pygame.transform.rotate(self.og_image, self.angle)
		self.rect = self.image.get_rect()
		self.rect.center = (self.px, self.py)
	
	#* Moves entity by x and y value relative to current position
	def move(self, relx, rely):
		self.boundscheck()
		self.rect.center = (self.px + relx, self.py + rely)
		self.px += relx
		self.py += rely
	
	#* Moves entity forward
	#^ Backward movement has not been checked to be working properly
	def forward(self, distance):
		self.boundscheck()
		delta_x = distance * math.cos(math.radians(360 - self.angle))
		delta_y = distance * math.sin(math.radians(360 - self.angle))
		self.rect.center = (self.px + delta_x, self.py + delta_y)
		self.px += delta_x
		self.py += delta_y
	
	#* Sets entitty position
	def set_position(self, x, y):
		self.rect.center = (x, y)
		self.px, self.py = x, y
	
	#* Sets entity to point at point
	def point_to(self, Tpoint):
		self.angle = math.atan2(Tpoint[1] - self.py, Tpoint[0] - self.px)
		self.angle = -math.degrees(self.angle)
		self.set_angle(self.angle)
	
	#* Collision detection
	def collides(self, other):
		if type(other) != pygame.sprite.Group:
			if abs(other.px - self.px) > 50 or abs(other.py - self.py) > 50:
				return False
		#* Collision with other sprite
		if type(other) != pygame.sprite.Group:
			self.boundscheck()
			other.boundscheck()
			mask1 = pygame.mask.from_surface(self.image)
			mask2 = pygame.mask.from_surface(other.image)
			offset = (other.px - self.px, other.py - self.py)
			return mask1.overlap(mask2, offset)
		else:
			others = []
			for i in other:
				if abs(i.px - self.px) < 20 and abs(i.py - self.py) < 20:
					others.append(i)
		#* Collision with sprite group
			mask1 = pygame.mask.from_surface(self.image)
			overlaps = [(mask1.overlap(pygame.mask.from_surface(i.image), (i.px - self.px, i.py - self.py)) != None) for i in others]
			return any(overlaps)