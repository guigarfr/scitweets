#!/usr/bin/env bash

SLEEP_SECS=10

echo "RHC port-forward command"
rhc port-forward scitweets &>rhc-port-forward.log &
echo "Sleeping for ${SLEEP_SECS} seconds"
sleep ${SLEEP_SECS}

echo "Getting database IP and port..."
export LOCAL_DB_IP=$(grep postgresql rhc-port-forward.log | awk -F "[: ]+" '{print $2}')
export LOCAL_DB_PORT=$(grep postgresql rhc-port-forward.log | awk -F "[: ]+" '{print $3}')
echo -e "\tDatabase Local in ${LOCAL_DB_IP}:${LOCAL_DB_PORT}"
echo -e "\n"

echo "Getting database authentication info..."
export DB_NAME=$(rhc app show scitweets | grep PostgreSQL -A 6 | grep Name | awk '{print $(NF)}')
export DB_USERNAME=$(rhc app show scitweets | grep PostgreSQL -A 6 | grep Username | awk '{print $(NF)}')
export DB_PASSWORD=$(rhc app show scitweets | grep PostgreSQL -A 6 | grep Password | awk '{print $(NF)}')

export OPENSHIFT_POSTGRESQL_DB_URL="postgres://${DB_USERNAME}:${DB_PASSWORD}@${LOCAL_DB_IP}:${LOCAL_DB_PORT}"

echo -e "\tName: ${DB_NAME}"
echo -e "\tUsername: ${DB_USERNAME}"
echo -e "\tPassword: ${DB_PASSWORD}"
echo -e "\n"

echo -e "Database URL: ${OPENSHIFT_POSTGRESQL_DB_URL}\n"


PORT_FORWARD_PROCESS=$(ps ax | grep port-forward | head -n 1 | awk '{print $1}')
kill -9 ${PORT_FORWARD_PROCESS}