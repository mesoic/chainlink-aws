#!/bin/python
import modules.chainlinkDeployer as clDeployer

if __name__ == "__main__": 

	# Initilize network
	Deployer = clDeployer.chainlinkDeployer()

	# Stop continers
	Deployer.kill_container("eaas-failover")
	Deployer.kill_container("fluxNode0")
	Deployer.kill_container("fluxNode1")
	Deployer.kill_container("fluxNode2")