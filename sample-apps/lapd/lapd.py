#!/usr/bin/env python 

import pygame, sys, os, time, random, math
from pygame.locals import *

# optional
if not pygame.font: print 'Warning, no fonts'
if not pygame.mixer: print 'Warning, no sound'


pygame.init()
redscore = 0
bluescore = 0

def distance(p1, p2):
	return math.sqrt (( p1.x - p2.x ) * ( p1.x - p2.x ) + ( p1.y - p2.y ) * ( p1.y - p2.y ) )

def distance2(a, b, c, d):
	return math.sqrt (( a - c ) * ( a - c ) + ( b - d ) * ( b - d ) )
	
def findangle( q, w, e, r ): #angle a to b
	#if w - r <= 0:
		return math.pi + math.atan2( (q - e), (w - r) )
	#else:
		#return math.atan( (q - e) / (w - r) ) + math.pi

def input(events):
	for event in events:
		if event.type == QUIT:
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_UP:
				p1.fv = 10
			elif event.key == K_DOWN:
				p1.fv = -10
			elif event.key == K_RIGHT:
				p1.rr = -0.3
			elif event.key == K_LEFT:
				p1.rr = 0.3
			elif event.key == K_RETURN:
				for d in droids: # claim turret
					if d.team == 0 and distance (p1, d) <= 20:
						d.team = 1
				counttmp=0
				for tank in tanks:
					if tank.team == 1:
						if distance(p1, base[1]) <= 20 and distance2(tank.startpos[0], tank.startpos[1], tank.x, tank.y) <=10 : #launch new tank
							if counttmp == 0: #test to see if this is the first
								#tank.setPath(waypoints1) #redundant
								#tank.setPosition(tank.startpos[0], tank.startpos[1])
								onhit(tank)
								tank.i = 0 #start condition
								tank.next = tank.waypoints[0][0]
								counttmp = 1 #so the next time through it wont be the first
				counttmp=0
				for plane in planes:
					if plane.team == 1: # note that the launch point is differennt
						if distance2(p1.x, p1.y, 500, base[1].y) <= 20 and distance2(plane.startpos[0], plane.startpos[1], plane.x, plane.y) <=10 : #launch plane
							if counttmp == 0: #test to see if this is the first
								#plane.setPath(pwaypoints1) #redundant
								#plane.setPosition(plane.startpos[0], plane.startpos[1])
								onhit(plane)
								plane.next = plane.waypoints[0][0]
								plane.i = 0 #start condition
								counttmp = 1 #so the next time through it wont be the first
			elif event.key == K_p:
				p1.b.angle = p1.angle
				p1.b.fv = bulletvelocity
				
			elif event.key == K_w:
				p2.fv = 10
			elif event.key == K_s:
				p2.fv = -10
			elif event.key == K_d:
				p2.rr = -0.3
			elif event.key == K_a:
				p2.rr = 0.3
			elif event.key == K_SPACE:
				for d in droids:
					if d.team == 0 and distance (p2, d) <= 20:
						d.team = 2
				counttmp=0		
				for tank in tanks:
					if tank.team == 2:
						if distance(p2, base[2]) <= 20 and distance2(tank.startpos[0], tank.startpos[1], tank.x, tank.y) <=10: #launch new tank
							if counttmp == 0: #test to see if this is the first
								#tank.setPath(waypoints2) #redundant
								#tank.setPosition(tank.startpos[0], tank.startpos[1])
								onhit(tank)
								tank.next = tank.waypoints[0][0]
								tank.i = 0 #start condition
								counttmp = 1
				counttmp=0
				for plane in planes:
					if plane.team == 2: # note that the launch point is differennt
						if distance2(p2.x, p2.y, 500, base[2].y) <= 20 and distance2(plane.startpos[0], plane.startpos[1], plane.x, plane.y) <=10: #launch plane
							if counttmp == 0: #test to see if this is the first
								#plane.setPath(pwaypoints2) #redundant
								#plane.setPosition(plane.startpos[0], plane.startpos[1])
								onhit(plane)
								plane.next = plane.waypoints[0][0]
								plane.i = 0 #start condition
								counttmp = 1 #so the next time through it wont be the first
			elif event.key == K_q:
				p2.b.angle = p2.angle
				p2.b.fv = bulletvelocity
		elif event.type == KEYUP:
			if event.key == K_UP:
				p1.fv = 0
			elif event.key == K_DOWN:
				p1.fv = 0
			elif event.key == K_RIGHT:
				p1.rr = 0
			elif event.key == K_LEFT:
				p1.rr = 0
			elif event.key == K_w:
				p2.fv = 0
			elif event.key == K_s:
				p2.fv = 0
			elif event.key == K_d:
				p2.rr = 0
			elif event.key == K_a:
				p2.rr = 0
				
