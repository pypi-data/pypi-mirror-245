

'''
	descriptions:
		two+ possible reasons for cycling:
			1. rethinkdb_data is already in use
				
				This one will like loop forever...
				
				could figure this out by looking up the cwd
				of all rethinkdb processes... etc.
				
			
			2. port or ports are already in use
'''

'''
import pathlib
import lymphatic.node.start_cycle as ly_node_start_cycle
ly = ly_node_start.sweetly (
	process = {
		"cwd": pathlib.Path (__file__).parent.resolve ()
	},
	rethink_params = [
		f"--daemon",
		f"--pid-file { pid_file_path }"
	]
)
'''

'''
	important:
		
'''

'''
	possibilites:
		--directory
	
		--no-http-admin
		--log-file
'''

import pathlib

import botany.modules.exceptions.parse as parse_exception
import botany.cycle as cycle
import botany.ports.find_multiple as find_multiple_ports

import lymphatic.node.start as ly_node_start

def start_node (* positionals, ** keywords):
	server_name = positionals [0]
	process = positionals [1]
	rethink_params = positionals [2]
	
	print ("positionals:", positionals)

	ports = find_multiple_ports.beautifully (
		limits = [ 10000, 60000 ],
		amount = 3
	)
	
	print ("ports:", ports)

	ly = ly_node_start.loyally (
		server_name = server_name,
		ports = {
			"driver": ports [0],
			"cluster": ports [1],
			"http": ports [2]
		},
		process = process,
		rethink_params = rethink_params
	)
	
	return {
		"ports": {
			"driver": ports [0],
			"cluster": ports [1],
			"http": ports [2]
		}
	}

			


def sweetly (
	server_name = "",
	process = "",
	rethink_params = [],
	
	loops = 10,
	delay = 1
):
	try:
		connection = cycle.loops (
			start_node, 
			cycle.presents ([
				server_name,
				process,
				rethink_params
			]),
			
			loops = loops,
			delay = delay,
			
			records = 1
		)
		
		return connection;
		
	except Exception as E:
		parsed_exception = parse_exception.now (E)
		print ("start loop exception:", str (E))		
		raise Exception ("A node could not be started.")