# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render

from socket import *


HOST = ''           
PORT = 20000         

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))
	
idOfObj = 0
gdbPath = ''
path = ''

lastTenDebug = []

def index(request):
	
	command = 'check 0'

	s.send( command )            
	data = s.recv(1024)
	
	load = data
			
	context = { 'compileResult': '', 'load' : load }
	return render(request, "index.html", context) 
		

	
def compiler(request):

	code = request.POST.get('code')
	global gdbPath
	global path
	
	if code == None:
		idOfObj = 0
		
			
	else:
		command = 'code@'
		command += code
	
		s.send( command )            
		data = s.recv(1024)
		path = data.split('@')[0]
		gdbPath = path + '.out'
		
		exeName = path.split('/')[-1] + '.out'
	
		s.send( 'gcc ' + path + ' -o ' + gdbPath + ' -g ' )
		data = s.recv(1024)
		print data
		idOfObj = data.split(' ')[-1]
	
	
	s.send('compile ' + str(idOfObj) )
	data = s.recv(1024)
	
	
	s.send('getErrors ' + str(idOfObj))
	data = s.recv(1024)

	data = data.strip(' \t\n\r')
	
	check = 0
	if data == 'You do not have any errors!':
		check = 1	
	
	
	lineNumList = []
	splittedData = data.split('\n')
	
	for line in splittedData:
		splittedLine = line.split()
		
		lenSL = len(splittedLine)
		i = 0
		
		while i < lenSL :
			if splittedLine[i] == 'In' and splittedLine[i+1] == 'line':
				lineNumList.append( int(splittedLine[i+2]) )
				break
				
			i += 1	
	
	
	fp = open( path, "r" )
	wholeCode = fp.read()	
	
	temp = data.split("\n")
	
	compileResult = []
	for line in temp:
		compileResult.append(line)
		
	context = { 'compileResult': compileResult, 'check' : check, 'lineNumList': lineNumList, "wholeCode" : wholeCode }
	
			  
	return render(request, "compiler.html", context) 
	
	



def debugger(request):
	
	global gdbPath
	
	arguments = request.POST.get('arguments')
	c = request.POST.get('command')
	
	debugResult = ''
	
	if arguments != None:
	
		command = 'gdb ' + gdbPath + ' ' + arguments

		s.send( command )            
		data = s.recv(1024)
		idOfObj = data.split(' ')[-1]
		
	
	
	if c != None:
		
		idOfObj = 0
		c = c.strip(' \n')
		s.send( c + ' ' +  str(idOfObj) )
		data = s.recv(1024)
		debugResult = data


	lastTenDebug.append(debugResult)
		
	temp = lastTenDebug[::-1]
	temp = temp[0:10]
	
	context = { 'debugResult': debugResult, 'lastTenDebug': temp }
			  
	return render(request, "debugger.html", context) 
	
	
	
def debuggerBreak(request):
	
	global gdbPath
	
	arguments = request.POST.get('arguments')
	c = request.POST.get('command')
	
	debugResult = ''
	
	if arguments != None:
	
		command = 'gdb ' + gdbPath + ' ' + arguments

		s.send( command )            
		data = s.recv(1024)
		idOfObj = data.split(' ')[-1]
		
	
	
	if c != None:
		
		idOfObj = 0
		c = c.strip(' \n')
		s.send( 'b ' + c + ' ' +  str(idOfObj) )
		data = s.recv(1024)
		debugResult = data


	lastTenDebug.append(debugResult)
		
	temp = lastTenDebug[::-1]
	temp = temp[0:10]
	
	context = { 'debugResult': debugResult, 'lastTenDebug': temp }
			  
	return render(request, "debugger.html", context) 
	
	
	
def debuggerPrint(request):
	
	global gdbPath
	
	arguments = request.POST.get('arguments')
	c = request.POST.get('command')
	
	debugResult = ''
	
	if arguments != None:
	
		command = 'gdb ' + gdbPath + ' ' + arguments

		s.send( command )            
		data = s.recv(1024)
		idOfObj = data.split(' ')[-1]
		
	
	
	if c != None:
		
		idOfObj = 0
		c = c.strip(' \n')
		s.send( '_print ' + c + ' ' +  str(idOfObj) )
		data = s.recv(1024)
		debugResult = data


	lastTenDebug.append(debugResult)
	
	temp = lastTenDebug[::-1]
	temp = temp[0:10]
	
	context = { 'debugResult': debugResult, 'lastTenDebug': temp }
			  
	return render(request, "debugger.html", context) 
	
	
	
def debuggerClear(request):
	
	global gdbPath
	
	arguments = request.POST.get('arguments')
	c = request.POST.get('command')
	
	debugResult = ''
	
	if arguments != None:
	
		command = 'gdb ' + gdbPath + ' ' + arguments

		s.send( command )            
		data = s.recv(1024)
		idOfObj = data.split(' ')[-1]
		
	
	
	if c != None:
		
		idOfObj = 0
		c = c.strip(' \n')
		s.send( 'clear ' + c + ' ' +  str(idOfObj) )
		data = s.recv(1024)
		debugResult = data


	lastTenDebug.append(debugResult)
	
	temp = lastTenDebug[::-1]
	temp = temp[0:10]
	
	context = { 'debugResult': debugResult, 'lastTenDebug': temp }
			  
	return render(request, "debugger.html", context) 
		
	
		
