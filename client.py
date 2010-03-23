#!/usr/bin/env python
from __future__ import division #to give true division


"""
A 2D sidescrolling shooter written in pygame
"""



import os, pygame, math, time, sys, socket,select, thread, colorsys, random
from pygame.locals import *
sys.path.append(os.path.split(sys.path[0])[0])
from Net import *
if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'



memory = {}
def last(arg):#not used currently#my idea to replace test comparing current value of a variable to its value the last time it was checked
	#result = []
	found = 0
	for item in globals():
		if globals()[item] is arg:#thank you python, for being awesome. now vaiables know their own names
			#print item
			if item in memory:
				bob = memory[item]
				memory[item] = globals()[item]
				found = 1
				return bob #ie return old value
			else:
				memory[item] = globals()[item]
	if found == 0:
		return "wasnt in list"
				
				#if globals()[item] == memory[item]
				#	return True
				#else: 
				#	return False
			#result.append(item)
	#None
	


def connect():
	global client_server_sock
	client_server_sock = socket.socket()
	client_server_sock.connect(("localhost",6317))
	





def distance(p1, p2):
	total = 0
	for i in range(len(p1)):
		total += (p1[i] - p2[i])**2
	return total **(1/2)
	#distance2(p1[0], p1[1], p2[0], p2[1])
	
def distance2(a, b, c, d):
	return 	math.sqrt (( a - c )*( a - c ) + ( b - d )*( b - d ) )
	
def findangle( q, w, e, r ): #angle a to b
	return math.pi + math.atan2( (q - e), (w - r) )
	
def order(a, list):#
	score = -1#as it is going to match itself
	for i in range(len(list)):
		if a <= list[i]:#note < on its own gives tradition positions
			score +=1
	return score
			
	


def load_image(name, colorkey=None):
	fullname = os.path.join('data', name)
	image = pygame.image.load(fullname)
	image = image.convert_alpha()
	return image, image.get_rect()

def load_sound(name):
	fullname = os.path.join('data', name)
	sound = pygame.mixer.Sound(fullname)
	return sound


class Sound():
	def __init__(self, name):
		self.sound = load_sound(name)
		self.on = 0
		self.onlast = 0
	def play(self, dist):
		None
		#self.sound.set_volume(math.exp(-dist/400))
		#self.channel = self.sound.play() #by doing it through channel, should hopefully mean same sound from different players at different volumes
		self.sound.set_volume(math.exp(-dist/400))
		self.sound.play()#comment this line out to turn off sounds
	def stop(self):
		None
		self.sound.stop()
	def update(self):
		if self.on == 1 and self.onlast == 0:
			self.play()
		if self.on == 0 and self.onlast == 1:
			self.stop()
		self.onlast = self.on
		#need to set self.on to be zero when sound has finished playing
	def setArray(self):
		self.sound = pygame.sndarray.make_sound(self.array)
		
	


def scrpos2(value, coord):
	area = pygame.display.get_surface().get_rect()
	if coord == "x":
		#this causes a problem i havent been able to work through due to circularity of ideas. means you can move the mouse and move the guy#done
		tmpdist = (mpx - gunformotiontracking.xrectfixed)/4#so it moves with the mouse
		#tmpdist = (mpx - man.x)/4
		newpos = focused.fixed.x + tmpdist
		if -(newpos - back.rect.width/2) <= area.width/2:#so it is block from going off the map
			centerx = back.rect.width/2 - area.width/2
		elif newpos - (-back.rect.width/2)<= area.width/2:
			centerx = (-back.rect.width/2) + area.width/2
		else:
			centerx = newpos
		returnvalue =  (((value - centerx)*masterscale + centerx) - (centerx)) + area.width / 2
		return returnvalue
	else:
		tmpdist = (mpy - gunformotiontracking.yrectfixed)/4
		#tmpdist = (mpy - man.y)/4
		newpos = focused.fixed.y + tmpdist	
		if -(newpos - back.rect.height/2) <= area.height/2:
			centery = back.rect.height/2 - area.height/2
		elif newpos - (-back.rect.height/2)<= area.height/2:
			centery = (-back.rect.height/2) + area.height/2
		else:
			centery = newpos	
		return (((value - centery)*masterscale + centery) - centery) + area.height /2
def realpos2(value, coord):
	area = pygame.display.get_surface().get_rect()
	if coord == "x":
		#tmpdist = 0
		tmpdist = (mpx - gunformotiontracking.xrectfixed)/4
		#tmpdist = (mpx - man.x)/4
		newpos = focused.fixed.x + tmpdist
		if -(newpos - back.rect.width/2) <= area.width/2:
			centerx = back.rect.width/2 - area.width/2
		elif newpos - (-back.rect.width/2)<= area.width/2:
			centerx = (-back.rect.width/2) + area.width/2
		else:
			centerx = newpos
		return (((value - scrpos2(centerx, "x"))/masterscale + scrpos2(centerx, "x")) + centerx) - area.width / 2
	else:
		#tmpdist = 0
		tmpdist = (mpy - gunformotiontracking.yrectfixed)/4
		#tmpdist = (mpy - man.y)/4
		newpos = focused.fixed.y + tmpdist	
		if -(newpos - back.rect.height/2) <= area.height/2:
			centery = back.rect.height/2 - area.height/2
		elif newpos - (-back.rect.height/2)<= area.height/2:
			centery = (-back.rect.height/2) + area.height/2
		else:
			centery = newpos	
		return (((value - scrpos2(centery, "y"))/masterscale + scrpos2(centery, "y")) + centery) - area.height /2		
		
		
def scrpos(value0, value1):
	return (scrpos2(value0, "x"), scrpos2(value1, "y"))
	
def realpos(value0, value1):
	return (realpos2(value0, "x"), realpos2(value1, "y"))
		
def findempty():
	global hitter
	random.seed()
	count = 0
	foundstart = False
	hitter = 0#possible thread issue fixme, as both use global hitter variable
	while foundstart == False:
		count +=1
		x = random.randint(int(-front.scale/2), int(front.scale/2))
		y = random.randint(int(-front.height()/2), int(front.scale/front.height()/2))
		foundstart = True
		for i in range(-18, 18):
			for j in range(-18, 18):
				if isblack(*scrpos(x + i, y +j)):
					foundstart = False
					break
	return 	(x, y)	

				
masterscale = 1	

def debugdraw(a, b):
	global whilecount
	pygame.draw.circle(front.image, (0, 0, 0), (int(a + front.scale/2),int(b + front.height())), 2, 0)


class Ob():
	def __init__(self, x =0, y =0):
		self.x = x
		self.y = y
	def __getitem__(self, number):
		if number == 0:
			return self.x
		if number == 1:
			return self.y  	
		if number == 2:
			try:
				self.z
				return self.z
			except:
				#print "fail"
				return "garbage"
			#return self.z
		if number >2:
			return "garbage"#need to learn how to raise errors
	def __setitem__(self, number, result):
		if number == 0:
			self.x = result
		if number == 1:
			self.y = result
		if number == 2:
			self.z = result
	def __len__(self):
		#return 2
		count = 0
		a = True
		while a == True:
			#print self[count]
			if self[count] != "garbage" and self[count] != None:
				#self[count]
				count +=1
			else:
				a = False
				return count
		return count
	#	count = 0
	#	try:
	#		while True:
	#			self[count]
	#			count +=1
	#	except:
	#		return count
				

	
def get_alphaed( surf, alpha):#thanks claudio canepa
	global tmpsurf
	try:
		if front.scale != front.scalelast or 1==1:
			tmpsurf = pygame.transform.scale(tmpsurf, (int(surf.scale), int(surf.height())))
		print "sucessful try"
		#if tmpsurf.hopingforacrash == 1:
		#	None
	except:
		tmpsurf = pygame.Surface( surf.get_size(), SRCALPHA, 32)
	tmpsurf.fill( (255,255,255,alpha) )
	#tmpsurf.blit( surf, (0,0), None, BLEND_RGB_SUB)
	#BLEND_RGB_SUB
	tmpsurf.blit( surf, (0,0), None, BLEND_RGBA_MULT)
	return tmpsurf, tmpsurf.get_rect()			



def collidepoint(self):
	if self.hashitlastt == 1:
		self.lasttest = "t"
		return self.x, self.y - self.scale/2
	if self.hashitlastb == 1:
		self.lasttest = "b"
		return self.x, self.y + self.scale/2
	if self.hashitlastl == 1:
		self.lasttest = "l"
		return self.x - self.height()/2, self.y
	if self.hashitlastr == 1:
		self.lasttest = "r"
		return self.x + self.height()/2, self.y
		
	if self.lasttest == "t":
		return self.x, self.y - self.scale/2
	if self.lasttest == "b":
		return self.x, self.y + self.scale/2
	if self.lasttest == "l":
		return self.x - self.height()/2, self.y
	if self.lasttest == "r":
		return self.x + self.height()/2, self.y
			

#anticlockwise = 1
def findnext(self):
	global hitter
	found = False
	tmpangle = math.pi + findangle(self.x, self.y, *collidepoint(self))
	count = 1
	circlefrac = 1/32
	while found == False:
		if self.anticlockwise == 1:
			tmpangle += 2*math.pi *circlefrac
		else:
			tmpangle -= 2*math.pi *circlefrac
		a, b = collidepoint(self)[0] +count*self.scale*math.sin(tmpangle), collidepoint(self)[1] +count*self.scale*math.cos(tmpangle)#fixme, needs origwidth trciks
		hitter = self
		if isblack(*scrpos(a, b)):
			found = True
		count +=circlefrac/8
	
	
	
	
	if self.anticlockwise == 1:
		if self.lasttest == "t" and self.hashitlastr == 0:
			return a + 1*self.scale, b
		if self.lasttest == "b"and self.hashitlastl == 0:
			return a - 1*self.scale, b
		if self.lasttest == "l"and self.hashitlastt == 0:
			return a, b-1*self.scale
		if self.lasttest == "r"and self.hashitlastb == 0:
			return a, b+1*self.scale#fixme origwidth
	else:
		if self.lasttest == "t" and self.hashitlastl == 0:
			return a - 1*self.scale, b
		if self.lasttest == "b"and self.hashitlastr == 0:
			return a + 1*self.scale, b
		if self.lasttest == "l"and self.hashitlastb == 0:
			return a, b+1*self.scale
		if self.lasttest == "r"and self.hashitlastt == 0:
			return a, b-1*self.scale#fixme origwidth	


	if self.anticlockwise == 1:
		if self.lasttest == "t" and self.hashitlastr == 1:
			return a, b +1*self.scale
		if self.lasttest == "b"and self.hashitlastl == 1:
			return a, b-1*self.scale
		if self.lasttest == "l"and self.hashitlastt == 1:
			return a + 1*self.scale, b
		if self.lasttest == "r"and self.hashitlastb == 1:
			return a - 1*self.scale,
	else:
		if self.lasttest == "t" and self.hashitlastl == 1:
			return a, b+1*self.scale
		if self.lasttest == "b"and self.hashitlastr == 1:
			return a, b-1*self.scale
		if self.lasttest == "l"and self.hashitlastb == 1:
			return a + 1*self.scale, b
		if self.lasttest == "r"and self.hashitlastt == 1:
			return a - 1*self.scale, b		
	
	return a, b
	None

def chooseclock(self):
	if self.hashitlastt == 1:
		if self.xv >=0:
			plus = 1
		else:
			plus = 0
	if self.hashitlastb == 1:
		if self.xv >=0:
			plus = 0
		else:
			plus = 1
	if self.hashitlastl == 1:
		if self.yv >=0:
			plus = 0
		else:
			plus = 1
	if self.hashitlastr == 1:
		if self.yv >=0:
			plus = 1
		else:
			plus = 0
	self.anticlockwise = plus
				

