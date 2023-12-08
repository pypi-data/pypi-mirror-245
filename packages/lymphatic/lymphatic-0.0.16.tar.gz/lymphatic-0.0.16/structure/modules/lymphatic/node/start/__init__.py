

'''
	Description:
		This starts the node from internally.
		
		This creates a data directory if one does not
		already exist.
		
			if data directory doesn't exist:
				rethinkdb create
				
			rethinkdb serve
'''

'''
import pathlib
import lymphatic.node.start as ly_node_start
ly = ly_node_start.loyally (
	proxy = False,
	server_name = "node-1",
	ports = {
		"driver": 18871,
		"cluster": 0,
		"http": 0	
	},
	process = {
		"cwd": pathlib.Path (__file__).parent.resolve ()
	},
	rethink_params = [
		f"--daemon",
		f"--pid-file {}"
	]
)


ly.stop ()
'''

'''
	steps:
		* checks that cannot connect
		* The node is started.
		* checks that can connect to the server with the server_name provided.
		* makes assertions about the database contents
'''

'''
setsid
'''

import atexit
import json
import subprocess
import shlex
import time

import lymphatic.node.cannot_connect as cannot_connect
import lymphatic.node.connect as ly_node_connect
import lymphatic.node.start.assertions as node_start_assertions

import os
		

def loyally (
	proxy = False,
	
	server_name = "",
	rethink_params = [],
	ports = {},
	
	records = 1,
	
	** keywords
):		
	assert (type (server_name) == str)
	assert (len (server_name) >= 1)
	

	course_name = "[rethink node start] ";

	#
	process_keys = keywords ["process"]

	#
	driver_port = str (ports ["driver"])
	cluster_port = str (ports ["cluster"])
	http_port = str (ports ["http"])

	#
	#	check if can connect,
	#	if it can, then there's already a rethinkdb process
	#	running
	#
	if (records >= 1):
		print (f"{ course_name }Making sure can't connect to an already running process.")
	
	
	cannot_connect.ensure (
		loops = 1,
		driver_port = driver_port
	)

	node_string = "rethinkdb"
	if (proxy):
		node_string += " proxy"
	
	script = " ".join ([
		node_string,
		
		f"--server-name { server_name }",
		
		f"--driver-port { driver_port }",
		f"--cluster-port { cluster_port }",
		f"--http-port { http_port }",
		
		* rethink_params
	])
	
	if (records >= 1):	
		print (f"{ course_name }script:", script)
		print (f"{ course_name }rethink_params:", rethink_params)
		print (f"{ course_name }keywords:", keywords)

	process = subprocess.Popen (
		shlex.split (script),
		
		#check = True, 
		
		** process_keys
	)	
	[ r, c ] = ly_node_connect.sweetly (
		driver_port = driver_port,
		loops = 2
	)
	server_data = c.server ();
	print ("server_data:", server_data)
	assert (server_data ["name"] == server_name)
	
	node_start_assertions.check (r, c)		
	c.close ()

	