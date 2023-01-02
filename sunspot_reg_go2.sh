#!/bin/bash

INFILE=$arg1
EP=$arg2

SYSMON_CMD=/lus/gila/projects/candle_aesp_CNDA/software/tools/pti-gpu/tools/sysmon/build/sysmon

function monitor_gpus {
	while true ; do
		${SYSMON_CMD}
		sleep 10
	done
}

monitor_gpus &
CHILD_PID=$!

./gpu_tile_compact.sh python ./sunspot_reg_go2.py --infile $INFILES --ep $EP

kill $CHILD_PID