class A(pygame.sprite.Sprite, Ob):
	"""Base class defining all the objects"""
	def pyname(self):
		result = []
		for item in globals():
			if globals()[item] is self:#thank you python, for being awesome. now vaiables know their own names
				result.append(item)		
		return result
	def width(self):
		return self.scale
	def height(self):
		return self.scale/self.origwidth*self.origheight
	def redraw(self):
		if self.rescale() or self.recolor() or self.reangle():
			result = True
		else:
			result = False
		return result
	def reangle(self):
		try:
			if self.angle != self.anglel:
				result = True
			else:
				result = False
		except:
			result =  True
		self.anglel = self.angle
		return result
	def recolor(self):
		try:
			if self.parent.rcolor != self.rcolorl or self.parent.rcolor != self.parent.rcolorl:
				result = True
			else:
				result = False
		except:
			result = True
			
		self.rcolorl = self.parent.rcolor
		return result			
	def rescale(self):
		try:
			if self.scale != self.scalel:# or self.angle != self.anglel:
				result = True
			else:
				result = False
		except:#for first time
			result = True
		self.scalel = self.scale
		return result			
	def __init__(self, limage = 0, limage2 = 0):
		self.parent = self#by default, so always a parent exists. ultimately means the parent of man is man
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		self.image1, self.rect1 = load_image(limage, None)
		self.image, self.rect = self.image1, self.rect1
		#self.image_subpixel = SubPixelSurface(self.image)

		self.original1, self.rect1 = load_image(limage, None)
		self.original, self.rect = self.original1, self.rect1
		if not limage2 == 0:
			self.image2, self.rect2 = load_image(limage2, None)#for hearts
			self.original2, self.rect2 = load_image(limage2, None)#for hearts
			
		self.image3, self.rect3 = get_alphaed(self.image1, 100)
		self.original3, self.rect3 = get_alphaed(self.image1, 100)
					
		self.origwidth =self.rect.width
		self.origheight = self.rect.height
		self.scale = self.rect.width
		self.scalelast = 0#so that it will do the first scale		
		
		self.x = 0
		self.y = 0
		self.xvc = 0.0
		self.yvc = 0.0
		self.xv = 0.0 #x velocity supplied
		self.yv = 0.0
		self.xf = 0.0
		self.yf = 0
				
		self.angle = 0
		self.scaleincrement = 0.0
		
		self.t = 0.2 #time step
		self.mu = 0.1
		self.modifiedx = 0
		self.modifiedy = 0
		self.jumpcount=0
		
		self.hashit=1
		self.hashitt=0
		self.hashitb=0
		self.hashitl=0
		self.hashitr=0
		
		self.xvlast = 0
		self.yvlast = 0
		self.xflast = 0
		self.yflast = 0
		
		self.name = 0
		self.framecount = 100
		self.weregoing = 0
		self.pressingbutton3 = 0
		self.maxfrac = 10
		self.maxframe = 8
		
		self.fullstate = 1
		self.timesincelasthealth = 9000
		self.title = 0
		self.firingstate = 0		
		self.timesinceupdate = 0
		self.explodecount=1
		
		self.hashitlastt = 0
		self.hashitlastb =0
		self.hashitlastl = 0
		self.hashitlastr = 0
		self.catchcount = 0
		self.modifiedscale = 0
		self.lasthealth = 1
		self.lastscale = 0
		self.score = 0
		
		self.init = Ob(0,0)
		self.fixed = Ob(0,0)
		self.best = Ob(0.0)

		
		self.random = random.random()
		self.hookhitcount =0
		
		self.rcolor = 0
		self.bcolor = 0
		self.gcolor = 0
		
		self.rcolorl = 0
		self.bcolorl = 0
		self.gcolorl = 0
		
		self.explosive = 0
		self.hasflag = 0
		
		self.flagtaken = 0
		
		self.sound = Sound("sample.wav")
		try:
			self.sound.array = pygame.sndarray.array(self.sound.sound)
		except:
			print "please install numeric for your version of python, a version for python 2.5 (windows) can be found on the pygame download page"	
		self.sound.parent = self
		
		#self.updated = 0
		self.flagbag = []
		
		self.tfirst = -1
		self.bfirst = -1
		self.lfirst = -1
		self.rfirst = -1
		self.lasttest = 0
		self.lasttest2 = 0
		self.listofblocks = []
		self.dealtwith = 0
		self.stopnow = 0
		self.werepoppin = 0
		self.oldlength = 0
		self.touching = 0
		
		self.best.x = 0
		self.best.y = 0
		self.targetfound = 0
		
		self.capturedlist = []
		self.captured = 0
		self.returned = 0
		
		try:
			self.target = man.init
		except:
			self.target = Ob()
		self.touchingcount = 0
		
		self.scroll = 0
		self.gunlist = []
		self.originallist = []
		self.state = 0
		self.lastscroll = 0
		self.on = 0
		self.onlast = 0
		self.blur = 0
		
	def update(self): #man and otherss

		

	
		if self in home and not self in clones:
			for opponent in players:
				if opponent in grounds or opponent in bots:
					if (not opponent is self) and opponent.name != self.name:#so bot  cant pick up network image of self
						if opponent.flag.flagtaken == 0:#grab a flag
							if distance(opponent.flag,self)<self.scale/1 + opponent.flag.height()/2:
								self.flagbag.append(opponent.flag)
								self.capturedlist.append(opponent.name)
			
			
			if distance(self.init,self)<self.scale/1 + self.flag.height()/2:# bring it home
				if self.flag.x == self.init.x and self.flag.y == self.init.y:
					self.captured = 1
					#if len(self.flagbag) != 0:
					#	returnedflag.play(distance(self, focused))
			if distance(self, self.flag) <self.scale/2:#return your own flag
				if self.flag.x != self.init.x or self.flag.y != self.init.y:
					if self.flag.flagtaken  == 0:
						self.returned = 1		

		if self.title == "bullet":
			self.scale = self.parent.scale/290*75
			self.scaledifference = 0
		self.scale *=masterscale
		
		global hitter
		self.lastscale = self.scale#fixme, move to end of update?
		self.scale = self.scale * (100 + self.scaleincrement)/100
		
		
		
		self.scaledifference = self.scale - self.lastscale

	
		#add forces together
		#variable forces already added in, so these must be adding not absolute!
		if self  in home or self in clones:
			self.yf += -self.yvc*self.mu/5#/10   # friction, based on velocity
			if self.hashitlastb == 0:
				self.xf += -self.xvc*self.mu
			else:
				self.xf += -self.xvc*self.mu	#more friction if you are running on the bottom#possible
		
		
		#calculate new velocity based on acceleration
		self.xvc += 2*self.xf*self.t
		self.yvc += 2*self.yf*self.t		
	
		#apply non physical absolute velocties
		if self.modifiedx == 1:
			self.xvc = self.xv
		if self.modifiedy == 1:
			self.yvc = self.yv
	
		self.maxfrac = int(max(math.fabs(self.xvc), math.fabs(self.yvc))/20) + 1#plus 1 to stop zero division#the faster you go, the more it will stop you going through walls. (can still go through really thin walls though)
		#print self.maxfrac
		

		
				
		hitter = self
		if self is man or (self.title == "bullet" and self.hashit == 0) or self in bots or self in clones: #correct line
		#if self is man:
			########
			for frac in  range(0,self.maxfrac+1):
			#is these isblack test come back true, no action taken, ie dont move the man
				if isblack(*scrpos(self.x + self.scale/2 + self.xvc*self.t*(frac/self.maxfrac), self.y)) or isblack(*scrpos(self.x + self.scale/2 + self.xvc*self.t*(frac/self.maxfrac), self.y - self.height()/(4.0))) or isblack(*scrpos(self.x + self.scale/2 + self.xvc*self.t*(frac/self.maxfrac), self.y + self.height()/(4.0))):
					self.hashit = 1
					self.hashitr = 1			
					if self.xvc >= 0:
						self.xvc *= frac/self.maxfrac
					break
			if self.xvc >=0: #so we dont end up moving twice
				self.x += self.xvc*self.t
			########
			for frac in  range(0,self.maxfrac+1):
				if isblack(*scrpos(self.x - self.scale/2 + self.xvc*self.t*(frac/self.maxfrac), self.y)) or isblack(*scrpos(self.x - self.scale/2 + self.xvc*self.t*(frac/self.maxfrac), self.y - self.height()/(4.0))) or isblack(*scrpos(self.x - self.scale/2 + self.xvc*self.t*(frac/self.maxfrac), self.y + self.height()/(4.0))):
					self.hashit = 1
					self.hashitl = 1				
					if self.xvc <= 0:
						self.xvc *= frac/self.maxfrac
					break
			if self.xvc <=0:
				self.x += self.xvc*self.t	
			########
			for frac in  range(0,self.maxfrac+1):
				if isblack(*scrpos(self.x , self.y+ self.height()/2 + self.yvc*(frac/self.maxfrac)*self.t)) or isblack(*scrpos(self.x - self.scale/(4.0), self.y+ self.height()/2 + self.yvc*(frac/self.maxfrac)*self.t)) or isblack(*scrpos(self.x + self.scale/(4.0), self.y+ self.height()/2 + self.yvc*(frac/self.maxfrac)*self.t)):
					self.hashit = 1
					self.hashitb = 1
					self.jumpcount = 0 #say it has 				
					if self.yvc >= 0:
						self.yvc *= frac/self.maxfrac #slow it down
					break
			if self.yvc >= 0:	
					self.y += self.yvc*self.t
			#########
			for frac in  range(0,self.maxfrac +1):
				if isblack(*scrpos(self.x , self.y - self.height()/2 + self.yvc*(frac/self.maxfrac)*self.t)) or isblack(*scrpos(self.x - self.scale/(4.0), self.y - self.height()/2 + self.yvc*(frac/self.maxfrac)*self.t)) or isblack(*scrpos(self.x + self.scale/(4.0), self.y - self.height()/2 + self.yvc*(frac/self.maxfrac)*self.t)):
					self.hashit = 1
					self.hashitt = 1
					#if self is bot:
					#	print "touchin top"
					if self.yvc <= 0:
						self.yvc *=frac/self.maxfrac
			if self.yvc <= 0:	
				self.y += self.yvc*self.t
	
		
												
		else:
			self.x += self.xvc*self.t
			self.y += self.yvc*self.t
		
		
			
		if self.title == "bullet": 
			if self.hashit == 1: #ie if it is a bullet, which has hit an object, ie ignore complicated bit above, and override
				if self.explodecount == 0:
					self.explode.play(distance(self, man))
					self.explodecount = 1

					if self.explosive == 1:
						#need to abstract into setblack, for many backgrounds
						destroy(self.x, self.y, self)
					
				self.x = self.parent.x
				self.y = self.parent.y
				self.xvc = 0
				self.yvc = 0
			else:
				self.explodecount = 0
			
			


		#non phyiscal things	
		if self.title == "bullet": #ie if it is a bullet
			self.angle = math.pi + math.atan2(self.xvc, self.yvc)
		
		#this could be the thing blocking shooting when you are stuck between walls
		if self in home or self in clones:
			if self.hashitb == 1 and self.hashitt == 1: #not perfect, it should check if expanding is going to make it collide, rather than whether t is colliding already
				if self.scaledifference > 0:
				
					self.scale = self.lastscale
					self.scaledifference = 0
			elif self.hashitl == 1 and self.hashitr == 1:
				if self.scaledifference > 0:
					self.scale = self.lastscale
					self.scaledifference = 0 
			else:
				None		

	
		
		if self.scaledifference > 0: #so when you shrink, just shrinks to the center
			if self.hashitb == 1:
				if isblack(*scrpos(self.x , self.y - (self.scale+self.scaledifference)*self.height()/self.width()/2)):#odd code#shouldnt this just have self.scale, as difference is already added
					None
				else:
					self.y -= (self.scaledifference*self.height()/(self.width()*2))
			if self.hashitt == 1:
				if isblack(*scrpos(self.x , self.y + (self.scale+self.scaledifference)*self.height()/self.width()/2)):
					None
				else:
					self.y += (self.scaledifference*self.height()/(self.width()*2))
			if self.hashitl == 1:
				if isblack(*scrpos(self.x + (self.scale + self.scaledifference), self.y)):
					None
				else:	
					self.x += (self.scaledifference/2)
			if self.hashitr == 1:
				if isblack(*scrpos(self.x - (self.scale + self.scaledifference), self.y)):
					None
				else:	
					self.x -= (self.scaledifference/2)
					
		if self is man:#opponents dont use this routine :(
			self.squishsoundcount = 0
			if self.hashitt == 1 and self.hashitlastt ==0:
				self.squishsoundcount = 1
			if self.hashitb == 1 and self.hashitlastb ==0:
				self.squishsoundcount = 1
			if self.hashitl == 1 and self.hashitlastl ==0:
				self.squishsoundcount = 1						
			if self.hashitr == 1 and self.hashitlastr ==0:
				self.squishsoundcount = 1
			if self.squishsoundcount == 1:
				hitwall.play(0)				
		
		try:
			self.updatecolor()
		except:
			None


		
		if self.redraw() or whilecount <=10:
			self.image = self.original
		
			if self in home and not self in clones:
				
				pygame.draw.circle(self.image, (self.rcolor, self.gcolor, self.bcolor), (int(self.origwidth/2), int(self.origheight/2)), int(self.origwidth*0.4 + 1), 0)#could draw this circle onto a blank surface and then render that at subpixel places

				
			self.image = pygame.transform.scale(self.image, (int(self.scale), int(self.height())))#line seems redundant, but somehow isnt
		
			if self.title == "bullet":
				self.image2 = self.original2
				self.image2 = pygame.transform.scale(self.image2, (int(self.scale), int(self.height())))
				self.image2.fill((255-self.parent.rcolor, 255-self.parent.gcolor, 255-self.parent.bcolor), None, BLEND_RGB_SUB)
				self.image.blit(self.image2, (0,0))
			self.image = pygame.transform.scale(self.image, (int(self.scale), int(self.height())))
			self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))


		
		self.rect = self.image.get_rect()
		self.rect.center = scrpos(self.x, self.y)
		

		self.hashitlastt = self.hashitt
		self.hashitlastb = self.hashitb
		self.hashitlastl = self.hashitl
		self.hashitlastr = self.hashitr		
		
		
			
		self.xvlast = self.xvc
		self.yvlast = self.yvc
		self.xflast = self.xf
		self.yflast = self.yf			
	
		#reset
		self.xv = 0
		self.yv = 0
		self.xf = 0
		self.yf = 0	
		self.modifiedx = 0
		self.modifiedy = 0
		
		self.hashitt = 0
		self.hashitb = 0
		self.hashitl = 0
		self.hashitr = 0
		self.scale /=masterscale
		


