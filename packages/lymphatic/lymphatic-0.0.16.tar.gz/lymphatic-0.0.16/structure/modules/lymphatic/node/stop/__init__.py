
'''
	import lymphatic.node.stop as ly_node_stop
	ly_node_stop.beautifully (
		pid_file_path,
		driver_port
	)
		
'''

'''
	notes:
		rethinkdb removes the pid file when stopped
		like this.
'''

import lymphatic.node.cannot_connect as ly_node_cannot_connect

import psutil

def beautifully (
	pid_file_path,
	driver_port
):
	print ("[stopping rethinkdb]")

	FP = open (pid_file_path)
	P_ID = int (FP.read ().strip ())

	p = psutil.Process (P_ID)
	p.terminate ()
	
	ly_node_cannot_connect.ensure (
		loops = 2,
		driver_port = driver_port
	)
	
	return;