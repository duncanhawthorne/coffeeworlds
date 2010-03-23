#/usr/bin/env python
from __future__ import division #to give true division


"""
A 3D explorer
"""



import os, pygame, math, time, sys, socket,select, thread, colorsys, random
#from pygame.locals import *
sys.path.append(os.path.split(sys.path[0])[0])
from Net import *
from subpixelsurface import *
from math import *
#from matrix import *
from coffeeworlds import *
import coffeeworlds
#import coffeeworlds







	








pa = 0
pw = 0
ps = 0
pd = 0
pup = 0
pdo = 0

pri = 0
prk = 0
prj = 0
prl = 0
#mpx, mpy = 0,0
press3 = 0

def readinput(events):
	global mpx, mpy
	
	(mpx, mpy) = pygame.mouse.get_pos()[0] -320, pygame.mouse.get_pos()[1] -240
	pygame.mouse.set_pos([320, 240])
	
	camera.h += mpx/200
	camera.v += mpy/200
	
	
	global pa
	global pw
	global ps
	global pd
	global pup
	global pdo

	global pri
	global prk
	global prj
	global prl
	global press3

	

	for event in events:
		if event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				x = Bullet() 
				buls.append(x)
				sprites.append(x)
				x.firing = 1	
			if event.button == 3:
				camera.hooked = 1
				
		elif event.type == MOUSEBUTTONUP:
			if event.button == 3:
				camera.hooked = 0		
						
				
				
		if event.type == KEYDOWN:
			if event.key == K_q:
				pygame.quit()
				sys.exit()
			if event.key == K_a:
				prj = 1
			if event.key == K_d:
				prl = 1
			if event.key == K_w:
				pup = 1
			if event.key == K_s:
				pdo = 1

			if event.key == K_j or event.key == K_LEFT:
				prj = 1
			if event.key == K_l or event.key == K_RIGHT:
				prl = 1
			if event.key == K_i:
				pri = 1
			if event.key == K_k:
				prk = 1
				
			if event.key == K_UP:
				pup = 1
			if event.key == K_DOWN:
				pdo = 1
				
			if event.key == K_p:
				x = Bullet() 
				buls.append(x)
				sprites.append(x)
				x.firing = 1
							
		elif event.type == KEYUP:
			if event.key == K_a:
				prj = 0
			if event.key == K_d:
				prl = 0
			if event.key == K_w:
				pup = 0
			if event.key == K_s:
				pdo = 0								

			if event.key == K_UP:
				pup = 0
			if event.key == K_DOWN:
				pdo = 0							

			if event.key == K_j or event.key == K_LEFT:
				prj = 0
			if event.key == K_l or event.key == K_RIGHT:
				prl = 0
			if event.key == K_i:
				pri = 0
			if event.key == K_k:
				prk = 0

							
#	if pd == 1:
#		if 0 <= camera.v  <= math.pi:
#			camera.h += 0.05
#		else:
#			camera.h -= 0.05
#	if pa == 1:
#
#		if 0 <= camera.v <= math.pi:
#			camera.h -= 0.05
#		else:
#			camera.h += 0.05
#			
	##bodge	
	if camera.v > 2*math.pi:
		camera.v -= 2*math.pi
	if camera.v < 0:
		camera.v += 2*math.pi	
	######				
#			
#	if ps == 1:
#		camera.v -= 0.05
#	if pw == 1:
#		camera.v += 0.05
		
	if pup == 1:
		pos = [5,0,0]
		a,b,c = rtoi(camera, pos)
		
		camera.x += a
		camera.y += b
		camera.z += c
	if pdo == 1:
		pos = [-5,0,0]
		a,b,c = rtoi(camera, pos)
		
		camera.x += a
		camera.y += b
		camera.z +=c

	if prl == 1:
		pos = [0,0,5]
		a,b,c = rtoi(camera, pos)
		
		camera.x += a
		camera.y += b
		camera.z += c
	if prj == 1:
		pos = [0,0,-5]
		a,b,c = rtoi(camera, pos)
		
		camera.x += a
		camera.y += b
		camera.z += c
	if prk == 1:
		pos = [0,5,0]
		a,b,c = rtoi(camera, pos)
		
		camera.x += a
		camera.y += b
		camera.z += c	

	if pri == 1:
		pos = [0,-5,0]
		a,b,c = rtoi(camera, pos)
		
		camera.x += a
		camera.y += b
		camera.z += c	
		


def itor(self):
	None
			