class Man(A):
	def setMultiBullet(self, image):
		for i in range(0,4):
			self.gunlist[0][1].append(Bullet(image))
			
			
			self.gunlist[0][1][i].image2, self.gunlist[0][1][i].rect2 = load_image(image[0:-4]+"variable.png", None)
			self.gunlist[0][1][i].original2, self.gunlist[0][1][i].rect2 = load_image(image[0:-4]+"variable.png", None)
			self.gunlist[0][1][i].parent = self
			self.gunlist[0][1][i].explode = pistolhit
			self.gunlist[0][1][i].title = "bullet"
			
	def setBullet(self, image):
		self.b = Bullet(image)
		self.b.image2, self.b.rect2 = load_image(image[0:-4]+"variable.png", None)
		self.b.original2, self.b.rect2 = load_image(image[0:-4]+"variable.png", None)
		self.b.parent = self.parent
		self.b.title = "bullet"
		self.b.explode = explode
		
	def setLaser(self):
		self.laser0 = Laser("hook.png")
		self.laser0.parent = self.parent
		self.laser0.title = "bullet"
		self.laser1 = Laser("hook.png")
		self.laser1.parent = self.parent
		self.laser1.title = "bullet"		
		
	def setFlame(self):
		self.flame = Flame("hook.png")
		self.flame.parent = self.parent
		self.flame.title = "bullet"			
		
	def setGun0(self, image):

		self.gun0= Gun(image)
		self.gun0.image2, self.gun0.rect2 = load_image(image[0:-4]+"variable.png", None)
		self.gun0.original2, self.gun0.rect2 = load_image(image[0:-4]+"variable.png", None)
		self.originallist.append(self.gun0.original2)
		
		self.gun0.parent = self
		self.gun0.title = "gun"
		
		self.gunlist.append([self.gun0, []])
		self.setMultiBullet("bullet0.png")
		

		self.gun0.gunnumber = 0
	def setGun1(self, image):
		
		
		self.gun1= Gun(image)
		self.gun1.image2, self.gun1.rect2 = load_image(image[0:-4]+"variable.png", None)
		self.gun1.original2, self.gun1.rect2 = load_image(image[0:-4]+"variable.png", None)
		self.originallist.append(self.gun1.original2)
		
		
		self.gun1.parent = self
		self.gun1.title = "gun"
		
		self.gun1.setBullet("bullet1.png")
		

		self.gunlist.append([self.gun1, [self.gun1.b]])
		
		self.gun1.gunnumber = 1
				
	def setGun2(self, image):
		
		
		self.gun2= Gun(image)
		self.gun2.image2, self.gun2.rect2 = load_image(image[0:-4]+"variable.png", None)
		self.gun2.original2, self.gun2.rect2 = load_image(image[0:-4]+"variable.png", None)
		self.originallist.append(self.gun2.original2)
		
		self.gun2.parent = self
		
		self.gun2.setLaser()
		self.gun2.laser0.lasercross = Ob()
		self.gun2.laser1.lasercross = Ob()
		
		self.gun2.laser0.lasercount = 0
		self.gun2.laser1.lasercount = 1

		self.gunlist.append([self.gun2, [self.gun2.laser0, self.gun2.laser1]])
		self.gun2.gunnumber = 2
	def setGun3(self, image):
		
		
		self.gun3= Gun(image)
		self.gun3.image2, self.gun3.rect2 = load_image(image[0:-4]+"variable.png", None)
		self.gun3.original2, self.gun3.rect2 = load_image(image[0:-4]+"variable.png", None)
		self.originallist.append(self.gun3.original2)
		
		self.gun3.parent = self
		self.gun3.flamecross = Ob()
		
		self.gun3.setFlame()
		self.gun3.b = self.gun3.flame
		self.gun3.flame.weregoing = 0

		self.gunlist.append([self.gun3, [self.gun3.flame]])
		self.gun3.gunnumber = 3
	def setGun4(self, image):
		
		
		self.gun4= Gun(image)
		self.gun4.image2, self.gun4.rect2 = load_image(image[0:-4]+"variable.png", None)
		self.gun4.original2, self.gun4.rect2 = load_image(image[0:-4]+"variable.png", None)
		self.originallist.append(self.gun4.original2)
		
		
		self.gun4.parent = self
		self.gun4.title = "gun"
		
		
		self.clone = Bot("mantransparent.png")
		self.clone.scale = 50
		self.clone.name = "clone"
		self.clone.clonecount = 0
		self.clone.parent = self
		
		self.gun4.clone = self.clone
		self.gun4.clone.setHook()
		self.gun4.clone.setCross()
		
		clones.append(self.gun4.clone)

		self.gunlist.append([self.gun4, [self.gun4.clone, self.gun4.clone.hook, self.gun4.clone.cross]])	
		self.gun4.gunnumber = 4
	def setHook(self):
		self.hook = Hook("hook.png")
		self.hook.parent = self
		self.hook.title = "hook"
	def setCross(self):
		self.cross = Cross("cross.png")
		self.cross.parent = self
		self.cross.title = "cross"
	def setFlag(self, image):
		self.flag =Flag(image)
		self.flag.image2, self.flag.rect2 = load_image(image[0:-4]+"variable.png", None)
		self.flag.original2, self.flag.rect2 = load_image(image[0:-4]+"variable.png", None)
		self.flag.parent = self
		self.flag.title = "flag"	
	def updatecolor(self):
		try: #otherwise it is a race condition between the two threads
			self.colortmpcalc = self.position/numberofplayers *0.8 + 0.2##scale 0.2 to 1
		except:
			if self in clone:
				self.colortmpcalc = 0 #black
			else:
				self.colortmpcalc = 1	#ie full color
		
		self.rcolor = colorsys.hsv_to_rgb(self.random, self.lasthealth, self.colortmpcalc)[0] *255 
		self.gcolor = colorsys.hsv_to_rgb(self.random, self.lasthealth, self.colortmpcalc)[1] *255
		self.bcolor = colorsys.hsv_to_rgb(self.random, self.lasthealth, self.colortmpcalc)[2] *255
		
		self.color = (self.rcolor, self.gcolor, self.bcolor)		


			
	
scene = "3"
#c,d = 0,-800
class Bot(Man):
	def preupdate(self):
		self.c, self.d = self.target.x, self.target.y
		
		
		if self.touching == 0:#youve only got there once youve left a wall
			if self.targetfound == 1:
				None
				if distance(self, self.target) <=30:
					self.targetfound = 0
		
		if self.touching == 0 or self.targetfound == 0:		
			if len(self.flagbag) != 0:#so updates if get new flag#should only do this once, as soon as disconnects from wall
				#self.targetfound == 0
				self.target = self.init
				self.targetfound = 1
				self.touching = 0
		
		if self.touching == 0 or self.targetfound == 0:
			if whilecount >=10:#littel start up hack
				if self.flag.x != self.init.x or self.flag.y != self.init.y:#go and rescue your flag, higher priority (ie later) than capturing enemy's flag
				#should be your flag but rather the network image of your flag?	
					if self.flag.flagtaken == 1:
						self.target = self.flag.holder
					else:
						self.target = self.flag
					self.targetfound = 1
					self.touching = 0#to break off objects
			
			
		if self.targetfound == 0:# and 1==2:

			possibles = [[],[]]
			for player in players:
				if not player is self:
					possibles[0].append(player)
					possibles[0].append(player.flag)
					
			for item in possibles[0]:
				possibles[1].append(distance(item, self))
			
			#fixme all nonsense, not even comparing distances#####THIS IS A SERIOUS FIXME
			for i in range(len(possibles[1])):
				if order (possibles[1][i], possibles[1]) == 1:
					self.target = possibles[0][i]
				
			if self.target == man:#bodge safety
				self.target = man.fixed
					
			self.targetfound = 1
			self.touching = 2
			
			
		
		if self.touching == 2:
			if self.touchingcount >= 4:
				self.touching = 0
			self.touchingcount +=1	
		
		else:
			self.touchingcount = 0
		
		if self.touching == 0:
			if self.hashitlastt == 1 or self.hashitlastb == 1 or self.hashitlastl == 1 or self.hashitlastr == 1:
				chooseclock(self)
				self.best.x = self.x
				self.best.y = self.y
				self.touching = 1
			
		if self.hashitlastt == 1:
			if self.d - self.y > 0:
				if distance2(self.x, self.y, self.c, self.d) < distance2(self.best.x, self.best.y, self.c, self.d):
					self.touching = 2
		if self.hashitlastb == 1:
			if self.d - self.y < 0:
				if distance2(self.x, self.y, self.c, self.d) < distance2(self.best.x, self.best.y, self.c, self.d):
					self.touching = 2
		if self.hashitlastl == 1:
			if self.c - self.x > 0:
				if distance2(self.x, self.y, self.c, self.d) < distance2(self.best.x, self.best.y, self.c, self.d):
					self.touching = 2
		if self.hashitlastr == 1:
			if self.c - self.x < 0:
				if distance2(self.x, self.y, self.c, self.d) < distance2(self.best.x, self.best.y, self.c, self.d):
					self.touching = 2
			
		
		if self.touching == 1:
			bob = 0
			None
			if distance2(self.x, self.y, self.c, self.d) < distance2(self.best.x, self.best.y, self.c, self.d):
				self.best.x = self.x; self.best.y = self.y
			a,b = findnext(self)
			#debugdraw(a, b)
			self.angle = findangle(self.x, self.y, a, b)

			#self.xf += 70*math.sin(self.angle)*20/200*2*3/20
			#self.yf += 70*math.cos(self.angle)*20/200*2*3/20
			self.xv = 70*math.sin(self.angle)*20/200*2*3
			self.yv = 70*math.cos(self.angle)*20/200*2*3			
			
			#role around
		else:
			self.angle = findangle(self.x, self.y, self.c, self.d)
			if distance(self, self.target) <=100: #only slows down when gets close
				bob = 0
				##self.xf += 70*math.sin(self.angle)*distance2(self.c, self.d, self.x, self.y)/200/2/20
				##self.yf += 70*math.cos(self.angle)*distance2(self.c, self.d, self.x, self.y)/200/2/20
				self.xv = 70*math.sin(self.angle)*distance2(self.c, self.d, self.x, self.y)/200/2
				self.yv = 70*math.cos(self.angle)*distance2(self.c, self.d, self.x, self.y)/200/2				
			else:
				bob = 0
				##self.xf += 70*math.sin(self.angle)*2/2/20
				##self.yf += 70*math.cos(self.angle)*2/2/20
				self.xv = 70*math.sin(self.angle)*2/2
				self.yv = 70*math.cos(self.angle)*2/2					
				
		if bob == 0:		
			self.modifiedx = 1
			self.modifiedy = 1
		
		
		self.gun.angle = math.pi + findangle(self.x, self.y, self.c, self.d)
		self.b.yf += 22*man.scale/100*masterscale
		if self.target in players:
			if whilecount // 10 - whilecount / 10 == 0:#not such rapid firing
				if self.b.hashit == 1:#make sure in sync
						self.b.explodecount = 0
						self.b.explosive = 0
						pistolfire.play(distance(self, man))
						self.b.hashit = 0
						self.b.angle = self.gun.angle
						self.b.x = int(self.x)
						self.b.y = int(self.y)
						self.b.xv = int(500*-math.sin(self.gun.angle)*(self.scale/100))*masterscale + self.xvlast
						self.b.yv = int(500*-math.cos(self.gun.angle)*(self.scale/100))*masterscale + self.yvlast#possible fix me, changed from self.b.scale
						self.b.modifiedx = 1
						self.b.modifiedy = 1
				



		
