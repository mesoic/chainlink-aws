#!/bin/sh
source ~/.bash_profile

# Source configuration data
source .node/.config

#########################################################
# 		Step 1: Boot EaaS Failover Proxy Server 		#
#########################################################

# EaaS setup information
FIEWS_WSS=wss://cl-ropsten.fiews.io/v1/${FIEWS_API}

# Infura
INFURA_WSS=wss://ropsten.infura.io/ws/v3/${INFURA_API}

# Linkpool
LINKPOOL_WSS=wss://ropsten-rpc.linkpool.io/ws

# Boot the EaaS proxy
docker run --detach --restart always --name ropsten-eth-failover -p 4000:4000 fiews/cl-eth-failover ${FIEWS_WSS} ${INFURA_WSS} ${LINKPOOL_WSS}

# Sleep (for docker container start)
sleep 3

# Set ETH_URL environment varirable to contain the IP
ETH_URL=`echo $(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ropsten-eth-failover)`
ETH_URL="ws://${ETH_URL}:4000"

#########################################################
# 		Step 2: Write chainlink .env config file 		#
#########################################################

# Write .env file
echo "ROOT=/chainlink
LOG_LEVEL=info
ETH_CHAIN_ID=3
MIN_OUTGOING_CONFIRMATIONS=2
LINK_CONTRACT_ADDRESS=${LINK_CONTRACT_ADDRESS}
ORACLE_CONTRACT_ADDRESS=${ORACLE_CONTRACT_ADDRESS}
MINIMUM_CONTRACT_PAYMENT=${MINIMUM_CONTRACT_PAYMENT}
CHAINLINK_TLS_PORT=0
SECURE_COOKIES=false
ALLOW_ORIGINS=*
ETH_URL=${ETH_URL}
JSON_CONSOLE=true
LOG_TO_DISK=false
DATABASE_URL=postgresql://${DB_USERNAME}:${DB_PASSWORD}@${DB_ENDPOINT}:${DB_PORT}/${DB_DATABASE}
DATABASE_TIMEOUT=0" > .node/.env

# Cat configuration file after writing
# cat ~/.chainlink-ropsten/.env

#########################################################
# 		Step 3: Set up logging and boot the node 		#
#########################################################

# Create instance timestamp for unique logging stream
CL_INSTANCE=`echo $(ec2-metadata -i) | awk '{split($0,a," "); print a[2]}'`
CL_TIMESTAMP="$(date +%s)"

# Chainlink setup information
CL_PWD="/chainlink/.password"

# primary container (chainlink)
docker run --detach --restart always --name ropsten-primary -it -p 6688:6688 --log-driver="awslogs" --log-opt awslogs-group="chainlink-logging-group" --log-opt awslogs-stream="ropsten-primary-${CL_INSTANCE}-${CL_TIMESTAMP}" -v ~/chainlink/ropsten/.node:/chainlink --env-file=.node/.env smartcontract/chainlink local node -p $CL_PWD
