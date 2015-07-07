#!/usr/bin/python

import sys
from subprocess import Popen, PIPE

from time import sleep
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read




class GCC:

	fileName = ""
	flags = ""
	
	compile_stderr = ""
	forGetErrors = ""
	
	hasError = False
	
	
	def __init__( self, fileName, flags ):
		
		self.flags = flags
		self.fileName = fileName

		
	def compileTheFile( self ) :
		
		result = ""
		
		Popened = [ '/usr/bin/gcc', self.fileName ]
		
		for arg in self.flags :
			Popened.append(arg)
			
		Popened.append('-g')	
		
		compiled = Popen( Popened, stdout = PIPE, stderr = PIPE )
	
		readed = compiled.stderr.readline()
		while readed != "" :
			self.compile_stderr += readed
			readed = compiled.stderr.readline()		
		
		
		
		if self.compile_stderr == "" :
			result += "Your file is compiled succesfully!\n"
			self.compile_stderr = ""
			
			for flag in self.flags :
				if flag[0] != '-' :
					result += "You can execute your file as ./" + flag + '\n'
					return result;  			
			
			result += "You can execute your file as ./a.out\n"
			return result
		
		else:
			result += "Your file is not compiled succesfully!"
			self.hasError = True
			
		
		self.forGetErrors = self.compile_stderr				
		self.compile_stderr = ""
		
		return result
		
		
		
	def getErrors( self ) :
		
		if self.hasError == False :
			return "You do not have any errors!\n"
		
		
		result = ""
		
			
		i = 0
		errorString = ""
		
		while i < len(self.forGetErrors) and self.forGetErrors[i] != ':' :
			errorString += self.forGetErrors[i]
			i += 1
			
			
		if errorString == "gcc" :
			result += self.forGetErrors[5:] + "\n"
			result += "Example usage is gcc file.c [flags]\n"
			return result	
			
			
	
		if errorString == self.fileName:
			
			#print forGetErrors.split("\n")
			lineSplitted = self.forGetErrors.split("\n")

			for line in lineSplitted :
				if len(line.split(":")) > 4 and ( line.split(":")[3] == " error" or line.split(":")[3] == " warning" ) :	
					result += "In line " + line.split(":")[1] + line.split(":")[4] + "\n"
			 	
				if len(line.split(":")) > 4 and line.split(":")[3] == " fatal error" : 
					result += "In line " + line.split(":")[1] + line.split(":")[4] + line.split(":")[5] + "\n"
			 		
			return result
		
			
				
		if ( "undefined" in self.forGetErrors.split("\n")[1].split(" ") ) and ( "reference" in self.forGetErrors.split("\n")[1].split(" ") ) :
			result += self.forGetErrors.split("\n")[1].split(":")[-1] + "\n"
			return result
		
		
		
		if errorString == "/usr/bin/ld":
			result += "main function is not defined!\n"


		else :	
					
			result += "Example usage is gcc file.c [flags]\n"
		
		self.forGetErrors = ""
		return result
		



