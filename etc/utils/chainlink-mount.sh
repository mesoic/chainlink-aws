#!/usr/bin/bash

source .config

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
		IP=3.123.45.56

		echo "BINDING(ropsten): ${IP}"
		echo "PEM(ropsten): ${PEM}"
		;;

	"unmount")
		sudo umount -f /mnt/
		;;	
esac

sudo sshfs -o allow_other,IdentityFile=$PEM ec2-user@$IP:/home/ec2-user/ /mnt/
sleep 1
sudo ssh -i $PEM -4 -L 6687:localhost:6687 -L 6688:localhost:6688  ec2-user@$IP