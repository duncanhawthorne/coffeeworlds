#!/usr/bin/env python
print "---MASTERMIND SERVER---"
#before dictionary switch 151
import os,sys
sys.path.append(os.path.split(sys.path[0])[0])
from Net import *
class ServerHandler(Server):
	def __init__(self):
		Server.__init__(self)
		self.chat = {}
		self.warninglightscount = 0
	def connect_func(self,sock,host,port):
		print "Server successfully connected to %s on port %s!" % (host,port)
	def client_connect_func(self,sock,host,port,address):
		print "A client, (ip: %s, code: %s) connected on port %s!" % (address[0],address[1],port)
	def client_disconnect_func(self,sock,host,port,address):
		print "A client, (ip: %s, code: %s) disconnected from port %s!" % (address[0],address[1],port)
		print "warning lights going on"
		self.warninglightscount = 1
		#if len(self.chat) == 1 or len(self.chat)==0:#the zero case is a legitimate last person leaving
		#	self.chat=[]#blank it because it wont update by itself
		#	self.warninglightscount = 0
		#	print "warning lights going off"
		self.potentialcrashers = []
		for first in self.chat:
			#self.potentialcrashers.append(line["name"])
			self.potentialcrashers.append(first)
	def add_message(self,message):
		self.chat.append(message)
		if len(self.chat) >= 60:
			self.chat = self.chat[1:]
	def handle_data(self,data):

		
		#crash detection##still sucks if sveral disconnect at once
		if self.warninglightscount != 0:
			print self.warninglightscount
			self.warninglightscount +=1
			try:#as on first connect of new guy there is no name sent
				if data[2]["name"] in self.potentialcrashers:
					self.potentialcrashers.remove(data[2]["name"])
			except:
				None
				
		if self.warninglightscount > 30:
			for crasher in self.potentialcrashers:
				del self.chat[crasher]
			for crasher in self.potentialcrashers:
				for item in self.chat:
					if self.chat[item]["flag"]["owner"] == crasher:
						self.chat[item]["flag"]["owner"] = "-"
						self.chat[item]["flag"]["current"][0] = self.chat[item]["flag"]["init"][0]#need to return it as could have dropped to infinity
						self.chat[item]["flag"]["current"][1] = self.chat[item]["flag"]["init"][1]		 				
								   					  	
			self.warninglightscount = 0
			print "warning lights going off"
		 #crash detection#################	
						
	
	
		self.wantdataback = 0
		if data[1] == "=":
			self.wantdataback = 1
			print self.chat
			#fixme this should all be automatic, based on what data is sent		
					
			self.chat[data[2]["name"]]["position"]["man"][0]=data[2]["position"]["man"][0]
			self.chat[data[2]["name"]]["position"]["man"][1]=data[2]["position"]["man"][1] ##these are the position
			self.chat[data[2]["name"]]["position"]["bullet"][0]=data[2]["position"]["bullet"][0]
			self.chat[data[2]["name"]]["position"]["bullet"][1]=data[2]["position"]["bullet"][1]
			self.chat[data[2]["name"]]["position"]["hook"][0]=data[2]["position"]["hook"][0]
			self.chat[data[2]["name"]]["position"]["hook"][1]=data[2]["position"]["hook"][1]
			self.chat[data[2]["name"]]["position"]["clone"][0]=data[2]["position"]["clone"][0]
			self.chat[data[2]["name"]]["position"]["clone"][1]=data[2]["position"]["clone"][1]
			self.chat[data[2]["name"]]["position"]["clonehook"][0]=data[2]["position"]["clonehook"][0]
			self.chat[data[2]["name"]]["position"]["clonehook"][1]=data[2]["position"]["clonehook"][1]			
								
			self.chat[data[2]["name"]]["scale"]=data[2]["scale"]#scale, moved
			self.chat[data[2]["name"]]["clonescale"]=data[2]["clonescale"]#scale, moved
					
			self.chat[data[2]["name"]]["velocity"]["man"][0]=data[2]["velocity"]["man"][0]
			self.chat[data[2]["name"]]["velocity"]["man"][1]=data[2]["velocity"]["man"][1] ##these are the velocity
			self.chat[data[2]["name"]]["velocity"]["bullet"][0]=data[2]["velocity"]["bullet"][0]
			self.chat[data[2]["name"]]["velocity"]["bullet"][1]=data[2]["velocity"]["bullet"][1]
			self.chat[data[2]["name"]]["angle"] = data[2]["angle"]  # this is the angle, not an integer, unlike the others
			self.chat[data[2]["name"]]["explosive"] = data[2]["explosive"]
			self.chat[data[2]["name"]]["clonestate"] = data[2]["clonestate"]
			self.chat[data[2]["name"]]["gun"] = data[2]["gun"]
			self.chat[data[2]["name"]]["flame"] = data[2]["flame"]
			self.chat[data[2]["name"]]["laser"] = data[2]["laser"]
			self.chat[data[2]["name"]]["hook"] = data[2]["hook"]
			self.chat[data[2]["name"]]["clonehook"] = data[2]["clonehook"]
		elif data[1] == "!":
			self.chat[data[2]["name"]]["health"] -= 0.2*data[2]["killerscale"]/(self.chat[data[2]["name"]]["scale"])
			if self.chat[data[2]["name"]]["health"] <= 0:
				self.chat[data[2]["name"]]["health"] = 0
				self.chat[data[2]["killername"]]["score"] += 1#add 1 to the score of the shooter
		elif data[1] == "*":
			self.chat[data[2]["name"]]["health"] = 1  
		elif data[1] == "^":
			self.chat[data[2]["name"]]["health"] += 0.2/(self.chat[data[2]["name"]]["scale"])*30
			if self.chat[data[2]["name"]]["health"] > 1:
				self.chat[data[2]["name"]]["health"] = 1
		elif data[1] == "+":
			self.chat[data[2]["name"]] = {"position":{"man":[0.0, 0.0], "bullet":[0.0, 0.0], "hook":[0.0, 0.0], "clone":[0.0, 0.0], "clonehook":[0.0,0.0]}, "health":1, "scale":0.0, "velocity":{"man":[0.0, 0.0], "bullet":[0.0, 0.0]}, "angle":0, "score":0, "explosive":0, "flag":{"current":[0,0], "owner":0, "init":[0,0]}, "clonestate":0, "gun":0, "flame":0, "laser":0, "hook":0, "clonehook":0, "clonescale":0}#name, position, health, scale, velocity, angle, score, explosive, flag
			print self.chat
		elif data[1] == "-":
			del self.chat[data[2]["name"]] 
		elif data[1] == "FO":
			self.chat[data[2]["name"]]["flag"]["owner"] = data[2]["taker"]
			self.chat[data[2]["taker"]]["score"] += 3 #3 points for a flag half capture	  			
		elif data[1] == "FD":
			self.chat[data[2]["name"]]["flag"]["owner"] = "returnable"
			self.chat[data[2]["name"]]["flag"]["current"][0] = data[2]["where"][0]
			self.chat[data[2]["name"]]["flag"]["current"][1] = data[2]["where"][1]
						 	
		elif data[1] == "FC":
			self.chat[data[2]["name"]]["flag"]["owner"] = "-"
			self.chat[data[2]["by"]]["score"] += 7 #7 points for a flag full capture
			self.chat[data[2]["name"]]["flag"]["current"][0] = self.chat[data[2]["name"]]["flag"]["init"][0]
			self.chat[data[2]["name"]]["flag"]["current"][1] = self.chat[data[2]["name"]]["flag"]["init"][1]   
							
		elif data[1] == "Fsetstart":
			self.chat[data[2]["name"]]["flag"]["init"][0] = data[2]["init"][0]
			self.chat[data[2]["name"]]["flag"]["init"][1] = data[2]["init"][1]
			self.chat[data[2]["name"]]["flag"]["current"][0] = self.chat[data[2]["name"]]["flag"]["init"][0]
			self.chat[data[2]["name"]]["flag"]["current"][1] = self.chat[data[2]["name"]]["flag"]["init"][1]					
			self.chat[data[2]["name"]]["flag"]["owner"] = "-"
		elif data[1] == "FR":
			self.chat[data[2]["name"]]["flag"]["current"][0] = self.chat[data[2]["name"]]["flag"]["init"][0]
			self.chat[data[2]["name"]]["flag"]["current"][1] = self.chat[data[2]["name"]]["flag"]["init"][1]
			self.chat[data[2]["name"]]["flag"]["owner"] = "-"	   				 			
		elif data[1] == "nomessage":
			self.wantdataback = 1
			
			
		self.wantdataback = 1	
		if self.wantdataback == 1:  #possible way to reduce bandwidth later 
			#print "sending it back"
	   		self.send_data(self.chat)
def main():
	server = ServerHandler()
	server.connect("localhost",6317)
	server.serve_forever()
	server.quit()
if __name__ == '__main__': main()
