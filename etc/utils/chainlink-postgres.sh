#!/bin/bash
source .config

psql -p 5432 -h ${DB_NAME} -U ${DB_USER} postgres
