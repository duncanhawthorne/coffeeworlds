class Bob():	
	pass
		
def pyname(self):
	result = []
	for item in globals():
		if globals()[item] is self:
			result.append(item)		
	return result

bob = "fred"
fred = Bob()
james = 1
barry = 1
print pyname(bob)
print pyname(fred)
print pyname(james)
