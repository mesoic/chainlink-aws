#!/bin/python 
import os
import json
import collections

class fluxMonitor: 

	# Initialize
	def __init__(self):

		# Open configuration file
		with open('../config/fluxMonitorConfig.json') as json_file:	
	  		self.config = json.load(json_file)

	# Method to programatically generate .env files 
	def generate_env(self): 

		# Create configuration for base
		base_config = {
			"ROOT"					: "/chainlink",
			"LOG_LEVEL" 			: "info",
			"ETH_CHAIN_ID"			: "3",					  # Ropsten
			"ETH_URL"				: "ws://172.17.0.2:4000", # Fiews proxy
			"ALLOW_ORIGINS"			: "*",
			"JSON_CONSOLE"			: "true",
			"LOG_TO_DISK"			: "false",
			"SECURE_COOKIES"		: "false",
			"DATABASE_TIMEOUT"		: "0",
			"CHAINLINK_TLS_PORT"	: "0", 
			"LINK_CONTRACT_ADDRESS"	: "0x20fe562d797a42dcb3399062ae9546cd06f63280",
			"MINIMUM_CONTRACT_PAYMENT" 	 : "1000000000000000", # 0.001 LINK
			"MIN_OUTGOING_CONFIRMATIONS" : "2"
		}

	  	# Configure database URL
	  	postgres_base = "postgresql://%s:%s@%s:%s"%( 
			self.config["cl-database"]["DB_USER"],
			self.config["cl-database"]["DB_PASSWORD"],
			self.config["cl-database"]["DB_ENDPOINT"], 
			self.config["cl-database"]["DB_PORT"] 
	  	)

	  	# Loop through nodes and generate a .env file
	  	for _node in self.config["nodes"]:

	  		# If node file does not exist, create it
	  		if not os.path.exists("../nodes/%s"%(_node)): 
	  			os.makedirs("../nodes/%s"%(_node))

	  		# Get the file pointer
			f = open( "../nodes/%s/.env"%(_node), "w")

			# Write the base configuration
			for k,v in base_config.items(): 
				f.write("%s=%s\n"%(k, v)) 

			# Write node specific data
			f.write("%s=%s\n"%(
				"ORACLE_CONTRACT_ADDRESS",
				self.config["nodes"][_node]["ORACLE_CONTRACT_ADDRESS"]
			))

			f.write("%s=%s/%s\n"%(
				"DATABASE_URL",
				postgres_base, 
				self.config["nodes"][_node]["DB_NAME"]
			))

			f.close()
	
	# Loop through keystore json object and create .passwd files
	def generate_keystore(self):

		with open('../config/fluxMonitorKeystore.json') as json_file:	
			keystore = json.load(json_file)


		# Loop through nodes and generate a .env file
		for _node in self.config["nodes"]:

			f = open( "../nodes/%s/.passwd"%(_node), "w")
			f.write(keystore[_node]["_private"])
			f.close()


	# Method to run EaaS failover proxy docker container.
	# This container must be running prior to running nodes.
	def run_EaaS(self): 

		# Configure Ethereum as a Service (EaaS) endpoints
		EaaS = {

			"fiews"		: "%s/%s"%("wss://cl-ropsten.fiews.io/v1", self.config["EaaS"]["FIEWS_API"]), 
			"infura"	: "%s/%s"%("wss://ropsten.infura.io/ws/v3", self.config["EaaS"]["INFURA_API"]), 
			"linkpool" 	: "wss://ropsten-rpc.linkpool.io/ws"
		}

		# Add endpoints
		EaaS_data = "%s %s %s"%(EaaS["fiews"], EaaS["infura"], EaaS["linkpool"])

		# Construct command 
		cmd = "docker run --detach --restart always --name eaas-failover -p 4000:4000 fiews/cl-eth-failover %s"%(EaaS_data)

		# Run the container
		os.system(cmd)


	# Method to run a node (with AWS cloudwatch logging)
	# When running the node the first time (i.e. when .env points to an existing but empty database), 
	# we need to NOT detach the docker container because we need to interact on the command line.
	# Specifically, we can generate need to generate the eth keypair, username, and password.
	def run_node(self, _node, port, detached = True):

		# Define node root
		_node_dir = os.path.abspath("../nodes/%s"%(_node))

		# Check that the node exists
  		if not os.path.exists(_node_dir): 
  			print("Node (%s) does not exist: Check configuration"%(_node))
  			return

  		# Normal runtime
  		if detached:	
	
			# primary container (chainlink node)
			cmd  = "docker run --detach --restart always --name %s -it -p %s:%s "%(_node, port, port)
			cmd += "--log-driver=\"awslogs\" --log-opt awslogs-group=\"chainlink-logging-group\" --log-opt awslogs-stream=\"%s\" "%(_node)
			cmd += "-v %s:/chainlink --env-file=%s/.env smartcontract/chainlink local node -p /chainlink/.passwd"%(_node_dir, _node_dir)

			print(cmd)
		
		# First run
		else:

			cmd = "docker run -it -p %s:%s "%(port, port)
			cmd += "-v %s:/chainlink --env-file=%s/.env smartcontract/chainlink local node"%(_node_dir, _node_dir)

			print(cmd)		

		os.system(cmd)

	# Method to halt EaaS
	def kill_container(self, _name):

		os.system("docker kill %s"%(_name))
		os.system("docker system prune -f")


if __name__ == "__main__": 

	# Create an instace of the flux monitor
	fm = fluxMonitor()

	# Runs a single node in the flux 
	fm.run_single("fluxNode0")