def rtoi(camera, pos, *arg):
	x = cos(camera.h)*sin(camera.v), cos(camera.h)*cos(camera.v), - sin(camera.h)
	y = sin(camera.h)*sin(camera.v), + sin(camera.h)*cos(camera.v), + cos(camera.h)
	z = cos(camera.v), - sin(camera.v), 0
	if arg == 0:
		return  x[0] * pos[0] + x[1] * pos[1] + x[2] * pos[2]
	if arg == 1:
		return  y[0] * pos[0] + y[1] * pos[1] + y[2] * pos[2]
	if arg == 2:
		return  z[0] * pos[0] + z[1] * pos[1] + z[2] * pos[2]

	return  x[0] * pos[0] + x[1] * pos[1] + x[2] * pos[2], y[0] * pos[0] + y[1] * pos[1] + y[2] * pos[2], z[0] * pos[0] + z[1] * pos[1] + z[2] * pos[2]
							

#def distance3(a,b):
#	return ((a.x - b.x)**2 + (a.y - b.y)**2 + (a.z - b.z)**2)**(0.5)

def to2(x1,y1,z1):
	x = [sin(camera.v)*cos(camera.h), sin(camera.v)*sin(camera.h), cos(camera.v)]
	y = [cos(camera.v)*cos(camera.h), cos(camera.v)*sin(camera.h), -sin(camera.v)]
	z = [-sin(camera.h), cos(camera.h), 0]#? 
	
	pos = [x1 - camera.x, y1 - camera.y, z1 - camera.z]
		
	rr = x[0] * pos[0] + x[1] * pos[1] + x[2] * pos[2]
	rt = y[0] * pos[0] + y[1] * pos[1] + y[2] * pos[2]
	rp = z[0] * pos[0] + z[1] * pos[1] + z[2] * pos[2]
	
	if rr > 0:
		appeary = rt/rr*500
		appearx = rp/rr*500
	else:
		appeary = 0
		appearx = 0
	return appearx + 320, appeary + 240, rr
	None
	





class Dot(Ob):
	def __init__(self, coords=[0,0,0], color = 250):
		self.x = coords[0]
		self.y = coords[1]
		self.z = coords[2]
		self.rcolor = random.random()*250
		self.gcolor = random.random()*250
		self.bcolor = random.random()*250
		
		self.size =0
		
		
	def to2(self):
		
		self.appearx,self.appeary,self.rr = to2(self.x, self.y, self.z)
		if self.rr > 0:
			self.size = 5000/math.fabs(self.rr)	
		return self.appearx, self.appeary, self.rr
#		return
#		#return a,b
#		
#		
#		x = [sin(camera.v)*cos(camera.h), sin(camera.v)*sin(camera.h), cos(camera.v)]
#		y = [cos(camera.v)*cos(camera.h), cos(camera.v)*sin(camera.h), -sin(camera.v)]
#		z = [-sin(camera.h), cos(camera.h), 0]#? 
#	
#		self.pos = [self.x - camera.x, self.y - camera.y, self.z - camera.z]
#		
#		self.rr = x[0] * self.pos[0] + x[1] * self.pos[1] + x[2] * self.pos[2]
#		self.rt = y[0] * self.pos[0] + y[1] * self.pos[1] + y[2] * self.pos[2]
#		self.rp = z[0] * self.pos[0] + z[1] * self.pos[1] + z[2] * self.pos[2]
#	
#		if self.rr > 0:
#			self.appeary = self.rt/self.rr*500
#			self.appearx = self.rp/self.rr*500
#		self.size = 5000/math.fabs(self.rr)	




class Bullet(Dot):
	def __init__(self):
		Dot.__init__(self,[0,0,0])
		
		self.x = 0
		self.y = 0
		self.z = 0
		
		self.xv = 0
		self.yv = 0
		self.zv = 0
		
		self.xf = 0
		self.yf = 0
		self.zf = 0
		
		self.t = 0.2
		
		self.firing = 0
		
	def update(self):
		if self.firing == 1:
			self.firing = 2
			self.xv , self.yv, self.zv = rtoi(camera, [80,0,0])
			self.x = camera.x
			self.y = camera.y
			self.z = camera.z
		
		if self.firing == 2:
			self.zf = -0.2
	
	def calcpos(self):		
		self.xv += 2*self.xf*self.t
		self.yv += 2*self.yf*self.t
		self.zv += 2*self.zf*self.t
	
		self.x += self.xv*self.t
		self.y += self.yv*self.t
		self.z += self.zv*self.t

		#else:
		#	self.x = camera.x
		#	self.y = camera.y
		#	self.z = camera.z	


