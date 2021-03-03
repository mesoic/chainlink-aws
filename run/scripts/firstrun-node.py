#!/bin/python
import modules.chainlinkDeployer as clDeployer

if __name__ == "__main__": 

	# Initilize network
	Deployer = clDeployer.chainlinkDeployer()

	# Run the chainlink node
	# Example for how to invoke first run. This can also ne used if one would 
	# like to start the node with manual keystore password entry.
	Deployer.run_node("fluxNode2", port = 6688, detached = False)