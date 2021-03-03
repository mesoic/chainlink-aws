#!/bin/python
import modules.chainlinkDeployer as clDeployer

if __name__ == "__main__": 

	# Initilize deployer
	Deployer = clDeployer.chainlinkDeployer()

	# Auto-generate .env files 
	Deployer.generate_env()

	# Auto-generate .passwd files
	Deployer.generate_keystore()