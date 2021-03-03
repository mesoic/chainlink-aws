#!/bin/bash
sudo systemctl start docker
~/chainlink/ropsten/ropsten-kill.sh
~/chainlink/ropsten/ropsten-boot.sh