class Bullet(A):
	pass
		
	
class Gun(Man):	
	def update(self):
		self.original2 = ultimateman.originallist[self.gunnumber % len(ultimateman.gunlist)]#hack

		self.scale = self.parent.scale*1.5
		self.scale *=masterscale
		
		
		self.x = self.parent.x
		self.y = self.parent.y
		
		if self.parent == man and focused == man:
			self.angle = math.pi + math.atan2(mpx - scrpos2(self.x, "x"), mpy - scrpos2(self.y, "y"))
		
		if self.rescale() or self.recolor():# or True:	
			self.image = self.original
		
			self.image = pygame.transform.scale(self.image, (int(self.scale), int(self.height())))
		
			#remove this to turn off gun coloring
			self.image2 = self.original2
			self.image2 = pygame.transform.scale(self.image2, (int(self.scale), int(self.height())))
			self.image2.fill((255-self.parent.rcolor, 255-self.parent.gcolor, 255-self.parent.bcolor), None, BLEND_RGB_SUB)
			self.image.blit(self.image2, (0,0))
		
			self.image = pygame.transform.scale(self.image, (int(self.scale), int(self.height())))
			self.imagestraight = self.image
		#else:
		if math.pi < self.angle < 2*math.pi:
			self.image = self.imagestraight
		else:
			self.image = self.imagestraight	
			self.image = pygame.transform.flip(self.image, 1, 0)		
		self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))		
		
		self.rect = self.image.get_rect()
		self.rect.center = scrpos(self.x,self.y)
		self.scale /=masterscale

class Flag(A):
	def update(self):

		if self.flagtaken  == 1:
			self.x = self.holder.x + self.holder.scale/2/2
			self.y = self.holder.y - self.height()/2#should be different to line above
			self.scale = self.holder.scale
		else:
			None
			self.scale = 30	
			
		if True:#self.redraw():	#redraw was buggy, probably a parent issue. fixme
			self.image = self.original	
			self.image = pygame.transform.scale(self.image, (int(self.scale), int(self.height())))#line seems redundant
		
			self.image2 = self.original2
			self.image2 = pygame.transform.scale(self.image2, (int(self.scale), int(self.height())))
		
			try:
				self.image2.fill((255-self.parent.rcolor, 255-self.parent.gcolor, 255-self.parent.bcolor), None, BLEND_RGB_SUB)
			except:
				print "requires pygame 1.8.1"
				sys.exit()#fixme, put this back in
		
			self.image.blit(self.image2, (0,0))
		
			self.image = pygame.transform.scale(self.image, (int(self.scale), int(self.height())))
			self.flipstate = 1
		
		if self.flagtaken  == 1:
			if math.pi < self.holder.gun.angle < 2*math.pi:
				if self.flipstate == 1:
					self.image = pygame.transform.flip(self.image, 1, 0)#this will bug, due to flipping
					self.flipstate = 0
				try:
					self.x -= self.holder.scale/2	
				except:#must be held by no one
					None
			else:
				if self.flipstate == 0:	
					self.image = pygame.transform.flip(self.image, 1, 0)#this will bug, due to flipping
					self.flipstate = 1
	
		self.scale *=masterscale

		self.scalelast = self.scale
		
		self.rect = self.image.get_rect()
		self.rect.center = scrpos(self.x,self.y)#	
		self.scale /=masterscale
	
class Ground(A):
	def update(self):
		#blurring stuff	
		if self is front:#more general needed for more fronts#general fixme on thihs point#ie if self in fronts
				if blur == 2:
					if needsmask == 0:
						self.image = self.image3
				if blur == 0:
					if needsmask == 0:
						self.image = self.image1				
		
		self.scale *=masterscale
		if self.redraw():#we dont want to have to redo scaling images for these big images everytime
			self.image1 = pygame.transform.scale(self.original1, (int(self.scale), int(self.height())))
			self.image3 = pygame.transform.scale(self.original3, (int(self.scale), int(self.height())))
			self.image = self.image1#just the first time setup#should be done elsewhere fixme
		
			self.rect = self.image.get_rect()#can be tabbed, as this only changes if the image changes, ie needs a redraw (FIXME, ie put me everywhere)
		self.rect.center = scrpos(self.x,self.y)#	
		self.scale /=masterscale
		
class Cross(A):
	def update(self):
		if self is man.cross:#fixme, cross should stop being a sprite soon
			if self.parent.hook.firingstate == 0:
				self.x = man.x
				self.y = man.y
		if self.title == "cursor":
			(self.x, self.y) = realpos(mpx, mpy)
			self.scale = focused.scale/2#could cause problems with the two threads, due to setting scale somewhere in the middle....(mastersclae type problem)
		self.scale *=masterscale
		
		if self.redraw():
			self.image = self.original
			self.image = pygame.transform.scale(self.image, (int(self.scale), int(self.height())))		
			if self.title == "cursor":
				self.image.fill((255-focused.rcolor, 255-focused.gcolor, 255-focused.bcolor), None, BLEND_RGB_SUB)#awesome, just changes the non transparent colors#
				
		
		
		self.rect = self.image.get_rect()
		self.rect.center = scrpos(self.x,self.y)#	
		self.scale /=masterscale			
	
framecount = 1
#maxframe = 8
class Hook(A):
	def update(self):
		if (self.weregoing == 1 or (self.weregoing == 0 and self.framecount < self.maxframe)) and self.pressingbutton3 == 1:
			self.scale *=masterscale
			self.firingstate = 1
			self.endx = self.parent.x + (self.framecount/self.maxframe)*(self.parent.cross.x - self.parent.x)
			self.endy = self.parent.y + (self.framecount/self.maxframe)*(self.parent.cross.y - self.parent.y) 
			
			self.x = (self.endx + self.parent.x)/2
			self.y = (self.endy + self.parent.y)/2
			self.scale = distance2(self.endx, self.endy, self.parent.x, self.parent.y)
			#print self.scale
			self.angle = findangle(self.parent.x, self.parent.y, self.endx, self.endy)#same as if used cross coordinates
			
			try: #crash if too big
				self.otherscale = 600/(self.scale-1)+1
			except:
				self.otherscale = 600
			

			if self.redraw():
				self.image = self.original
				try:
					self.image = pygame.transform.scale(self.image, (int(math.fabs(int(self.otherscale*(self.parent.scale*5*masterscale/self.parent.origheight))+1)), int(math.fabs(self.scale))))
				except:
					self.image = pygame.transform.scale(self.image, (50, math.fabs(self.scale))) #pygame crash if you scale too big
				
				self.image.fill((self.parent.rcolor, self.parent.gcolor, self.parent.bcolor), None)	
				self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))
			
			
			
		
			self.rect = self.image.get_rect()
			self.rect.center = scrpos(self.x,self.y)
			if self.framecount < self.maxframe:
				self.framecount += 1
			if self.framecount == self.maxframe:
				if self.parent.hookhitcount == 1:
					hookfire.stop()
					hookhit.play(distance(self, man))
					self.parent.hookhitcount =2
				if self.parent.hookhitcount ==0:
					self.parent.hookhitcount=1

				
			self.scale /=masterscale	
		else:
			self.parent.hookhitcount =0
			self.firingstate = 0
			self.x=self.parent.x
			self.y=self.parent.y#ie inside the parent
			self.image = pygame.transform.scale(self.original, (0, 0))#ie disappear
			self.rect = self.image.get_rect()
			self.rect.center = scrpos(self.x,self.y)


class Laser(A):
	def update(self):
		if self.on == 1 and self.onlast == 0:
			
			self.start = Ob()
			if self.lasercount == 0:
				laserfire.play(distance(self, focused))
				self.start.x = self.parent.x; self.start.y = self.parent.y
				self.tmpangle = math.pi + self.parent.gun.angle
				self.secondfirecount = 0
				self.reachedi = 0
			if self.lasercount == 1:#for bounces
				self.start.x = self.parent.gun2.laser0.rememberedx; self.start.y = self.parent.gun2.laser0.rememberedy
				if (self.parent.gun2.laser0.tmpangle) % (2*math.pi)<= math.pi + math.pi /4 and (self.parent.gun2.laser0.tmpangle) % (2*math.pi)>=  math.pi - math.pi /4:
					self.tmpangle =  math.pi - (self.parent.gun2.laser0.tmpangle - 0)
					#print "top"
				elif (math.pi + self.parent.gun2.laser0.tmpangle) % (2*math.pi)<= math.pi/2 + math.pi /4 and (math.pi + self.parent.gun2.laser0.tmpangle) % (2*math.pi) >= math.pi/2 - math.pi /4:
					 self.tmpangle =  math.pi + 3/2*math.pi + (3*math.pi /2 - self.parent.gun2.laser0.tmpangle)
					# print "left"
				elif (math.pi + self.parent.gun2.laser0.tmpangle) % (2*math.pi)<= math.pi + math.pi /4 and (math.pi + self.parent.gun2.laser0.tmpangle) % (2*math.pi) >= math.pi - math.pi /4:
					self.tmpangle = math.pi + math.pi + (math.pi - self.parent.gun2.laser0.tmpangle )
					#print "bottom"
				elif (math.pi + self.parent.gun2.laser0.tmpangle) % (2*math.pi) <= 3/2*math.pi + math.pi /4 and (math.pi + self.parent.gun2.laser0.tmpangle) % (2*math.pi) >= 3/2*math.pi - math.pi /4:
					#print "right"
					self.tmpangle = 3/2*math.pi - self.parent.gun2.laser0.tmpangle + math.pi/2
				else:
					#print (self.parent.gun2.laser0.tmpangle) % (2*math.pi)
					print "this shoudnt have happened"
					self.tmpangle = math.pi / 2
									
			for i in range(0, int(70*self.parent.scale/32*masterscale * 1.5)):
	
				self.weregoing = 0
				self.framecount = 1
				(self.lasercross.x, self.lasercross.y) = (self.start.x + math.sin(self.tmpangle)*i*5, self.start.y +math.cos(self.tmpangle)*i*5)
				self.reachedi = i
				
				if isblack(*scrpos(self.lasercross.x, self.lasercross.y)):
					break
					
				else:
					self.rememberedx, self.rememberedy = self.lasercross.x, self.lasercross.y
					
			self.on = 0
		self.onlast = self.on
	
		self.maxframe = 3

		if (self.weregoing == 1 or (self.weregoing == 0 and self.framecount < self.maxframe + 1)):# and self.pressingbutton1 == 1:

			self.scale *=masterscale
			self.firingstate = 1
			self.endx = self.start.x + (self.framecount/self.maxframe)*(self.lasercross.x - self.start.x)
			self.endy = self.start.y + (self.framecount/self.maxframe)*(self.lasercross.y - self.start.y) 
			
			self.x = (self.endx + self.start.x)/2
			self.y = (self.endy + self.start.y)/2
			self.scale = distance2(self.endx, self.endy, self.start.x, self.start.y)
			self.angle = findangle(self.start.x, self.start.y, self.endx, self.endy)#same as if used cross coordinates
			

			if self.framecount == self.maxframe:
				if self.lasercount == 0:
					if self.secondfirecount == 0:
						if isblack(*scrpos(self.endx, self.endy)):
							self.parent.gun2.laser1.on = 1
							self.secondfirecount = 1
			if self.framecount < self.maxframe +1:
				self.framecount += 1
			else:#can never get here? fixme#we must be able to, as it runs this bit, but how?
				hitter = self.parent
				isblack(*scrpos(self.endx, self.endy)) #should be true#just here to get isblackobject output
				if isblackobject in bots or isblackobject in opponents:
					if not [isblackobject, self.parent] in listofdeaths: #only add new deaths.
						listofdeaths.append([isblackobject, self.parent])

			
			if self.redraw():
				self.image = self.original
				self.image = pygame.transform.scale(self.image, (int(self.parent.scale/6), int(math.fabs(self.scale))))
	
				self.image.fill((self.parent.rcolor, self.parent.gcolor, self.parent.bcolor), None)	
				self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))
		
				self.rect = self.image.get_rect()
				self.rect.center = scrpos(self.x,self.y)

			self.scale /=masterscale	
		else:
			self.parent.hookhitcount =0
			self.firingstate = 0
			self.x=self.parent.x
			self.y=self.parent.y#ie inside the parent
			self.image = pygame.transform.scale(self.original, (0, 0))#ie disappear
			self.rect = self.image.get_rect()
			self.rect.center = scrpos(self.x,self.y)
			
