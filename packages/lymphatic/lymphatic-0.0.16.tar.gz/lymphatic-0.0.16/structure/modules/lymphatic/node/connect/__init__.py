

'''
	import lymphatic.node.connect as ly_node_connect
	[ r, c ] = ly_node_connect.sweetly (
		driver_port = ""
	)
'''

'''
	import lymphatic.system.connect as ly_connect
	[ r, c ] = ly_connect.sweetly (
		loops = 3,
		delay = 2
	)
'''

'''	
	from rethinkdb import RethinkDB
	r = RethinkDB ()
	conn = r.connect (
		host = 'localhost',
		port = 28015,
		ssl = {
			'ca_certs': '/path/to/ca.crt'
		}
	)
'''

from rethinkdb import RethinkDB

import lymphatic.system.climate as climate
import botany.cycle as cycle
import botany.modules.exceptions.parse as parse_exception

class connection_exception (Exception):
	pass


def sweetly (
	loops = 10,
	delay = 1,
	driver_port = None,
	host = "localhost",
	
	label = "connect"
):
	print ('driver_port', driver_port)

	if (driver_port == None):
		ports = climate.find ("ports")
		driver_port = ports ["driver"]

	connection_attempt = 1;
	def connect (* positionals, ** keywords):	
		nonlocal connection_attempt;
		print (
			f"{ label }: Attempt '{ connection_attempt }' to connect to rethink at: { host }, { driver_port }", 	
		)
		
		connection_attempt += 1
		
		
		'''	
			conn = r.connect (
				host = 'localhost',
				port = 28015,
				ssl = {
					'ca_certs': '/path/to/ca.crt'
				}
			)
		'''
		r = RethinkDB ()
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
			
			loops = loops,
			delay = delay,
			
			records = 0
		)
	except Exception as E:
		parsed_exception = parse_exception.now (E)
		print ("connection loop exception:", str (E))		
		raise connection_exception ("A connection could not be made.")
	
	return connection;
