#! /usr/bin/python
from threading import *
from socket import *

from project_p4 import *


class Agent(Thread):          # complete the line, per connection class

    def __init__(self,serv,sockObj, agentID):
		Thread.__init__(self)
		self._s = serv
		self.sock = sockObj[0]
		self.addr = sockObj[1]
		self.agentID = agentID
		
		path = '/tmp/' + str( self.addr[0] ) + '.c'
		wf = open(path, 'w')
		wf.close()
		
    def run(self):

		command = self.sock.recv(1024)
		
		print "Command:  ", command
		print ""
		print "**********************************************"
		print ""
		
		while command:
			
			c2 = command.split('@')
			
			codeFlag = False
			if c2[0] == 'code':
				
				path = '/tmp/' + str( self.addr[0] ) + '.c'
				wf = open(path, 'w')
	
				wf.write( c2[1] )
				wf.write( "\n" )
				wf.close()
				data = path + '@'
				codeFlag = True
				
				self.sock.send( data )
				#command = self.sock.recv(1024)
				#continue
			
			c = command.strip(' \n').split(' ')
			
			
			if c[0] == "check":
				# check existence of gcc object
				gcc = serv.get( "gcc", self.addr[0], int(c[1]) )
				if gcc :
					data = "True"
				else :
					data = "False"	
				
				self.sock.send( data )	
				
			
			elif c[0] == 'destroy':

				serv._set( c[1] , self.addr[0], int(c[2]) )
				
				data = "Your object has been deleted!\n"
				self.sock.send( data )
				
			
			elif c[0] == 'gcc':
				
				flags = []
				for flag in c[2:] :
					flags.append(flag)
							
				gccObj = GCC( c[1], flags )
				idOfObj = serv._set( "gcc" , self.addr[0], gccObj )
				
				data = "Your GCC object has been initialized and its id is " + str(idOfObj) + "\n"
				self.sock.send( data )
		
		
			elif c[0] == 'compile':
				gcc = serv.get( "gcc", self.addr[0], int(c[1]) )
				
				if gcc:	
					data = gcc.compileTheFile()
					self.sock.send( data )

				else:
					data = "You have not initialized your object!\n"
					self.sock.send( data )
			
			
			elif c[0] == 'getErrors':
				gcc = serv.get( "gcc", self.addr[0], int(c[1]) )
				
				if gcc:	
					data = gcc.getErrors()
					self.sock.send( data + '\n')

				else:
					data = "You have not initialized your object!\n"
					self.sock.send( data + '\n')


		#######################################################################################################

	
			elif c[0] == 'gdb':
				
				inputs = []
				for inp in c[2:] :
					inputs.append(inp)

				gdbObj = GDB( c[1], inputs )
				idOfObj = serv._set( "gdb", self.addr[0], gdbObj )
				
				data = "Your GDB object has been initializedand and its id is " + str(idOfObj) + "\n"
				self.sock.send( data + '\n')
				
	
			elif c[0] == 'run':
				
				gdb = serv.get( "gdb", self.addr[0], int(c[1]) )
				
				if gdb:	
					data = gdb.run()
					print "Data is : "
					print data
					self.sock.send( data )

				else:
					data = "You have not initialized your object!\n"
					self.sock.send( data + '\n')
			
			
			elif c[0] == 'next':
				
				gdb = serv.get( "gdb", self.addr[0], int(c[1]) )
				
				if gdb:	
					data = gdb.next()
					self.sock.send( data )

				else:
					data = "You have not initialized your object!\n"
					self.sock.send( data + '\n')
			

			elif c[0] == 'step':
				
				gdb = serv.get( "gdb", self.addr[0], int(c[1]) )
				
				if gdb:	
					data = gdb.step()
					self.sock.send( data )

				else:
					data = "You have not initialized your object!\n"
					self.sock.send( data + '\n')
		

			elif c[0] == '_print':
				
				gdb = serv.get( "gdb", self.addr[0], int(c[2]) )
				
				if gdb:	
					data = gdb._print(c[1])
					self.sock.send( data )

				else:
					data = "You have not initialized your object!\n"
					self.sock.send( data + '\n')
			
			
			elif c[0] == 'clear':
				
				gdb = serv.get( "gdb", self.addr[0], int(c[2]) )
				
				if gdb:	
					data = gdb.clear(c[1])
					self.sock.send( data )

				else:
					data = "You have not initialized your object!\n"
					self.sock.send( data + '\n')
			
			
			elif c[0] == 'b':
				
				gdb = serv.get( "gdb", self.addr[0], int(c[2]) )
				
				if gdb:	
					data = gdb.b(c[1])
					self.sock.send( data )

				else:
					data = "You have not initialized your object!\n"
					self.sock.send( data + '\n')
			
			else:
				if codeFlag == False:		
					data2 = "Your command is not recognized!\n"
					self.sock.send( data2 )
					
					
			command = self.sock.recv(1024)


'''
clients
{
	ip  : { gcc : [ ], gdb : [ ] }
	ip2 : { gcc : [ ], gdb : [ ] }	
	.
	.
	. 
}
'''

class CacheServ:

	_clients = {}
	_id = 0
    
	def __init__(self,ipport):
		self._l = Lock()
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.bind(('',ipport))
		self.sock.listen(1)


	def _set(self, typeObj, ip, obj ):    # set var in dict to value
		self._l.acquire()
		self._clients[ip][typeObj].append(obj)
		self._clients[ip][typeObj][0] = obj
		self._l.release()
		#return len( self._clients[ip][typeObj] ) - 1
		return 0

	def get(self, typeObj, ip, idOfObj ):           # get var from dict
		self._l.acquire()
		if self._clients.has_key(ip) and idOfObj < len( self._clients[ip][typeObj] ) and self._clients[ip][typeObj][idOfObj] != -1:
			v = self._clients[ip][typeObj][idOfObj]
		else:
			v = False 	
		self._l.release()
		return v
	
	
	def destroy( self, typeObj, ip, idOfObj ):
		self._l.acquire()
		self._clients[ip][typeObj][idOfObj] = -1
		self._l.release()


	
	def varl(self):
		self._l.acquire()
		v = ' '.join(self._vars.keys())
		self._l.release()
		return v
	
        
	def start(self):    # start accepting connections
		c = self.sock.accept()
		self._clients[c[1][0]] = { "gcc" : [], "gdb" : [] }
		
		while c :       # main loop, create a thread here
			a = Agent(self, c, self._id)    
			
			print "SOCKET_OBJ  :  " , c[0]
			print ""
			print "SOCKET_ADDR :  " , c[1]
			print ""
			print "AGENT :  " , a
			print ""
			a.start()
			
			c = self.sock.accept()
			self._id += 1
			
			if self._clients.has_key(c[1][0]) == False:
				self._clients[c[1][0]] = { "gcc" : [], "gdb" : [] }

		return


if __name__ == '__main__':
    serv = CacheServ(20000)
    serv.start()
    
    
