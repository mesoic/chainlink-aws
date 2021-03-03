#!/usr/bin/bash
source .config

# Script to remotely mount this instance on a local machine and correctly forward ports
KEYRING=${KEYRING}
case "$1" in

	"mainnet")
		PEM=${KEYRING}/chainlink-mainnet.pem
		IP=${MAINNET_IP}

		echo "BINDING(mainnet): ${IP}"
		echo "PEM(mainnet): ${PEM}"
		;;

	"ropsten")
		PEM=${KEYRING}/chainlink-ropsten.pem
		IP=${ROPSTEN_IP}

		echo "BINDING(ropsten): ${IP}"
		echo "PEM(ropsten): ${PEM}"
		;;

	"failover")
		PEM=${KEYRING}/chainlink-failover.pem
		IP=${FAILOVER_IP}

		echo "BINDING(failover): ${IP}"
		echo "PEM(failover): ${PEM}"
		;;

	"flux-monitor")	
		PEM=${KEYRING}/chainlink-flux-monitor.pem
		IP=${FAILOVER_IP}

		echo "BINDING(flux-monitor): ${IP}"
		echo "PEM(flux-monitor): ${PEM}"
		;;

	"unmount")
		sudo umount -f /mnt/
		;;	
esac

# mount the filesystem 
sudo sshfs -o allow_other,IdentityFile=$PEM ec2-user@$IP:/home/ec2-user/ /mnt/
sleep 1

# ssh into the instance
sudo ssh -i $PEM -4 -L 6686:localhost:6686 -L 6687:localhost:6687 -L 6688:localhost:6688  ec2-user@$IP