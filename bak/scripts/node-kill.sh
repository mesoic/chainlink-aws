#!/bin/bash
docker kill ropsten-eth-failover
docker kill ropsten-primary
docker kill ropsten-secondary
docker kill ropsten-alpha-vantage
docker system prune -f
