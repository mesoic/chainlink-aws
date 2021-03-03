#!/bin/python
import modules.chainlinkDeployer as clDeployer

if __name__ == "__main__": 

	# Initilize deployer
	Deployer = clDeployer.chainlinkDeployer()

	# Run the chainlink nodes
	Deployer.run_EaaS()
	Deployer.run_node("fluxNode0", port = 6686, detached = True)
	Deployer.run_node("fluxNode1", port = 6687, detached = True)
	Deployer.run_node("fluxNode2", port = 6688, detached = True)
