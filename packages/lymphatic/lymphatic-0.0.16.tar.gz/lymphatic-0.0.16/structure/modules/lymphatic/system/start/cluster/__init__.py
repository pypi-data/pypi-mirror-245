
'''
	priorities:
		[ ] If any of the nodes in the cluster fail to start,
			then shutdown every node.  In this manner, the cycle
			can be used to attempt to restart the entire cluster
			again (with different ports).		
		
		[ ] start 3 nodes on any port, with defined proxy ports.
'''

'''
	"data_directory"
		/nodes
			/node_1
			/node_2
			/node_3
			/proxy
			
		/pids
'''

'''
import lymphatic.system.start.cluster as start_cluster
start_cluster.beautifully ({
	"data_directory": 
	"nodes": 3,
	"proxy": {
		"ports": {
			"driver": "",
			"cluster": "",
			"http": ""
		}
	}
})
'''
import botany.ports.find_multiple as find_multiple_ports

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def beautifully (parameters):
	nodes = parameters ["nodes"]

	ports = find_multiple_ports.beautifully (
		limits = [ 10000, 60000 ],
		amount = nodes * 3
	)

	proceeds_statement = []

	#def component (circuit):
	#	circuit ()

	with ThreadPoolExecutor () as executor:
		proceeds = executor.map (
			lambda circuit : circuit (), 
			circuits
		)
		
		executor.shutdown (wait = True)
		
		for proceed in proceeds:
			proceeds_statement.append (proceed)