def loadImage(filename):
	return pygame.image.load(os.path.join(filename))

class Base:
	def __init__(self, x = 0, y = 0, team = 0):
		self.x = x
		self.y = y
		self.team = team
	
class A:
	def __init__(self, x = 0, y = 0, team = 0):
		self.x = x
		self.y = y
		self.fv = 0
		self.angle = 0
		self.rr = 0
		self.score = 0
		self.team = team
		self.health = 0
		self.startpos = [0, 0 ]
		self.tmp = 0
	def setPosition(self, x = 0, y = 0):
		self.x = x
		self.y = y
	def setSurface(self, surf):
		self.surface = surf
	def draw(self, screen):
		self.tmp = pygame.transform.rotate(team_surfaces[self.team], self.angle / math.pi * 360)
		screen.blit(self.tmp, (self.x, self.y))
	def move(self):
		self.x += self.fv * math.sin(self.angle)
		self.y += self.fv * math.cos(self.angle)	
		self.angle += self.rr
		if 'b' in dir(self) and self.b.fv == 0: #if it has a bullet, set the bullet to host
			self.b.setPosition(self.x, self.y)
	
class Player(A):
	def setBullet(self):
		self.b = A(self.x, self.y, team = 3)

class Bullet(A):
	pass
	
class Tank(Player):
	def setPath(self, waypoints):
		self.waypoints = waypoints
		self.randomizer = 0
		
		random.seed()
		self.i = len(self.waypoints) #should not be zero as dont want to start moving at the start
		self.next = self.waypoints[0][0] 
	def move(self):
		if self.i == (len(self.waypoints) -1 ) and distance2(self.x, self.y, self.next[0], self.next[1]) <= 7: #end of path, ie win
			if self.team == 1:
				global redscore; redscore += 1; print "redscore = %d" % redscore
				#self.setPosition(0, base[1].y) #return tank home
				onhit(self)			
			else:
				global bluescore; bluescore += 1; print "bluescore = %d" % bluescore
				#self.setPosition(0, base[2].y) #return tank home
				onhit(self)	
			#self.fv = 0 # stop tank
		if self.i < (len(self.waypoints) -1 ) and distance2(self.x, self.y, self.next[0], self.next[1]) <= 10:
			
			random.seed()
			self.i += 1
			self.next = self.waypoints[self.i][random.randint(0, (len(self.waypoints[self.i]) - 1 ))]
			
			self.angle = findangle(self.x, self.y, self.next[0], self.next[1])
			self.fv = 6
		
		self.x += self.fv * math.sin(self.angle)
		self.y += self.fv * math.cos(self.angle)	
		self.angle += self.rr
		if 'b' in dir(self) and self.b.fv == 0:
			self.b.setPosition(self.x, self.y)
			
			
class Plane(Player):
	def setPath(self, waypoints):
		self.waypoints = waypoints
		self.randomizer = 0
		
		#random.seed()
		self.i = -1 #should not be zero as dont want to start moving at the start
		self.next = self.waypoints[0][0] 
	def move(self):
		if (not self.i == -1) and distance2(self.x, self.y, self.next[0], self.next[1]) <= 10:
			
			random.seed()
			self.i += 1
			self.next = self.waypoints[1][random.randint(0, (len(self.waypoints[1]) - 1 ))]
			
			self.angle = findangle(self.x, self.y, self.next[0], self.next[1])
			self.fv = 6
		
		self.x += self.fv * math.sin(self.angle)
		self.y += self.fv * math.cos(self.angle)	
		self.angle += self.rr
		if 'b' in dir(self) and self.b.fv == 0:
			self.b.setPosition(self.x, self.y)

