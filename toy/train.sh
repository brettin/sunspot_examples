#!/bin/bash

arg1=$1
arg2=$2

INFILE=$arg1
EP=$arg2

SYSMON_CMD=/lus/gila/projects/candle_aesp_CNDA/software/tools/pti-gpu/tools/sysmon/build/sysmon

function monitor_gpus {
	while true ; do
		${SYSMON_CMD}
		sleep 10
	done
}

# still not working
#if [[ $(( ${PMIX_RANK} % 12)) == 0 ]] ; then
#	monitor_gpus > ${PMIX_RANK}-sysmon.log &
#	CHILD_PID=$!
#fi

# set up local logging
# LOCALDIR=/scratch}

./gpu_tile_compact.sh python train.py $INFILE


# move local logs to shared filesystem
# DEST_DIR = ${PBS_JOBID}/$(hostname)
# mkdir -p ${DEST_DIR}
# cp -r $LOCAL_DIR/* ${DEST_DIR}/


# This too is not working, probably because CHILD_PID is not set.
# kill -n 9 $CHILD_PID
