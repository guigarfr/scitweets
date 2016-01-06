#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Dir is $DIR"

echo "RHC port-forward command"
rhc port-forward scitweets > ${DIR}/rhc-port-forward.log
