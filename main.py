import math
import random
import sys
import threading
import time

import pygame

import levelparser
from enemy import Enemy
from player import Player

current_time = time.time()

#General setup
pygame.init()
clock = pygame.time.Clock()

#Game Screen
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

RUN = True
BG = (0, 0, 0)

player = Player(screen, 800, 400)

player_group = pygame.sprite.Group()
player_group.add(player)

dt = 0.0001

level = levelparser.parse(screen)

has_died = False

#print(level[0])

exec1 = time.time()
exec(level[0])
print("LOADING ENEMIES:", time.time() - exec1, "milliseconds")

has_died = False

lastKey = None

pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

#x = threading.Thread(target=fun, daemon=True)

#x.start()

while RUN:
	#F1 = time.time()
	screen.fill(BG)

	#* Gets keys
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			player(event.key)
			lastKey = event.key
		if event.type == pygame.KEYUP:
			lastKey = None
	if lastKey in [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]:
		player(lastKey)
	#U1 = time.time()
	#* Does some screen stuff and updates the sprites
	exec(level[1])
	#print("EPROC:", 1 / (time.time() - U1), "FPS")
	player_group.update(dt)
	if has_died == True:
		pygame.quit()
		sys.exit()
	has_died = False
	player_group.draw(screen)
	dt = clock.tick(60) / 1000
	pygame.display.flip()
	#print("FPROC", 1 / (time.time() - F1), "FPS")