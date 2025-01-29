#!/bin/bash
#
#

cd /tmp/${DAOS_POOL}/${DAOS_CONT}

for i in $(seq 1 4) ; do
	COUNT=$((10**$i)) ;
	CMD="time dd if=/dev/zero of=./$(hostname).filename.$COUNT bs=1M count=$COUNT" ;
	echo $CMD ;
	$CMD ;
done

