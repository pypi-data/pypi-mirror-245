

'''
	import lymphatic.system.connect as ly_connect
	[ r, c ] = ly_connect.start ()
'''

'''
	import lymphatic.system.connect as ly_connect
	[ r, c ] = ly_connect.now (ly_connect.parameters (
	
		#
		#	preselected = 10
		#
		loops = 5
	))
'''

'''
	priorities:

		import lymphatic.system.connect as ly_connect
		[ r, c ] = ly_connect.now (ly_connect.parameters (
		
			#
			#	preselected = 10
			#
			loops = 5,
			
			#
			#	preselected is driver port from climate
			#	
			driver_port = "10000"
		))
'''

from rethinkdb import RethinkDB

import lymphatic.system.climate as climate
import botany.cycle as cycle
import botany.modules.exceptions.parse as parse_exception

class connection_exception (Exception):
	pass

class parameters:
	def __init__ (this, ** keywords):
		print ("keywords:", keywords)
	
		if ("loops" in keywords):
			this.loops = keywords ['loops']
		else:
			this.loops = 10
			
		if ("driver_port" in keywords):
			this.driver_port = keywords ['driver_port']
		else:
			ports = climate.find ("ports")
			this.driver_port = ports ["driver"]
		
		this.delay = 1


def now (
	params = parameters ()
):
	print (
		"lymphatic system connect params:", 
		params.loops, 
		params.delay,
		params.driver_port
	)

	driver_port = params.driver_port;

	connection_attempt = 1;
	def connect (* positionals, ** keywords):	
		nonlocal connection_attempt;
		print (
			f"Attempt '{ connection_attempt }' to connect to rethink on port: { driver_port }", 	
		)
		
		connection_attempt += 1
		
		r = RethinkDB ()
		
		'''	
			conn = r.connect (
				host = 'localhost',
				port = 28015,
				ssl = {
					'ca_certs': '/path/to/ca.crt'
				}
			)
		'''
		c = r.connect (
			host = 'localhost',
			port = driver_port
		)

		print ('rethink connection established')
		return [ r, c ];
		
		
	try:
		connection = cycle.loops (
			connect, 
			cycle.presents ([]),
			
			loops = params.loops,
			delay = params.delay,
			
			records = 0
		)
	except Exception as E:
		parsed_exception = parse_exception.now (E)
		print ("connection loop exception:", str (E))		
		raise connection_exception ("A connection could not be made.")
	
	return connection;
	
start = now