class GDB:
	
	fileName = ""
	inputs = []	
	
	p = 0
	
		
	def __init__( self, fileName, inputs ):
		
		self.fileName = fileName	
		self.inputs = inputs
	
	
		# run the shell as a subprocess:
		self.p = Popen(['/usr/bin/gdb', self.fileName], stdin = PIPE, stdout = PIPE, shell = False)

		# set the O_NONBLOCK flag of p.stdout file descriptor:
		flags = fcntl(self.p.stdout, F_GETFL) # get current p.stdout flags
		fcntl(self.p.stdout, F_SETFL, flags | O_NONBLOCK)
		
		self.p.stdin.write( '\n' )
		
		sleep(0.1)
	
		while True:
			try:
				output = read(self.p.stdout.fileno(), 1024)
				
			except OSError:
				# the os throws an exception if there is no data
				#print '[No more data]'
				break
		
		return			
			

	def run( self )	:
					
		self.p.stdin.write( "run" + '\n')
		
		for i in self.inputs:
			self.p.stdin.write( str(i) + '\n')
		
		result = ""
		
		sleep(1)
		
		'''
		while True :
		
			ps = Popen( ['/bin/ps', '-ax'], stdout = PIPE )

			pid = 0
			line = ps.stdout.readline()
			found = False

			while( line ):
	
				splitted = line.split()
				pid = splitted[0]
				status = splitted[2]
				name = splitted[4]
				name = name.split('/')
				
				fn = self.fileName[2:]
				
				if fn in name :
					found = True
					if status[0] == 'R' :
						break
					
					#elif status[0] == 'S':
						
				line = ps.stdout.readline()
			
			
			if found == False :
				break
		'''
		

		while True:
			try:
				output =  read(self.p.stdout.fileno(), 1024)
			except OSError:
				# the os throws an exception if there is no data
				#print '[No more data]'
				break
				
		#print output	
		
		
		output = output.split("\n")

		if "Starting" in output[0].split(" "):
			index = 0

		else :
			index = 2
		
		if "normally]" in output[-2].split(" "):
		
			result += "Your program is being started...\n"
			
			for line in output[index+1:-2]:
				result += line + '\n'
			
			result += "Your program is executed successfully.\n"			
		
		
		elif "Breakpoint" in output[-3].split(" ") :
			
			#for line in output[index+1:-3]:
				#print line
			
			result += output[-3].split(" ")[0] + " " +output[-3].split(" ")[1] + "\n"
			result += "Line " + output[-2] + "\n"
			
		
		else:
			
			#for line in output[index+1:-3]:
				#print line
		
			error = output[-2].split()
			temp  = ""
			temp += "Segmentation fault at line " + error[0] + " in the expression "
			for ch in error[1:] :
				temp +=  ch + " "
		
			result += temp + "\n"				 	
		
		
		return result
	

		
	def next( self ) :

		self.p.stdin.write( "next" + '\n')
	
		result = ""

		sleep(0.1)

		while True:
			try:
				output =  read(self.p.stdout.fileno(), 1024)
				
			except OSError:
				# the os throws an exception if there is no data
				#print '[No more data]'
				break
		
		#print output.split()
		
		if len(output) == 1 : 
			return 
	
		if "normally]" in output.split():
			result += "Program exited normally.\n"
		
		elif "__libc_start_main" in output.split():
			result += "Last line of the code."	
		
		elif "Breakpoint" in output.split():
			result += "Breakpoint " + output.split()[1] + "\n"
			result += "Line " + output.split()[6] + "\n"
			
			temp = ""
			for ch in output.split()[7:-1]:
				temp += ch + " " 	
			
			result += temp + "\n"
		
		
		elif "SIGSEGV," in output.split():
			result += output.split("\n")[1] + "\n" 
			result += "In line " + output.split()[12] + "\n"
			
		else:
			result += output.split("\n")[0] + "\n"
			
		
		return result
		
		
	# geri gel
	def step( self ) :
	
		self.p.stdin.write( "step" + '\n')

		sleep(0.1)

		while True:
			try:
				output =  read(self.p.stdout.fileno(), 1024)
				print output
			except OSError:
				# the os throws an exception if there is no data
				#print '[No more data]'
				break
	
		#print output.split()
		
		if len(output) == 1 : 
			return ""
	
		if "normally]" in output.split():
			print "Program exited normally."
		
		elif "__libc_start_main" in output.split():
			print "Last line of the code."	
		
		elif "Breakpoint" in output.split():
			print "Breakpoint " + output.split()[1]
			print "Line " + output.split()[6]
			
			for ch in output.split()[7:-1]:
				print ch, 	
		
		elif "SIGSEGV," in output.split():
			print output.split("\n")[1]
			print "In line " + output.split()[12]
			
		else:
			print output.split("\n")[0]
			
		
		return
	
		
	
	def _print( self, varName )	:
		
		self.p.stdin.write( "print" + " " + varName +'\n')

		result = ""
		sleep(0.1)

		while True:
			try:
				output =  read(self.p.stdout.fileno(), 1024)
			except OSError:
				# the os throws an exception if there is no data
				#print '[No more data]'
				break		

		#print output.split()

		if len(output.split()) == 1 : 
			return 
		
		else:
			result += varName + " = " + output.split()[2] + "\n"	
		
		return result
		
	
	def clear( self, lineNumber ) :	
		
		self.p.stdin.write( "clear" + " " + str(lineNumber) + '\n')
		
		result = "" 
		sleep(0.1)

		while True:
			try:
				output =  read(self.p.stdout.fileno(), 1024)
			except OSError:
				# the os throws an exception if there is no datagdb.run()
				#print '[No more data]'
				break	
		
		if len(output.split()) == 1 : 
			return
		
		result += output.split("\n")[0]	+ "\n"	
		return result
		
		
	def b( self, lineNumber ) :

		self.p.stdin.write(	"break" + " " + str(lineNumber) + '\n')
	
		result = ""
		sleep(0.1)

		while True:
			try:
				output =  read(self.p.stdout.fileno(), 1024)
			except OSError:
				# the os throws an exception if there is no data
				#print '[No more data]'
				break			
		
		#print output.split()
				
		if len(output.split()) == 1 : 
			return 	 		
		
		if output.split()[0] == "Make" :
			result += "There is no line " + str(lineNumber) + " on the file.\n"
		
		elif output.split()[0] == "Breakpoint" :
			result += "Breakpoint " + output.split()[1] + " at line " + str(lineNumber) + "\n"
			
		else:
			result += "Breakpoint " + output.split()[2] + " also set at line " + str(lineNumber) + "\n"
			result += "Breakpoint " + output.split()[9] + " at line " + str(lineNumber) + "\n"
			
		return result




	#p wait handle
	#p.wait()
	#compiled.wait()

