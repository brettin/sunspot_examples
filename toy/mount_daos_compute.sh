#!/bin/bash
#
#

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <argument>"
  echo "Please provide exactly one argument. num nodes passed to mpiexec"
  exit 1
fi

n=$1

launch-dfuse.sh ${DAOS_POOL_NAME}:${DAOS_CONT_NAME}
mpiexec -n $n -ppn 1 ls -l /tmp/$DAOS_POOL/$DAOS_CONT