pygame.init()
team_surfaces = [loadImage("0.bmp"), loadImage("1.bmp"), loadImage("2.bmp"), loadImage("bullet.bmp")]
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Ultimate LAPD')
pygame.mouse.set_visible(0)

humh = 20
turh = 8
tanh = 8
damage = 4
plah = 8



#to do, should probably not have x, y in init. more apporpriate the set it later in for loop, as it is all the same, allowing simpler creation at this stage, and more concise lists.
#possible problem if the tanks start starting from outposts instead. not a huge deal. can always change any relevant startpos later

base = [ "0", Base( 250, 0, 1), Base( 250, 490, 2) ]
humans = [Player(base[1].x, base[1].y, team = 1), Player(base[2].x, base[2].y, team = 2)]
turrets = [ Player(100, 100, team = 0),  Player(100, 200, team = 0), Player(100, 300, team = 0), Player(100, 400, team = 0),\
		 Player(200, 100, team = 0),  Player(200, 200, team = 0), Player(200, 300, team = 0), Player(200, 400, team = 0),\
		 Player(300, 100, team = 0),  Player(300, 200, team = 0), Player(300, 300, team = 0), Player(300, 400, team = 0),\
		 Player(400, 100, team = 0),  Player(400, 200, team = 0), Player(400, 300, team = 0), Player(400, 400, team = 0),\
		 ]

tanks = [ Tank(0, base[2].y, team = 2), Tank(0, base[1].y, team = 1),  Tank(0, base[2].y, team = 2), Tank(0, base[1].y, team = 1) ,  Tank(0, base[2].y, team = 2), Tank(0, base[1].y, team = 1),  Tank(0, base[2].y, team = 2), Tank(0, base[1].y, team = 1)]

planes = [ Plane(20, base[2].y, team = 2), Plane(20, base[1].y, team = 1),  Plane(20, base[2].y, team = 2), Plane(20, base[1].y, team = 1) ,  Plane(20, base[2].y, team = 2), Plane(20, base[1].y, team = 1),  Plane(20, base[2].y, team = 2), Plane(20, base[1].y, team = 1)]

waypoints1 = [ ((0, base[1].y), (0, base[1].y)), ((base[1].x, base[1].y), (base[1].x, base[1].y)), ((50, 100), (150, 100), (250,100), (350,100), (450,100)),\
		((50, 200), (150, 200), (250,200), (350,200), (450,200)),\
		((50, 300), (150, 300), (250,300), (350,300), (450,300)),\
		((50, 400), (150, 400), (250,400), (350,400), (450,400)),\
		((base[2].x, base[2].y), (base[2].x, base[2].y)) ]

waypoints2 = [ ((0, base[2].y), (0, base[2].y)), ((base[2].x, base[2].y), (base[2].x, base[2].y)),\
		 ((50, 400), (150, 400), (250,400), (350,400), (450,400)),\
		((50, 300), (150, 300), (250,300), (350,300), (450,300)),\
		((50, 200), (150, 200), (250,200), (350,200), (450,200)),\
		((50, 100), (150, 100), (250,100), (350,100), (450,100)),\
		((base[1].x, base[1].y), (base[1].x, base[1].y)) ] #damn you non centralised sprites
		
pwaypoints1 = [ ((20, base[1].y), (20, base[1].y)), ( (50, 50), (150, 20), (250,40), (350,70), (450,62) ) ]
pwaypoints2 = [ ((20, base[2].y), (20, base[2].y)), ( (50, 350), (150, 420), (250,440), (350,470), (450,462) ) ]

droids = []
bullets = []
players = []

for human in humans:
	human.setBullet()
	bullets.append(human.b)
	players.append(human)
	players.append(human.b)
	human.health = humh
#	if human.team == 1:
#		human.startpos = (base[1].x, base[1].y)
#	else:
#		human.startpos = (base[2].x, base[2].y)
	human.startpos = (human.x, human.y) # as it is currently at the startpos
	
