#!/bin/python

import modules.fluxMonitor as fm

if __name__ == "__main__": 

	# Initilize network
	Monitor = fm.fluxMonitor()



	# Run the chainlink node


	# Example for how to invoke first run. This can also ne used if one would 
	# like to start the node with manual keystore password entry.
	if False: 
		Monitor.run_node("fluxNode2", port = 6688, detached = False)