from entity import Entity


class Enemy(Entity):
	def __init__(self, screen, px, py, imagepath="bone.png", waittime=3, velocity=0, delay=0, angle=0, spx=None, spy=None):
		super().__init__(screen, px, py, imagepath, self.bounds, spx, spy)
		self.imagepath = imagepath
		self.waittime = waittime
		self.canmove = False
		self.velocity = velocity
		self.delay = delay
		self.angle = angle
		self.update(0)
	
	#* Bullet update with timer so it sets canmove to true when timer is at least zero
	def update(self, dt):
		#print(self.delay, self.waittime)
		if self.delay <= 0:
			self.set_image(self.imagepath)
		if self.delay >= 0:
			self.set_image('zero.png')
			self.delay -= dt
		if self.delay <= 0:
			if self.waittime > 0:
				self.waittime -= dt
			if self.waittime <= 0:
				self.canmove = True
			if self.canmove and self.velocity != 0:
				self.forward(self.velocity)
	
	#* Bullet can not move when canmove is false
	def move(self, relx, rely):
		if self.canmove:
			super(Enemy, self).move(relx, rely)
	
	#* Bullet can not move when canmove is false
	def forward(self, distance):
		if self.canmove:
			super(Enemy, self).forward(distance)
	
	#* This function checks if the entity is out of bounds, this can be overridden just in case
	def bounds(self):
		if self.px < 0 or self.px > self.windowX:
			self.kill()
		if self.py < 0 or self.py > self.windowY:
			self.kill()