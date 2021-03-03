#!/bin/python

import modules.chainlinkDeployer as clDeployer

if __name__ == "__main__": 

	Deployer = clDeployer.chainlinkDeployer()
	Deployer.generate_env()
	Deployer.generate_keystore()