class Camera(Bullet):
	def __init__(self, coords=[0,0,0,math.pi/2,0]):
		Bullet.__init__(self)
		self.x = coords[0]
		self.y = coords[1]
		self.z = coords[2]
		self.v = coords[3]
		self.h = coords[4]
		
		self.hooked = 0
	def update(self):
		if self.hooked == 1:
			self.xf = (dots[0].x - camera.x)/1000
			self.yf = (dots[0].y - camera.y)/1000
			self.zf = (dots[0].z - camera.z)/1000
		if self.hooked == 0:
			self.xf = -self.xv/1000
			self.yf = -self.yv/1000
			self.zf = -self.zv/1000			
			


def setup_pygame():
	game = "bob"
	None
	global whilecount, smallresolution, resolution, screen, fullscreen, clock
	
	os.environ["SDL_VIDEO_CENTERED"] = "1" #hacky
	pygame.mixer.pre_init(44100,-16,2, 1024)
	random.seed()
	pygame.init()
	whilecount = 0
	pygame.event.set_grab(1)
	try:
		smallresolution = (int(pygame.display.Info().current_w*2/3), int(pygame.display.Info().current_h*2/3))
	except:
		print "requires pygame 1.8.1"
		sys.exit()
	resolution = (int(pygame.display.Info().current_w), int(pygame.display.Info().current_h))#current screen resolution
	try:
		1/0
		#screen = pygame.display.set_mode((0, 0)) #0.0 is default ie current screen resolution. would be ncie to get the resolution somehow
		##(0,0) bugs on dual screen setup
		#resolution = (0,0)
		screen = pygame.display.set_mode(smallresolution)#a hack so that when you leave fullscreeen you dont have a window over the whole screeen, but the iamge in jsut the top left, but rather revert back to this screen size
		screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)##change back to 0,0 fror publishing fixme
		fullscreen = 1
	except:
		print "get a newer version of pygame"
		screen = pygame.display.set_mode((640, 480))
		fullscreen = 0

	#fullscreen = 0		

	os.system("unset SDL_VIDEO_CENTERED")#sadly doesnt work (dont want it to be centered)
	#os.environ["SDL_VIDEO_CENTERED"] = "" #hacky#dont need it to be centered from now on
	#area = screen.get_rect()
	pygame.display.set_caption(game)

	pygame.mouse.set_pos(pygame.display.get_surface().get_rect().width/2, pygame.display.get_surface().get_rect().height/2) #thanks pymike
	pygame.mouse.set_visible(0)
	#pygame.event.set_grab(1) #grab the mouse

	clock = pygame.time.Clock()






if __name__ == "__main__":
	game = "3d"

	
	#whilecount, smallresolution, resolution, screen, fullscreen, clock = 0,0,0,0,0,0
	setup_pygame()
	








			
	
	
	camera = Camera()

	sprites = []

	dots = []

	dotrange = 1200
	for i in range(600):
		x = Dot([random.random()*2*dotrange-dotrange , random.random()*2*dotrange-dotrange, random.random()*2*dotrange-dotrange])
		dots.append(x)
		sprites.append(x)
	


	#dots.append(bul)

	buls = []



	#dots = [Dot([100 , 0, 0])]

	#meed to blit from back to front


	while 1:
	
		clock.tick(60)
		whilecount +=1
	
		readinput(pygame.event.get())
		screen.fill((0, 0, 0))
	
		for bul in buls:
			bul.update()
			bul.calcpos()
		#print bul.x, bul.y, bul.z
	
		for dot in sprites:
			dot.to2()
		
		
		sprites.sort(None, lambda item: item.rr, True)#so it draws things at the back first
		
		for dot in sprites:
			if dot.rr > 50:# and dot.z > 0:
				pygame.draw.circle(screen, (dot.rcolor, dot.gcolor, dot.bcolor), (int(dot.appearx), int(dot.appeary)) , int(dot.size), 0)

		for bul in buls:
			for dot in dots:
				if distance(dot, bul) <= 30:
					dots.remove(dot)
					sprites.remove(dot)
				
			if distance(camera, bul) >= 1000:
				buls.remove(bul)
				sprites.remove(bul)
	
	
		camera.update()
		camera.calcpos()
	
		if camera.hooked == 1:
			pygame.draw.line(screen, (250,0,0), camera.to2()[:2], dots[0].to2()[:2], 4)
		
	
		#a = to2(camera.x, camera.y, camera.z)[:2]
		#b = to2(dots[1].x, dots[1].y, dots[1].z)[:2]
		#pygame.draw.rect(screen, (0,0,0), (a[0], a[1], b[0]-a[0], b[1]-a[1]), 3)
	
		pygame.display.flip()#
	
	
	
	
#if __name__ == "__main__":
#	main()