class Flame(A):
	def update(self):
		if self.on == 1:
			self.weregoing = 1
			
			self.pressingbutton1 = 1
		else:
			self.pressingbutton1 = 0
			self.weregoing = 0
			self.framecount = 1
			#saber.stop()

		if (self.weregoing == 1 or (self.weregoing == 0 and self.framecount < self.maxframe)) and self.pressingbutton1 == 1:
			if whilecount % 5 == 0:
				saber.play(distance(focused, self))
		
			tmpangle = math.pi + self.parent.gun3.angle#findangle(man.x, man.y, *realpos(mpx, mpy))#*to turn into tuple
			for i in range(0, int(70*self.parent.scale/32*masterscale /2)):

				(self.parent.gun3.flamecross.x, self.parent.gun3.flamecross.y) = (self.parent.x + math.sin(tmpangle)*i*5, self.parent.y +math.cos(tmpangle)*i*5)

				if isblack(*scrpos(self.parent.x + math.sin(tmpangle)*i*5, self.parent.y +math.cos(tmpangle)*i*5)):
					#saberhit.play(distance(focused,self))#doesnt work nicely fixme
					break		

			self.scale *=masterscale
			self.firingstate = 1
			self.endx = self.parent.x + (self.framecount/self.maxframe)*(self.parent.gun3.flamecross.x - self.parent.x)
			self.endy = self.parent.y + (self.framecount/self.maxframe)*(self.parent.gun3.flamecross.y - self.parent.y)
			
			self.x = (self.endx + self.parent.x)/2
			self.y = (self.endy + self.parent.y)/2
			self.scale = distance2(self.endx, self.endy, self.parent.x, self.parent.y)
			self.angle = findangle(self.parent.x, self.parent.y, self.endx, self.endy)#same as if used cross coordinates
	
	
			if self.framecount < self.maxframe:
				self.framecount += 1
			else:
				hitter = self.parent
				isblack(*scrpos(self.endx, self.endy)) #should be true#just here to get isblackobject output
				if isblackobject in bots or isblackobject in opponents:
					if not [isblackobject, self.parent] in listofdeaths: #only add new deaths.
						listofdeaths.append([isblackobject, self.parent])			

			
			if self.redraw():
				self.image = self.original
				self.image = pygame.transform.scale(self.image, (int(self.parent.scale/6*1.5), int(math.fabs(self.scale))))

				
				self.image.fill((self.parent.rcolor, self.parent.gcolor, self.parent.bcolor), None)	
				self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))
		
			self.rect = self.image.get_rect()
			self.rect.center = scrpos(self.x,self.y)
				
			self.scale /=masterscale	
		else:
			self.parent.hookhitcount =0
			self.firingstate = 0
			self.x=self.parent.x
			self.y=self.parent.y#ie inside the parent
			self.image = pygame.transform.scale(self.original, (0, 0))#ie disappear
			self.rect = self.image.get_rect()
			self.rect.center = scrpos(self.x,self.y)	

#
class Otherplayer(Man):
	def update(self): 
		self.scale *=masterscale#could cause problems with the two threads, due to setting scale somewhere in the middle....
		
		self.updatecolor()
		
		if self.redraw():
			self.image = self.original
			try:
				pygame.draw.circle(self.image, (self.rcolor, self.gcolor, self.bcolor), (int(self.origwidth/2), int(self.origheight/2)), int(self.origwidth*0.4 + 1), 0)
			except:
				None
				#dont understnad why this is needed
			self.image = pygame.transform.scale(self.image, (int(self.scale), int(self.height()))) #sadly locks everyhting to being squares
		
		if self.timesinceupdate != 0: #incase the server is slow
			self.x += self.xv*self.t
			self.y += self.yv*self.t
		self.timesinceupdate += 1
		self.rect = self.image.get_rect()
		self.rect.center = scrpos(self.x,self.y)#
		self.scale /=masterscale



pressinga=0
pressingd=0
pressingbutton3=0
tmpcount=0
goingdownforquit=0
fullscreen = 0	

def readinput(events):
	global screen
	global fullscreen
	global focused
	man = focused
	
	global mpx, mpy
	global pressinga
	global pressingd
	global pressingbutton3
	global tmpcount
	global goingdownforquit
	global hitter
	hitter = man
	(mpx, mpy) = pygame.mouse.get_pos()
	if man.scale < 5:#provides minimum scaling
		man.scaleincrement = 0
	for event in events:
		if event.type == pygame.VIDEORESIZE:
			global smallresolution
			smallresolution = event.size
			screen = pygame.display.set_mode(smallresolution, pygame.RESIZABLE)#event.size gives the size of the resized window as a rect
		if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q) or (event.type == KEYDOWN and event.key == K_ESCAPE):
			goingdownforquit=1 #signal to the other thread
			time.sleep(1) #wait for the other thread to send the quit message to the server
			sys.exit() #then really close
		if event.type == KEYDOWN:
			if event.key == K_f:
				if fullscreen == 0:
					fullscreen = 1
					screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
				else:
					fullscreen = 0
					screen = pygame.display.set_mode(smallresolution, pygame.RESIZABLE)
			if event.key == K_r: #reset key
				for flag in man.flagbag:
					#print "flag dropped"
					man.flagbag.remove(flag)
					SendData(client_server_sock,["update","FR",{"name":flag.parent.name}])
					trash = ReceiveData(client_server_sock)				
				gotlife.play(0)
				man.x = man.init.x
				man.y = man.init.y
				man.xv = 0
				man.modifiedx = 1
				man.modifiedy = 1
				man.b.modifiedx = 1
				man.b.modifiedy = 1
				
				for item in man.gunlist[0][1]:
					item.hashit=1
				
				man.gun1.b.hashit=1
				
				man.yv = 0
				man.scale = 30
				man.hashitr = 0
				man.hashitl = 0
				man.hashitb = 0
				man.hashitt = 0
				pressingbutton3 = 0
				man.hook.pressingbutton3 = 0
				man.jumpcount = 0
			
				if blurring:
					global blur
					blur = 1
			if event.key == K_w:
				man.scaleincrement = +5
				man.modifiedscale = 1
			elif event.key == K_s:
				if man.scale > 5:
					man.scaleincrement = -5
				man.modifiedscale = 1
			elif event.key == K_a:
				pressinga=1
			elif event.key == K_d:
				pressingd=1
			elif event.key == K_SPACE:
				if man.jumpcount == 0 or man.jumpcount ==1:
					jump.play(0)
					man.modifiedy = 1
					if man.yvc >=0: #ie going down#to allow double jumping
						man.yv = -220*(man.scale/100)*masterscale
					else:
						man.yv += -220*(man.scale/100)*masterscale
					man.jumpcount += 1
		elif event.type == MOUSEBUTTONDOWN:
			if event.button == 4:
				if man is ultimateman:
					changegun.play(0)
					man.scroll += 1
					man.gun = man.gunlist[man.scroll % len(man.gunlist)][0]
					man.b = man.gunlist[man.scroll % len(man.gunlist)][1][0]
					dspritelist[dspritelist.index(man.gunlist[(man.scroll - 1)% len(man.gunlist)][0])] = man.gunlist[man.scroll % len(man.gunlist)][0]
			if event.button == 5:
				if man is ultimateman:
					changegun.play(0)
					man.scroll -= 1
					man.gun = man.gunlist[man.scroll % len(man.gunlist)][0]
					man.b = man.gunlist[man.scroll % len(man.gunlist)][1][0]
					dspritelist[dspritelist.index(man.gunlist[(man.scroll + 1)% len(man.gunlist)][0])] = man.gunlist[man.scroll % len(man.gunlist)][0]
			if event.button == 1:
			
				if focused == ultimateman.clone:#needs to above where it is set to be man.clone
					cursor.parent = ultimateman
					cursor.scalel = 0#hack to make colors update
					explode.play(0)
					ultimateman.clone.scaleincrement = 0
					ultimateman.clone.state = 0
					
					ultimateman.clone.hook.weregoing = 0
					ultimateman.clone.hook.pressingbutton3 = 0
					for player in opponents + home:
						if distance(player, ultimateman.clone) <= 80: #so no advantage to scaling
							if not [player, ultimateman] in listofdeaths: #only add new deaths.
								listofdeaths.append([player, ultimateman])			
					dspritelist.remove(ultimateman.clone)
					dspritelist.remove(ultimateman.clone.hook)
					focused = ultimateman
					gunformotiontracking.parent = focused
					
					
				if man is ultimateman:				
					if man.scroll % len(man.gunlist) == 0:
						for item in man.gunlist[0][1]:
							man.b = item
							if man.b.hashit == 1:#make sure in sync
						
								man.b.explodecount = 0
								man.b.explosive = 0
								pistolfire.play(0)
								man.b.hashit = 0
								man.b.angle = man.gun.angle
								man.b.x = int(man.x)
								man.b.y = int(man.y)
								man.b.xv = int(500*-math.sin(man.gun.angle)*(man.scale/100))*masterscale + man.xvlast
								man.b.yv = int(500*-math.cos(man.gun.angle)*(man.scale/100))*masterscale + man.yvlast
								man.b.modifiedx = 1
								man.b.modifiedy = 1
								break
						
						
					if man.scroll % len(man.gunlist) == 1:
						if man.b.hashit == 1:#make sure in sync
							man.b.explodecount = 0
							man.b.explosive = 1
							fire.play(0)
							man.b.hashit = 0
							man.b.angle = man.gun.angle
							man.b.x = int(man.x)
							man.b.y = int(man.y)
							man.b.xv = int(200*-math.sin(man.gun.angle)*(man.scale/100))*masterscale + man.xvlast
							man.b.yv = int(200*-math.cos(man.gun.angle)*(man.scale/100))*masterscale + man.yvlast
							man.b.modifiedx = 1
							man.b.modifiedy = 1
					if man.scroll % len(man.gunlist) == 2:
						man.gunlist[2][0].laser0.on = 1
					if man.scroll % len(man.gunlist) == 3:
						man.gunlist[3][0].flame.on = 1
					
					
					
					if man.scroll % len(man.gunlist) == 4:
						clone.play(0)
						cursor.parent = ultimateman.clone
						cursor.scalel = 0#hack to make colors update
						dspritelist.append(man.clone)
						dspritelist.append(man.clone.hook)
						man.clone.x, man.clone.y = man.x, man.y
						man.clone.scale = man.scale
						man.clone.xv = 0; man.clone.yv = 0
						man.clone.modifiedx = 1; man.clone.modifiedy = 1
						man.clone.state = 1
						man.hook.weregoing = 0
						man.hook.pressingbutton3 = 0
						man.scaleincrement = 0
						gunformotiontracking.parent = man.clone
						focused = man.clone					
			if event.button == 3:
				pressingbutton3=1
				man.hook.pressingbutton3 = 1
		elif event.type == KEYUP:
			if event.key == K_w:
				man.scaleincrement = 0
				man.modifiedscale = 0
			elif event.key == K_s:
				man.scaleincrement = 0
				man.modifiedscale = 0
			elif event.key == K_a:
				pressinga=0
			elif event.key == K_d:
				None
				pressingd=0
		elif event.type == MOUSEBUTTONUP:
			if event.button == 3:
				pressingbutton3=0
				man.hook.pressingbutton3 = 0
				
			if event.button == 1:
				if focused is ultimateman:
					focused.gunlist[3][0].flame.on = 0#cant just check man, but man only gets updated at top of this routine
	if pressingbutton3 == 1:
		if tmpcount == 0: #set it up, one time only, but on every click
			tmpangle = findangle(man.x, man.y, *realpos(mpx, mpy))#*to turn into tuple
			for i in range(0, int(70*man.scale/32*masterscale)):
				hookfire.play(0)
				if isblack(*scrpos(man.x + math.sin(tmpangle)*i*5, man.y +math.cos(tmpangle)*i*5)):
					man.hook.weregoing = 1
					
					(man.cross.x, man.cross.y) = (man.x + math.sin(tmpangle)*i*5, man.y +math.cos(tmpangle)*i*5)
					man.cross.hookedobject = isblackobject #this is useful is the object moves, so the hook can stay stuck to the relative part
					man.cross.relativex = man.cross.x - isblackobject.x
					man.cross.relativey = man.cross.y - isblackobject.y
					(man.cross.x, man.cross.y) = (man.cross.relativex + man.cross.hookedobject.x, man.cross.relativey + man.cross.hookedobject.y)
					break
				else:
					man.hook.weregoing = 0
					(man.cross.x, man.cross.y) = (man.x + math.sin(tmpangle)*i*5, man.y +math.cos(tmpangle)*i*5)
					
			
			tmpcount = 1 #so we dont redo the setup
		if man.hook.weregoing == 1 and man.hook.framecount == man.maxframe: #check this every click, every fraction of hold, but only act on good clikcs
			(man.cross.x, man.cross.y) = (man.cross.relativex + man.cross.hookedobject.x, man.cross.relativey + man.cross.hookedobject.y) #in case hookedobject has moved
			man.hook.distance = distance(man, man.cross)
			man.yf +=  0.4*man.hook.distance*math.cos(man.hook.angle)*(man.scale/100)*masterscale #not perfect, should be hookdistance-man.width. ie hook from closest side of man, not from center
			man.xf += 0.4*man.hook.distance*math.sin(man.hook.angle)*(man.scale/100)*masterscale

	else: #ie stopped pressing button3
		hookfire.stop()
		tmpcount = 0 #so allow to go back into the setup
		man.hook.framecount = 1
	if pressinga == 1:
		if man.xvc >=0:#moving right
			man.xf += -200*(man.scale/100)*masterscale
		else:#moving left
			if man.xvc >= -10.0*(man.scale/100)*masterscale:
				man.xf += -200*(man.scale/100)*masterscale
			else: #maximum speed
				man.xf += -20*(man.scale/100)*masterscale
	if pressingd == 1:
		if man.xvc <=0:#moving left		
			man.xf += 200*(man.scale/100)*masterscale
		else:#moving right
			if man.xvc <= 10.0*(man.scale/100)*masterscale:
				man.xf += 200*(man.scale/100)*masterscale
			else:
				man.xf += 20*(man.scale/100)*masterscale





