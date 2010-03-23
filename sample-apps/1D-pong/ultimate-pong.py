#!/usr/bin/env python 

import pygame, sys, os, time, random
from pygame.locals import *

# optional
if not pygame.font: print 'Warning, no fonts'
if not pygame.mixer: print 'Warning, no sound'

pygame.init()

def loadImage(filename):
	return pygame.image.load(os.path.join(filename))
	
paddle_surface = loadImage("paddle.bmp")

class Paddle:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y
		self.xv = 0
		self.yv = 0
		self.score = 0
	def setPosition(self, x = 0, y = 0):
		self.x = x
		self.y = y
	def setSurface(self, surf):
		self.surface = surf
	def draw(self, screen):
		screen.blit(self.surface, (self.x, self.y))
	
p1 = Paddle()
p2 = Paddle()
p3 = Paddle()
p4 = Paddle()
ball = Paddle()

players = [ball, p1, p2, p3, p4]

width = 760#must divide by 20
height = 760
ballsize = 10
paddlespeed = ballsize
ballspeed = paddlespeed/2

clock = pygame.time.Clock()
	
def startgame():		
	global p1, p2, p3, p4, ball
	p1.setPosition(0, screen.get_height() - ballsize)
	p2.setPosition(screen.get_width() - ballsize, 0)
	p3.setPosition(screen.get_width() - ballsize, 0)
	p4.setPosition(0, screen.get_height() - ballsize)
	ball.setPosition(screen.get_width()/2, screen.get_height()/2)
	
	random.seed()
	r1 = random.randint(0, 1)
	r2 = random.randint(0, 1)
	if r1 == 0:
		ball.yv = 0
		if r2 == 0:
			ball.xv = -ballspeed
		else:
			ball.xv = ballspeed
	else:
		ball.xv  = 0
		if r2 == 0:
			ball.yv = -ballspeed
		else:
			ball.yv = ballspeed
	
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Ultimate Pong')
pygame.mouse.set_visible(0)
font = pygame.font.Font(None, 36)
t_ping = font.render("PING", 1, (90, 90, 90))
t_pong = font.render("PONG", 1, (90, 90, 90))
lose_render = font.render("LOSE", 1, (90, 90, 90))
textpos = t_pong.get_rect(centerx = screen.get_width()/2, centery =screen.get_height()/2)

pong = True	
	
startgame()

for player in [ p1, p2, p3, p4 ]:
	player.setSurface(paddle_surface)

ball.setSurface(paddle_surface)

def readinput(events):
	global p1, p2
	
	for event in events:
		if event.type == QUIT:
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_RIGHT:
				p1.xv = paddlespeed
			elif event.key == K_LEFT:
				p1.xv = -paddlespeed
			elif event.key == K_DOWN:
				p1.yv = paddlespeed
			elif event.key == K_UP:
				p1.yv = -paddlespeed
				
			elif event.key == K_s:
				p2.yv = paddlespeed
			elif event.key == K_w:
				p2.yv = -paddlespeed
			elif event.key == K_d:
				p2.xv = paddlespeed
			elif event.key == K_a:
				p2.xv = -paddlespeed
				
			elif event.key == K_h:
				p3.xv = paddlespeed
			elif event.key == K_f:
				p3.xv = -paddlespeed
			elif event.key == K_g:
				p3.yv = paddlespeed
			elif event.key == K_t:
				p3.yv = -paddlespeed
				
			elif event.key == K_l:
				p4.xv = paddlespeed
			elif event.key == K_j:
				p4.xv = -paddlespeed
			elif event.key == K_k:
				p4.yv = paddlespeed
			elif event.key == K_i:
				p4.yv = -paddlespeed
				
		elif event.type == KEYUP:
			if event.key == K_RIGHT:
				p1.xv = 0
			elif event.key == K_LEFT:
				p1.xv = 0
			elif event.key == K_DOWN:
				p1.yv = 0
			elif event.key == K_UP:
				p1.yv = 0
				
			elif event.key == K_s:
				p2.yv = 0
			elif event.key == K_w:
				p2.yv = 0
			elif event.key == K_d:
				p2.xv = 0
			elif event.key == K_a:
				p2.xv = 0
				
			elif event.key == K_h:
				p3.xv = 0
			elif event.key == K_f:
				p3.xv = 0
			elif event.key == K_g:
				p3.yv = 0
			elif event.key == K_t:
				p3.yv = 0
				
			elif event.key == K_l:
				p4.xv = 0
			elif event.key == K_j:
				p4.xv = 0
			elif event.key == K_k:
				p4.yv = 0
			elif event.key == K_i:
				p4.yv = 0


def hit():
	global pong
	if pong == True:
		pong = False
	else:
		pong = True
		
def collisions():
	if ball.x == p1.x + ballsize:
		if p1.y == ball.y:
			hit()
			if ball.xv != 0:
				ball.xv = -ball.xv
				ball.yv = 0
			else:
				ball.xv = ballspeed
				ball.yv = 0
	if ball.x == p2.x - ballsize:
		if p2.y == ball.y:
			hit()
			if ball.xv != 0:
				ball.xv = -ball.xv 
				ball.yv = 0
			else:
				ball.yv = 0
				ball.xv = -ballspeed
				
	if ball.y == p3.y + ballsize:
		if p3.x == ball.x:
			hit()
			if ball.yv != 0:
				ball.yv = -ball.yv
				ball.xv = 0
			else:
				ball.yv = ballspeed
				ball.xv = 0
	if ball.y == p4.y - ballsize:
		if p4.x == ball.x:
			hit()
			if ball.yv != 0:
				ball.yv = -ball.yv 
				ball.xv = 0
			else:
				ball.xv = 0
				ball.yv = -ballspeed			
		
def gameover():
	
		#caluclate scores
		if ball.x <= -ballsize:
			p2.score +=1
		elif ball.x >= screen.get_width():
			p1.score +=1
		elif ball.y <= -ballsize:
			p4.score +=1
		else:
			p3.score +=1
		
		#display scores
		tmp=0
		screen.fill((0, 0, 0))	
		for i in range(1,5):
			player_score = font.render("player %d: %d" % (i, players[i].score), 1, (100, 100, 100))
			screen.blit(player_score, (screen.get_width()/2 + 40, screen.get_height()/2 + 40 + tmp))
			tmp += 40
		screen.blit(lose_render, textpos)		
		pygame.display.flip()

while (True):
	clock.tick(20)
	if ball.x <= -ballsize or ball.x >= screen.get_width() or ball.y <=-ballsize or ball.y >=screen.get_height(): #ie game over	
		gameover()

		
		time.sleep(3)
		startgame()
		continue
	else:
		screen.fill((0, 0, 0))
		
	readinput(pygame.event.get())
	
	if pong:
		screen.blit(t_pong, textpos)
	else:
		screen.blit(t_ping, textpos)
	
	for player in [p1, p2, p3, p4, ball]:
		player.x += player.xv
		player.y += player.yv
		player.draw(screen)
	
	collisions()
	
	pygame.display.flip()

