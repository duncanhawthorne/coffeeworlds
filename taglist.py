class taglist():
	def __init__(self, item):
		self.parent = None
		if item is None:
			self.data = []
		else:
			self.data = item
	def __getitem__(self, arg):
		self.getdata = taglist([])
		self.getdata.parent = self
		for line in self.data:
			if arg in line[1]:
				self.getdata.append(line)
		return self.getdata
	def __setitem__(self, arg, result):
		for i in range(len(self.data)):
			if arg in self.data[i][1]:
				self.data[i][0] = result
				
	def __len__(self):
		return len(self.data)
	def append(self, item):
		found = 0
		for line in self.data:
			if line[0] == item[0]:
				found = 1
		if found == 0:
			self.data.append(item)
		else:
			print "already in list"
		#check item[0] doesnt already exist#fixme
	def remove(self, item):
		for line in self.data:
			if line[0] == item:
				self.data.remove(line)
		
		#for i in range(len(self.data)):
		#	if self.data[i][0] = item:
		#		self.data.remove(self.data[i])
	def __repr__(self):
		data = []
		for item in self.data:
			data.append(item[0])
		return repr(data)
		#return repr(self.data)
		
	def __add__(self, arg):
		if type(arg) is list:
			tags = arg
		else:
			tags = [arg]
			
		if not self.parent is None:
			for item in self.data:
				#print "first"
				#key = item[0]
				for i in range(len(self.parent.data)):
					#print "second"
					if self.parent.data[i][0] == item[0]:
						for tag in tags:
							#print "third"
							self.parent.data[i][1].append(tag)
		else:
			print "error"						
	def __eq__(self, arg):
		if type(arg) is list:
			tags = arg
		else:
			tags = [arg]
			
		if not self.parent is None:
			for item in self.data:
				#print "first"
				#key = item[0]
				for i in range(len(self.parent.data)):
					#print "second"
					if self.parent.data[i][0] == item[0]:
						self.parent.data[i][1] = []
						for tag in tags:
							#print "third"
							self.parent.data[i][1].append(tag)
		else:
			print "error"						
	def __sub__(self, arg):
		if type(arg) is list:
			tags = arg
		else:
			tags = [arg]
			
		if not self.parent is None:
			for item in self.data:
				#print "first"
				#key = item[0]
				for i in range(len(self.parent.data)):
					#print "second"
					if self.parent.data[i][0] == item[0]:
						#self.parent.data[i][1] = []
						for tag in tags:
							#print "third"
							self.parent.data[i][1].remove(tag)
		else:
			print "error"
	def gettags(self):
		answer = []
		if not self.parent is None:
			for item in self.data:
				#print "first"
				#key = item[0]
				for i in range(len(self.parent.data)):
					#print "second"
					if self.parent.data[i][0] == item[0]:
						#self.parent.data[i][1] = []
						answer.append(self.parent.data[i][1])
			return answer
		else:
			print "error"					
#	def settags(self, item, tags):
#		for i in range(len(self.data)):
#			if item in self.data[i][1]:
#				self.data[i][1] = []
#				for tag in tags:
#					self.data[i][1].append(tag)
#	def addtags(self, item, tags):	
#		for i in range(len(self.data)):
#			if arg in self.data[i][1]:
#				#self.data[i][1] = []
#				for tag in tags:
#					self.data[i][1].append(tag)
#	def remtags(self, item, tags):	
#		for i in range(len(self.data)):
#			if arg in self.data[i][1]:
#				#self.data[i][1] = []
#				for tag in tags:
#					self.data[i][1].remove(tag)										
		
bob = taglist([["a", ["b", "c"]], ["fred", ["b", 12, None, "empty"]]])
bob.append(["a", ["e", "f", "b", "c"]])
print bob
print bob["e"]["b"]		

bob["e"] = "duncan"
print bob
print bob.data
print "hi"

print bob["c"].gettags()
bob["c"] + "sarah"
print bob
print bob.data



#bob.settags(12, ["james"])
print bob
print bob["james"]

print bob.data