def related(a,b):
	try:
		if a is b or a is b.parent or b is a.parent:
			return True
	except:
		None
	
	try:		
		if a.name == b.name and a.name != 0 :#bot colliding with the network image of itself
			return True
	except:
		None
	
	try:	
		if b.parent.name == a.name:#to stop bullet hitting networked image of self (bot)
			return True
	except:
		None
		
	try:	
		#maybe dont want bot colliding with man or opponent
		if b in bots and a in players:
			return True
	except:
		None
		
	return False


listofdeaths = []

hitter = 0
isblackobject = 0
def isblack(x, y):
	try:
		if hitter.title == "bullet" and hitter.parent in home:#local players bullets
			firing = 1
		else:
			firing = 0
	except:
		firing = 0

	by = hitter
			
	x = int(x); y = int(y)
	global isblackobject
	(rx, ry) = realpos(x,y) #needs top left to be at 0,0 to work
	for item in grounds:
		if not related(item, by):	
			#fixme, for speed, should only do perpixel test on back in grounds, for everything else, just do rectcollide test
			if item.rect.collidepoint(x,y): #makes sure that the later pixel test is really on the image
				(imagex,imagey)=(int((item.origwidth/item.width())*(rx - realpos2(item.rect.left, "x"))), int((item.origheight/item.height())*(ry - realpos2(item.rect.top, "y")))) #gets coords on image, relative to image

				try: #i cant work out why, but sometimes the rect.collidepoint test doesnt give me what i expect so i still put this inside a try test
					#if not item.image.get_at((imagex , imagey)) == (255, 255, 255, 255): #the test to use if no array but just want to test image
					#if item.array[int(imagex)][int(imagey)] != 0:
					if item.array[int(imagex)][int(imagey)] != 16777215: #isnt white			
					#if not item.array[int(imagex)][int(imagey)] == [255, 255, 255]:
						if firing == 1:
							if item in opponents or item is man or item in bots: #stuff abut the shooting switch
								if not [item, hitter.parent] in listofdeaths: #only add new deaths.
									listofdeaths.append([item, hitter.parent]) #not really appropriate place in a test for an action to take place#needs parent as it is a bullet 								
						isblackobject = item
						return True #first true deserves a return
				except:
					return False
	return False #if youve got through it all without a return
	
	
def destroy(x, y, self):
	for item in grounds:
		if not item in opponents and not item is man and not item in bots:
			(imagex,imagey)=(int((item.origwidth/item.width())*(x - realpos2(item.rect.left, "x"))), int((item.origheight/item.height())*(y - realpos2(item.rect.top, "y"))))
			
				
			#valuesdone = []#this method you stop hashing lines#make it global if you want it to be perfect, but it is slow
			for i in range(int(imagex -7*self.parent.scale/30), int(imagex +7*self.parent.scale/30)):
				for j in range(int(imagey -7*self.parent.scale/30), int(imagey +7*self.parent.scale/30)):
					try:
						if distance2(imagex, imagey, i, j) <= 7*self.parent.scale/30:
							if item.array[i][j] != 16777215:
								item.array[i][j] = 16777215
								for k in range(int(-(item.front.width()/item.origwidth)/2), int((item.front.width()/item.origwidth)/2)):
									for l in range(int(-(item.front.height()/item.origheight/2)), int(item.front.height()/item.origheight/2)):
										for imageq in [item.front.image1, item.front.image3]:
											if imageq == item.front.image3 and not blurring:#image3 being the blur layer
												None#little hacky to speed up when not blurring
											else:
												imageq.lock()
												try:
													y = i*item.front.width()/item.origwidth + k
													z = j*item.front.height()/item.origheight+ l
													r,g,b,a = imageq.get_at((int(y) ,int(z)))
													imageq.set_at((int(y) ,int(z)), (r/1.5,g/1.5,b/1.5))#make darker is
												except:
													None
												imageq.unlock()
					except:
						None
					