for turret in turrets:
	turret.setBullet()
	players.append(turret)
	players.append(turret.b)
	droids.append(turret)
	bullets.append(turret.b)
	turret.health = turh

for tank in tanks:
	tank.setBullet()
	players.append(tank)
	players.append(tank.b)
	droids.append(tank)
	bullets.append(tank.b)
	tank.health = tanh
	if tank.team == 1:
		tank.startpos = (waypoints1[0][0][0], waypoints1[0][0][1])
		tank.setPath(waypoints1)
	else:
		tank.startpos = (waypoints2[0][0][0], waypoints2[0][0][1])
		tank.setPath(waypoints2)
		
for plane in planes:
	plane.setBullet()
	players.append(plane)
	players.append(plane.b)
	droids.append(plane)
	bullets.append(plane.b)
	plane.health = plah
	if plane.team == 1:
		plane.startpos = (pwaypoints1[0][0][0], pwaypoints1[0][0][1])
		plane.setPath(pwaypoints1)
	else:
		plane.startpos = (pwaypoints2[0][0][0], pwaypoints2[0][0][1])
		plane.setPath(pwaypoints2)

def enemy(p, q):
	return (p.team == 1 and q.team == 2) or (p.team == 2 and q.team == 1)
		
def onhit(item):
	#print "hit"
	if item in bullets: #ie bullet
		item.fv = 0
	if item in turrets:
		if item.health >= damage:
			item.health -= damage
		else:
			item.health = turh
			item.team = 0
	if item in tanks or item in planes:
		if item.team == 1:
			if item.health >= damage:
				item.health -= damage
			else:
				item.health = tanh
				item.setPosition(item.startpos[0], item.startpos[1]) #start position
				item.fv = 0
				if item in planes:
					plane.i = -1
		else:
			if item.health >= damage:
				item.health -= damage
			else:	
				item.health = tanh
				item.setPosition(item.startpos[0], item.startpos[1]) #start position
				item.fv = 0
				if item in planes:
					plane.i = -1				
	if item in humans:
		if item.team == 1:
			if item.health >= damage:
				item.health -= damage
			else:	
				item.health = humh	
				item.setPosition(item.startpos[0], item.startpos[1]) #start position
				item.angle = 0
				item.fv = 0
		else:
			if item.health >= damage:
				item.health -= damage
			else:	
				item.health = humh	
				item.setPosition(item.startpos[0], item.startpos[1]) #start position
				item.angle = math.pi
				item.fv = 0

p1 = humans[0]
p2 = humans[1]
p2.angle = math.pi
bulletvelocity = 15



while (True):
	screen.fill((0, 0, 0))
	
	screen.blit(team_surfaces[3], (base[1].x, base[1].y)) #draw bases, startionary
	screen.blit(team_surfaces[3], (base[2].x, base[2].y)) #should probably be in players
	
	for p in players:
		p.move() #update poisiton
		p.draw(screen)
	
	for droid in droids:
		for player in players: #a droid auto firing on something
			if enemy(player, droid) and (distance(droid, player) <= 30): #droidrange
				if droid.b.fv == 0: #if bullet is there
					droid.b.fv = bulletvelocity # fire!
					droid.b.angle = findangle(droid.x, droid.y, player.x, player.y)
				
				if  -4 <= droid.b.x - player.x <= 10 and -4 <= droid.b.y - player.y <= 10: #if it hts
					onhit(droid.b)
					onhit(player)
	
			if distance(droid.b, droid) >= 30: #if it gets out of droidrange
				onhit(droid.b)
	
	for human in humans:
		for player in players:
			if enemy(human, player):
				if (not player in bullets) and (not human == player):
					if -4 <= human.b.x - player.x <= 10 and -4 <= human.b.y - player.y <= 10: #it hts
						onhit(player)
						onhit(human.b)
							
		if distance(human.b, human) >= 30: #if it gets out of range
			onhit(human.b)
						
	for tank in tanks: #claim turrets
		for turret in turrets:
			if distance(tank, turret) <=20:
				if turret.team == 0:
					turret.team = tank.team
	
	
	pygame.display.flip()
	input(pygame.event.get())
	time.sleep(0.1)
	
