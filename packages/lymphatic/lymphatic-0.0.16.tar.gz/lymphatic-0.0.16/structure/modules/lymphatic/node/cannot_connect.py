
'''
import lymphatic.node.cannot_connect as ly_node_cannot_connect
ly_node_cannot_connect.ensure (
	loops = 3,
	driver_port = driver_port
)
'''

import lymphatic.node.connect as connect

def ensure (
	loops = 5,
	driver_port = -10
):
	could_not_connect = False
	try:
		[ r, c ] = connect.sweetly (
			label = "asserting that can't connect",
			driver_port = driver_port,
			loops = loops
		)
		
		data = c.server ()
		
		print ('data:', data)
		print ("Was able to connect, when should not have been able to connect")
		
	except Exception as E:	
		print (E)
		could_not_connect = True
		
	assert (could_not_connect == True)