numberofplayers = 1
scoreaverage = 0
scores = [0]
def dealwithdata():
	global dspritelist
	global blur
	botcontinue = 0
	
	global scoreaverage; global numberofplayers; global scores; global whilecount
	numberofplayers = len(Chat)
	
	
	scoretotal = 0
	for c in Chat:
		scoretotal += Chat[c]["score"]
	scoreaverage = scoretotal/numberofplayers
	
	scores = []
	for c in Chat:
		scores.append(Chat[c]["score"])
		
	for c in Chat:
		for item in home:#fixme rename the bot2
			if botcontinue == 0:
				if c == item.name:#stuff for me
					botcontinue = 1
					#if c[8][1] == "r":
					#	SendData(client_server_sock,["update","FR",(name, "empty"), (man.init.x, man.init.y)])
			
					flagowner = 0
					for opponent2 in opponents +bots + [man]:
						if not opponent2 is item: #not checking itself#unecessary
							if opponent2.name == Chat[c]["flag"]["owner"]:
								item.flag.holder = opponent2
								flagowner = 1
								item.flag.flagtaken = 1
					if flagowner == 0:
						None
						item.flag.holder = 0		
						item.flag.x = Chat[c]["flag"]["current"][0]
						item.flag.y = Chat[c]["flag"]["current"][1]
						item.flag.flagtaken = 0		
			
					if Chat[c]["health"] < item.lasthealth:
						item.scalel = 0 #little hack to make colors update
						injure.play(0)
						
						if blurring:
							if item is man:
								#front.blur = 1
								blur = 1
									
					item.lasthealth = Chat[c]["health"]
			
					item.score = Chat[c]["score"]
					item.position = order(item.score, scores)	
			
					if Chat[c]["health"] == 0:#ie dead
						if item is man:
							blur = 0#hacky
						item.targetfound = 0
						#print "resetting position"
				
						for flag in item.flagbag:
							item.flagbag.remove(flag)
							SendData(client_server_sock,["update","FD",{"name":flag.parent.name, "where":[item.x, item.y]}])
							trash = ReceiveData(client_server_sock)
							#flag.flagtaken = 0
							#flag.holder = None
						item.x = item.init.x
						item.y = item.init.y
						item.xv=0
						item.yv = 0
						item.modifiedx = 1
						item.modifiedy = 1
						item.xf=0
						item.yf=0
						item.hook.weregoing = 0
						item.scale = 30
						item.b.hashit = 1
				
						item.scalel = 0 ; item.rcolorl = 0#little hack to make colors update
						
						SendData(client_server_sock,["update","*",{"name":item.name}])
						trash = ReceiveData(client_server_sock)
						gotlife.play(distance(man, item))
		
		if botcontinue == 1:
			botcontinue = 0
			continue# uncomment this will turn off seeing network image of bots#not redundant				
								
		for opponent in opponents:
			if opponent.name == c:
				opponent.scroll = Chat[c]["gun"]
				if opponent.scroll != opponent.lastscroll:
					opponent.gun = opponent.gunlist[opponent.scroll % len(opponent.gunlist)][0]
					opponent.b = opponent.gunlist[opponent.scroll % len(opponent.gunlist)][1][0]
					dspritelist[dspritelist.index(opponent.gunlist[(opponent.lastscroll)% len(opponent.gunlist)][0])] = opponent.gunlist[opponent.scroll % len(opponent.gunlist)][0]
				opponent.lastscroll = opponent.scroll
			

			
				flagowner = 0
				for opponent2 in opponents:#and man?
					if opponent2.name == Chat[c]["flag"]["owner"]:
						opponent.flag.holder = opponent2
						opponent.flag.flagtaken = 1
						flagowner = 1
				
				if flagowner == 0:
					if name == Chat[c]["flag"]["owner"]:
						opponent.flag.holder = man
						opponent.flag.flagtaken = 1
						flagowner = 1	
						
				if flagowner == 0:
					opponent.flag.holder = 0
					opponent.flag.x = Chat[c]["flag"]["current"][0]
					opponent.flag.y = Chat[c]["flag"]["current"][1]
					opponent.flag.flagtaken = 0
				
				opponent.score = Chat[c]["score"]
				opponent.position = order(opponent.score, scores)	
				if Chat[c]["health"] < opponent.lasthealth:
					injure.play(distance(man, opponent))
				
				
				if Chat[c]["health"] > opponent.lasthealth:
					gotlife.play(distance(man, opponent))
					
				opponent.lasthealth = Chat[c]["health"]	
				

				
				opponent.scale=Chat[c]["scale"]
				try:
					if opponent.scale != opponent.lastscale:
						if whilecount % 2 == 0:# and 1 == 2:
								opponent.sound.stop()#probably should have the sound belonging to the opponent
								for i in range(len(opponent.sound.array)):
									#print i
									#print array[i]
									opponent.sound.array[i][0] = int(4000*math.sin(i/220*2*math.pi/opponent.scale*240))
									opponent.sound.array[i][1] = opponent.sound.array[i][0]
								#print 1/220*2*math.pi/man.scale*120	
				
								opponent.sound.setArray()
								opponent.sound.play(distance(opponent, man))
				except:
					None				
				opponent.lastscale = opponent.scale								
				
				opponent.xv=Chat[c]["velocity"]["man"][0]
				opponent.yv=Chat[c]["velocity"]["man"][1]
				
				opponent.x=Chat[c]["position"]["man"][0]
				opponent.y=Chat[c]["position"]["man"][1]				
				
				opponent.timesinceupdate = 0
				
				if Chat[c]["clonestate"] == 0:
					if (Chat[c]["velocity"]["bullet"][0] != 0 or Chat[c]["velocity"]["bullet"][1] != 0) and opponent.b.hashit == 1:#send out bullet
						fire.play(distance(man, opponent))

						if opponent.b.hashit == 1:
							opponent.b.hashit = 0
							opponent.b.x=Chat[c]["position"]["bullet"][0]
							opponent.b.y=Chat[c]["position"]["bullet"][1]
							opponent.b.xv=Chat[c]["velocity"]["bullet"][0]
							opponent.b.yv=Chat[c]["velocity"]["bullet"][1]
							opponent.b.modifiedx = 1
							opponent.b.modifiedy = 1
							opponent.b.explosive = Chat[c]["explosive"]
					#			break
						
				
				if Chat[c]["velocity"]["bullet"][0] == 0 and Chat[c]["velocity"]["bullet"][1] == 0: #it must be back
					None
					opponent.b.hashit = 1 # should cause a place reset
				
				opponent.gun.angle = Chat[c]["angle"]
				if Chat[c]["hook"] == 1:
					hookfire.play(distance(man, opponent))
					opponent.hook.weregoing = 1 #
					opponent.hook.pressingbutton3 = 1
				else: # ieit is a "-"
					opponent.hook.weregoing = 0
					opponent.hook.framecount = 1
					opponent.hook.pressingbutton3 = 0
					
				opponent.cross.x = Chat[c]["position"]["hook"][0]
				opponent.cross.y = Chat[c]["position"]["hook"][1]
					
				if Chat[c]["clonestate"] == 1:
					if not opponent.clone in dspritelist:
						dspritelist.append(opponent.clone)
						dspritelist.append(opponent.clone.hook)
					opponent.clone.x, opponent.clone.y = Chat[c]["position"]["clone"][0], Chat[c]["position"]["clone"][1]
					opponent.clone.scale = Chat[c]["clonescale"]
					
					
					if Chat[c]["clonehook"] == 1:
						hookfire.play(distance(focused, opponent.clone))
						opponent.clone.hook.weregoing = 1 #
						opponent.clone.hook.pressingbutton3 = 1
					else: # ieit is a "-"
						opponent.clone.hook.weregoing = 0
						opponent.clone.hook.framecount = 1
						opponent.clone.hook.pressingbutton3 = 0					
					

					
					opponent.hook.weregoing = 0
				else:
					if opponent.clone in dspritelist:
						dspritelist.remove(opponent.clone)
						dspritelist.remove(opponent.clone.hook)	
						
				opponent.clone.cross.x = Chat[c]["position"]["clonehook"][0]
				opponent.clone.cross.y = Chat[c]["position"]["clonehook"][1]		
				
				opponent.gun3.flame.on = Chat[c]["flame"]
				
				opponent.gun2.laser0.on = Chat[c]["laser"]										
				
				break #as we have found one to update
			if opponent.name == 0:#need to create another opponent
				opponent.name = c
				opponent.lastscale = opponent.scale
				opponent.timesinceupdate = 0		
				grounds.append(opponent) #want this first;want test for movable object to hook onto to hook the person before the gun and bullet if possible
				opponent.array=pygame.surfarray.array2d(opponent.image)#could move to where opponent created
				opponent.gun = opponent.gunlist[0][0]#redundant fixme
				opponent.b = opponent.gunlist[0][1][0]
				
				dspritelist += [opponent.flag, opponent.hook]
				for i in range(len(opponent.gunlist)):
					if i != 4:#remove the clone
						for item in opponent.gunlist[i][1]:
							dspritelist.append(item) #ie the bullets
				dspritelist += [opponent.gunlist[0][0]]
				dspritelist += [opponent]

				#####################

				global spritelist
				spritelist += [opponent, opponent.flag] 
				spritelist += [opponent.hook, opponent.cross]

				for item in opponent.gunlist:
					spritelist.append(item[0])#ie the guns

				for i in range(len(opponent.gunlist)):
					for item in opponent.gunlist[i][1]:
						spritelist.append(item) #ie the bullets

				break #as we have found one to set
				
		continue #redundant
	
	for ground in grounds:#to need to remove an opponent
		if ground in opponents: #this comes up with supposedly alive opponents (ie drawn opponents)
			found=0 #because i dont know how to break out of 2 nested loops
			for c in Chat:
				if c == ground.name:
					found=1
					break
			if found==0:
				ground.name= 0
				grounds.remove(ground)
				

				dspritelist.remove(ground.flag)
				dspritelist.remove(ground.hook)
				for i in range(len(ground.gunlist)):
					if i != 4:#remove the clone
						for item in ground.gunlist[i][1]:
							dspritelist.remove(item) #ie the bullets
				dspritelist.remove(ground.gunlist[ground.scroll % len(ground.gunlist)][0])
				dspritelist.remove(ground)

				#####################

				#global spritelist
				spritelist.remove(ground)
				spritelist.remove(ground.flag)
				spritelist.remove(ground.hook)
				spritelist.remove(ground.cross)

				for item in ground.gunlist:
					spritelist.remove(item[0])#ie the guns

				for i in range(len(ground.gunlist)):
					for item in ground.gunlist[i][1]:
						spritelist.remove(item) #ie the bullets							
		
	return

captured = 0
returned = 0
def transferdata():
	global captured
	global returned
	global Chat
	
	for item in bots+[man]:#sends all the data to the server
		SendData(client_server_sock,["update","=", {"name":item.name, "position":{"man":[int(item.x), int(item.y)], "bullet":[int(item.b.x), int(item.b.y)], "hook":[int(item.cross.x), int(item.cross.y)], "clone":[int(item.clone.x), int(item.clone.y)], "clonehook":[int(item.clone.cross.x), int(item.clone.cross.y)]}, "scale":int(item.scale), "clonescale":int(item.clone.scale), "velocity":{"man":[int(item.xvlast), int(item.yvlast)], "bullet":[int(item.b.xvlast), int(item.b.yvlast)]}, "angle":item.gun.angle, "explosive":item.b.explosive, "clonestate":item.clone.state, "gun":item.scroll, "flame":item.gun3.flame.on, "laser":item.gun2.laser0.on, "hook":item.hook.firingstate, "clonehook": item.clone.hook.firingstate}])#send your position
		Chat = ReceiveData(client_server_sock) #get data from server	
	
	
	dealwithdata() #create a new ground setup basically
	
	for item in listofdeaths: #process the deaths from the isblack function
		SendData(client_server_sock,["update","!",{"name":item[0].name, "killerscale":item[1].scale, "killername":item[1].name}])#"-"#will be ignored by server for addding score
		trash = ReceiveData(client_server_sock)
		listofdeaths.remove(item)
	
	for heartpiece in hearts: #not really the right place for this to go in the data transfer thread, but it has the nice use of telling me when this thread has died, as the hearts dont change state

	
		if heartpiece.timesincelasthealth < 900 :
			heartpiece.timesincelasthealth +=1
			heartpiece.catchcount = 0
		else:
			if heartpiece.fullstate == 0:
				heartpiece.image3 = heartpiece.image
				heartpiece.image = heartpiece.image2
				heartpiece.image2 = heartpiece.image3
				heartpiece.fullstate=1
			if heartpiece.fullstate == 1:
				for item in home:		
					if distance(item, heartpiece) <= heartpiece.width()/2 + item.scale/2:
						if heartpiece.catchcount == 0:
							gotlife.play(0)
							if item is man:
								global blur
								blur = 0#hacky
							heartpiece.catchcount = 1
						heartpiece.image3 = heartpiece.image#doesnt work with scaling, shoudl replace original#fixme
						heartpiece.image = heartpiece.image2
						heartpiece.image2 = heartpiece.image3
						timesincelasthealth = 0
						SendData(client_server_sock,["update","^",{"name": item.name}])#should be based on scale fixme
						trash = ReceiveData(client_server_sock)
						heartpiece.fullstate = 0
						heartpiece.timesincelasthealth = 0
	for player in home:#ie man and all bots
		if player.captured == 1:
			amountcaptured = 0
			for flag in player.flagbag:
				if amountcaptured == 0:
					#returnedflag.play(distance(player, focused))#soudns awful
					amountcaptured = 1
				player.flagbag.remove(flag)
				SendData(client_server_sock,["update","FC",{"name":flag.parent.name, "by":player.name}])
				trash = ReceiveData(client_server_sock)
			player.captured = 0
		if player.returned == 1:
			SendData(client_server_sock,["update","FR",{"name":player.name}])
			trash = ReceiveData(client_server_sock)
			player.returned = 0
		for item in player.capturedlist:	
			SendData(client_server_sock,["update","FO",{"name":item, "taker":player.name}])
			trash = ReceiveData(client_server_sock)
			player.capturedlist.remove(item)					
			 
	
def masstransfer():
	#try:
		while 1:
			clock.tick(20)
			#clock.tick(60) #maybe there should be some sort of ticking, but just thought try as fast as possible
			#time.sleep(0.016)
			if goingdownforquit == 1:
				for homer in home:
					for flag in homer.flagbag:
						SendData(client_server_sock,["update","FD",{"name":flag.parent.name, "where":[homer.x, homer.y]}])#fixme could go wrong if someone is freefalling when they legitimately quit
						trash = ReceiveData(client_server_sock)
				
				#SendData(client_server_sock,["update","-",(man.name, "empty")]) #why is this necesary!, put it here instead of other thread
				#trash = ReceiveData(client_server_sock)
				
				for item in home:
					SendData(client_server_sock,["update","-",{"name":item.name}])
					trash = ReceiveData(client_server_sock)
				pygame.quit()
				sys.exit()
			else:
				transferdata()
	#except:
	#	#print "SOMETHING HAS GONE HORRIBLY HORRIBLY WRONG, WILL TRY RECONNECTING" #fix me. what to do when the thread dies?
	#	#client_server_sock.disconnect(("2tt.dyndns.org",6317))
	#	#connect()
	#	masstransfer()#so if something goes wrong, it will just start it up again..... #except it doesnt work




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
		#1/0
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

	os.system("unset SDL_VIDEO_CENTERED")#sadly doesnt work (dont want it to be centered)
	#os.environ["SDL_VIDEO_CENTERED"] = "" #hacky#dont need it to be centered from now on
	#area = screen.get_rect()
	pygame.display.set_caption(game)

	pygame.mouse.set_pos(pygame.display.get_surface().get_rect().width/2, pygame.display.get_surface().get_rect().height/2) #thanks pymike
	pygame.mouse.set_visible(0)
	#pygame.event.set_grab(1) #grab the mouse

	clock = pygame.time.Clock()
		
	
	


