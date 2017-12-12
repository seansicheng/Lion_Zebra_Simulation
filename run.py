import pygame
from pygame.locals import *
import os, sys
import random
import math
import copy

class animal(object):
	def __init__(self, filename, v, low, high):
		self.v = random.randint(v, 2*v)
		self.image = pygame.image.load(filename)
		self.image = pygame.transform.scale(self.image, (28, 28)).convert()
		self.angle = 2* math.pi * random.random()
		self.speed = [self.v*math.cos(self.angle), self.v*math.sin(self.angle)]
		#self.pos = [random.randint(width*low, width*high), random.randint(height*low, height*high)]
		self.pos = [random.randint(width*low, width*high)+ 100*math.cos(self.angle), random.randint(height*low, height*high) + 100*math.sin(self.angle)]
		self.track = list()	

	def is_out(self):
		return (self.pos[0] <= 28) | (self.pos[0] >= width-28) | (self.pos[1] <= 28) | (self.pos[1] >= height-28)

class Lion(animal):
	"""docstring for lion"""
	def __init__(self, *args):
		super(Lion, self).__init__(*args)
		self.eating = 0
		self.speed = [0, 0]
		self.score = 0

	
class animal_group():
	def __init__(self, num):
		self.lion = Lion("lion.jpg", 30, 0.15,0.15)
		self.zebra = list()
		for _ in range(num):
			self.zebra.append(animal("zebra.jpg", 10, 0.25,0.45))
	
	def update(self):
		nearest = 10000
		delete = list()
		i, n = 0, len(self.zebra)
		while i < n:
			each = self.zebra[i]
			y = (each.pos[1] - self.lion.pos[1])
			x = (each.pos[0] - self.lion.pos[0])
			r = math.sqrt(y**2 + x**2)
			if r < group.lion.v or each.is_out():
				if r < group.lion.v:	group.lion.score += 1
				self.zebra.pop(i)
				n -= 1
				continue
				#self.lion.eating = 3
				'''
			if r < nearest:		
				nearest = r
				self.lion.speed = [self.lion.v * x / r, self.lion.v * y / r]
				'''
			each.speed = [each.v * x / r, each.v * y / r]
			each.pos[0] += each.speed[0]
			each.pos[1] += each.speed[1]
			each.track.append(copy.copy(each.pos))
			i += 1


		if self.lion.eating > 0:
			self.lion.eating -= 1
		elif self.lion.is_out():
			self.lion.pos[0] -= 1.1*self.lion.speed[0]
			self.lion.pos[1] -= 1.1*self.lion.speed[1]
			self.lion.speed = [0, 0]
		else:
			self.lion.pos[0] += self.lion.speed[0]
			self.lion.pos[1] += self.lion.speed[1]
		self.lion.track.append(copy.copy(self.lion.pos))

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 60)

gameover = myfont.render('Game Over', False, (0, 0, 0))
screen_size = width, height = 2880, 1800
screen = pygame.display.set_mode((2880,1800), pygame.FULLSCREEN)
pygame.display.set_caption("Lion Zebra Simulation")
white = (255,255,255)
black = (0,0,0)
red = (0, 255, 0)

group = animal_group(500)
running = 1
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == K_ESCAPE:	sys.exit()
			elif event.key == K_SPACE:	running = 1- running
			elif event.key == K_UP:		group.lion.speed = [0, -group.lion.v ]
			elif event.key == K_DOWN:		group.lion.speed = [0, group.lion.v ]
			elif event.key == K_LEFT:		group.lion.speed = [-group.lion.v, 0]
			elif event.key == K_RIGHT:		group.lion.speed = [group.lion.v, 0]
	
	if running:
		group.update()
	screen.fill(white)
	score = myfont.render('SCORE: {0}'.format(group.lion.score), False, (0,0,0))
	screen.blit(score, (200, 200))
	
	screen.blit(group.lion.image, group.lion.pos)
	for pos in group.lion.track:
		pygame.draw.circle(screen, black, (int(pos[0]), int(pos[1])), 1, 0)

	if not len(group.zebra):		
		screen.blit(gameover,(width/2-200,height/2-100))
	for each in group.zebra:
		screen.blit(each.image, each.pos)
		
		for pos in each.track:
			pygame.draw.circle(screen, red, [int(pos[0]), int(pos[1])], 1, 0)
		
	pygame.display.flip()