if __name__ == "__main__":
	#----------------------------------------------------------------------------------------#

	##main start####
	game = "coffeeworlds"



	connect()	
	Chat = []

	whilecount = 0



	namecount = 0
	SendData(client_server_sock,["update","nomessage"])#empty unused message just to connect
	Chat = ReceiveData(client_server_sock) #get data from server
	while (namecount == 0) or (namecount == 1 and (name in namelist or name == "-" or name == "returnable")):
		cont = True
	
		namelist = []
		#for i in range(0, len(Chat)):
		#	namelist.append(Chat[i]["name"])
		for line in Chat:
			namelist.append(line)		
		while cont:
			if namecount == 0:
				name = raw_input("What is your screen name?  ")
			else:
				name = raw_input("Sorry, name already taken. Please enter a new one: ")
			namecount = 1
			for char in name:
				if char != " ":
					cont = False
					break

	setup_pygame()
	
	
	
	
	
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

	#botson = raw_input("Bots on (experimental)? (y/N)  ")
	botson = "n"






	background = pygame.Surface(screen.get_size())
	background = background.convert()#hack. i use convert instead of convert_alpha to let me later set whole surface alpha. damn you pygame for not letting me do this when surface has per pixel alpha
	background.fill((250, 250, 250))


	explode = Sound("explode.wav")
	jump = Sound("jump.wav")
	fire = Sound("fire.wav")
	hookhit = Sound("hookhit.wav")
	hookfire = Sound("hookfire.wav")
	hitwall = Sound("hitwall.wav")
	gotlife = Sound("gotlife.wav")
	injure = Sound("injure.wav")
	changegun = Sound("changegun.wav")
	saber = Sound("saber.wav")
	pistolfire = Sound("pistolfire.wav")
	saberhit = Sound("saberhit.wav")
	laserfire = Sound("laserfire.wav")
	returnedflag = Sound("returnedflag.wav")
	pistolhit = Sound("pistolhit.wav")
	clone = Sound("clone.wav")


	#x=0
	#y=0

	blurring = True
	blur = 0
	#if blurring:
	#	blur = 1
	#else:
	#	blur = 0


	#set the map here
	scene = "3"
	if scene == "2":#hack for ease
		needsmask = 1#unless we are doing blurring, may as well leave as 1, but really depennds on whether front background is transparent, or a pattern. transparent needs mask
	else:
		needsmask = 0#hack
	front = Ground("map"+scene+"front.png")
	back = Ground("map"+scene+"back.png")

	#front.blur = 1

	front.back = back
	back.front = front

	back.scale=4800 #remember to change the scale above, for bodge test
	front.scale=back.scale
	#these are 4800,6400 for map1,map2


	man = Man("man.png")
	focused = man
	ultimateman = man
	man.scale = 30# or man.scale/6
	man.name = name
	man.title = man


	bot0 = Bot("man.png")
	bot0.scale = 50
	bot0.name = name+"bot-"

	bot1 = Bot("man.png")
	bot1.scale = 50
	bot1.name = name+"bot1"


	bot2 = Bot("man.png")
	bot2.scale = 50
	bot2.name = name+"bot2"

	bot3 = Bot("man.png")
	bot3.scale = 50
	bot3.name = name+"bot3"

	clones = []

	home = [man]
	if botson == "y":#ie bots turned on
		bots = [bot0]
	else:
		bots = []
	for bot in bots:
		bot.title = "bot"
		home.append(bot)
	
	player1= Otherplayer("man.png")
	player2= Otherplayer("man.png")
	player3= Otherplayer("man.png")
	player4= Otherplayer("man.png")
	player5= Otherplayer("man.png")
	
	
	opponents = [ player1, player2, player3, player4, player5 ]
	players = []
	for homer in home:
		players.append(homer)
	for opponent in opponents:
		players.append(opponent)


	for player in players:
		player.setGun0("gun0.png")
		player.setGun1("gun1.png")
		player.setGun2("gun2.png")
		player.setGun3("gun3.png")
		player.setGun4("gun4.png")
		#player.setBullet()
	
		player.setHook()#needed for other thread#for bots to have
		#if not player is clone:
		player.setFlag("flag.png")#just want the network version of this for the bot
		player.setCross()#for the purposes of hooking, everything needs a cross
	
		player.gun = player.gunlist[0][0]
		player.b = player.gunlist[0][1][0]
	
	
	grounds = [back, man]#had bot in, but now he is on the network so doesnt need to be on grounds
	for bot in bots:
		grounds.append(bot)
	for ground in grounds:
		ground.array=pygame.surfarray.array2d(ground.image)


	gunformotiontracking= Gun("blank.png") #hack # there is inherent circularity in the way we choose the screen center, based on the mouse position, which can only be found relative to other objects by knowing the screen center. therefore we make a dummy image (hopefully drawn at the bottom) to resolve this, by being able to reference something else
	gunformotiontracking.parent = man
	gunformotiontracking.gunnumber = 0
	#gunformotiontracking.original2, gunformotiontracking.rect2 = load_image("blank.png", None)#dont need this as not rendered


	heart0= Ground("heart.png", "heartempty.png")
	heart1= Ground("heart.png", "heartempty.png")
	heart2= Ground("heart.png", "heartempty.png")
	heart3= Ground("heart.png", "heartempty.png")
	heart4= Ground("heart.png", "heartempty.png")
	heart5= Ground("heart.png", "heartempty.png")
	heart6= Ground("heart.png", "heartempty.png")
	heart7= Ground("heart.png", "heartempty.png")
	hearts = [heart0, heart1, heart2, heart3, heart4, heart5, heart6, heart7]


	cursor = Cross("cross.png")
	cursor.title = "cursor"
	cursor.parent = man





	##start

	dspritelist = [front]
	for heart in hearts:
		dspritelist.append(heart)

	
	dspritelist += [man.flag, man.hook]
	for i in range(len(man.gunlist)):
		if i != 4:#remove the clone
			for item in man.gunlist[i][1]:
				dspritelist.append(item) #ie the bullets
	dspritelist += [man.gunlist[0][0]]
	dspritelist += [man]
	
	for bot in bots:
		dspritelist += [bot.flag]
		for i in range(len(bot.gunlist)):
			if i != 4:#removes the clone#hack
				for item in bot.gunlist[i][1]:
					dspritelist.append(item) #ie the bullets	
		dspritelist += [bot.gunlist[0][0]] 
		dspritelist += [bot]
	
	dspritelist.append(cursor)	


	###end



	####start

	spritelist = [back]
	spritelist.append(gunformotiontracking)

	spritelist += [man, man.flag] 
	spritelist += [man.hook, man.cross]

	for item in man.gunlist:
		spritelist.append(item[0])#ie the guns

	for i in range(len(man.gunlist)):
		for item in man.gunlist[i][1]:
			spritelist.append(item) #ie the bullets
		
		
		

	for bot in bots:
		spritelist += [bot, bot.flag]
	
	for bot in bots:
		for item in bot.gunlist:
			spritelist.append(item[0])#ie the guns

		for i in range(len(bot.gunlist)):
			for item in bot.gunlist[i][1]:
				spritelist.append(item) #ie the bullets	



		
		

	spritelist.append(front)
	for heart in hearts:
		spritelist.append(heart)
	
	spritelist.append(cursor)	



	###end






	#this needs to be done first to allow the findempty test to come up with REAL empty places
	#########hack
	man.fixed.x = man.x; man.fixed.y = man.y
	gunformotiontracking.xrectfixed, gunformotiontracking.yrectfixed = gunformotiontracking.rect.center


	mpx, mpy = pygame.mouse.get_pos()
	man.init.x, man.init.y = findempty()
	man.x = man.init.x; man.y = man.init.y

	man.fixed.x = man.x; man.fixed.y = man.y
	gunformotiontracking.xrectfixed, gunformotiontracking.yrectfixed = gunformotiontracking.rect.center

	for sprite in spritelist:
		sprite.update()
	for sprite in spritelist:
		sprite.update()	
	########end of hack	
	
	
	for item in home:	
		item.init.x, item.init.y = findempty()
		item.x = item.init.x; item.y = item.init.y

	for heartpiece in hearts:
		heartpiece.x, heartpiece.y = findempty()



	for player in home:
		#join the server
		SendData(client_server_sock,["update","+",{"name":player.name}])#empty data to turn it into a tuple, should be able to use a *
		trash = ReceiveData(client_server_sock)
	
		SendData(client_server_sock,["update",None])
		trash = ReceiveData(client_server_sock)
	
	for player in home:
		SendData(client_server_sock,["update", "Fsetstart", {"name":player.name, "init":[player.init.x, player.init.y]}])
		trash = ReceiveData(client_server_sock)



	whilecount = 0#need this!
	transferdata() #one head start of data transfer, probably not necessary
	thread.start_new_thread(masstransfer,())




	#focused = clone

	#print man.rect

	lag = 0
	whilecount = 0
	while 1:
	
	
	
		#print mpx
		#print area.width
		#print pygame.display.Info().current_w
		#print pygame.display.Info().current_h
		#area = screen.get_rect()
		whilecount +=1
		#masterscale controls the map zooming in and out.#turned off when commented out, ie leave the masterscale at 1, revert to specific case
		#masterscale = 6/(man.scale/30 + 5)#this gives a combination of map changing size and player changing size
		#masterscale = 1/(man.scale/30)#this makes the man always stay the same size, and jsut hte map scales
		#print masterscale
	
		#transferdata()
		#clock.tick(60)#with this commented, runs as fast as it can, still too slow.
	
	
	
	

		try:
			if whilecount % 2  == 0:# and 1 == 2:
				if man.modifiedscale == 1:
					man.sound.stop()
					for i in range(len(man.sound.array)):
						#print i
						#print array[i]
						man.sound.array[i][0] = int(4000*math.sin(i/220*2*math.pi/man.scale*240))
						man.sound.array[i][1] = man.sound.array[i][0]
					#print 1/220*2*math.pi/man.scale*120	
	
					man.sound.setArray()
					man.sound.play(0)
	
					#print array
		except:
			None#if you dont have numeric
	
	
	
		
		#time.sleep(0.016)
	
		#this should probably be moved inside update
		for player in opponents:
			player.b.yf += 22*player.scale/100*masterscale
		
		man.yf += 22*man.scale/100*masterscale #gravity
		man.b.yf += 22*man.scale/100*masterscale
		man.clone.yf += 22*man.clone.scale/100*masterscale
	
		#current state, force exerted on bots, but force overridden as use absolute velocities
		for player in players:#used to be opponents, but now want to look out for "man"'s hook hitting bots#it will send a force now to the other opponents, but this will be ignored
			if player in grounds:
				if player.hook.weregoing == 1 and player.hook.pressingbutton3 == 1:
					if player.hook.framecount == player.maxframe:
						for homer in home:
							if not homer is player:	#so you dont hook yourself		
								if homer.rect.collidepoint(*scrpos(player.cross.x, player.cross.y)):
									#print "initiate force"
									player.hook.distance = distance(player.cross, player)
									homer.yf -=  0.4*player.hook.distance*math.cos(player.hook.angle)*(player.scale/100)/(homer.scale/100)
									homer.xf -= 0.4*player.hook.distance*math.sin(player.hook.angle)*(player.scale/100)/(homer.scale/100)
	
	
	
	

	

		readinput(pygame.event.get())


	
	
	
		man.fixed.x = man.x; man.fixed.y = man.y
		man.clone.fixed.x = man.clone.x; man.clone.fixed.y = man.clone.y
	
		gunformotiontracking.xrectfixed, gunformotiontracking.yrectfixed = gunformotiontracking.rect.center	

	
		#lasttime = time.time()##########################################################



		for bot in bots:
			bot.preupdate()
		for sprite in spritelist:
			#lasttime = time.time()
			#print sprite.pyname()
			sprite.update()
			#lag = (time.time() - lasttime)*60
			#print lag
	
		#lag += (time.time() - lasttime)*60###############################################
		#if whilecount % 20 == 0:
		#	print lag /20
		#	lag = 0	
	
	
		if blur == 1:
			blur = 2
			blurcount = whilecount
		if blur == 2:
			if whilecount - blurcount > 150:
				blur = 0	
	
		if needsmask == 1:	
			if blur == 2:
				background.set_alpha(100)
				screen.blit(background, (0, 0))	
			else:
				background.set_alpha(250)	
				screen.blit(background, (0, 0))
	
	
	
		swidth = pygame.display.get_surface().get_rect().width
		sheight = pygame.display.get_surface().get_rect().height	
		for sprite in dspritelist:
			#screen.blit(sprite.image, (0,0, swidth,sheight), (-sprite.rect.left,-sprite.rect.top,swidth,sheight))#only blits what is on the screen (is this necessary?)#shouldnt think so. ...so use old method
			screen.blit(sprite.image, sprite.rect)
	
	
	
	
		pygame.display.flip()#
	
	
		#pygame.display.set_caption(str(int(clock.get_fps())))
		#print (time.time() - lasttime)*60
	
		#print clock.get_fps()
	
	#speed checks:
	#input: 0
	#updating : 0.8
	#blitting: 0.1
	#flipping: 0.1	




