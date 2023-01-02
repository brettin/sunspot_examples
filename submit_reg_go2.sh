#PBS -l walltime=00:05:00
#PBS -l select=100:system=sunspot
#PBS -l place=scatter
#PBS -l filesystems=eagle:home
#PBS -N reg_go2
#PBS -A CSC249ADOA01
#PBS -q workq

if [ -z "$arg1" ]; then
        echo "arg1 not set, it should be a filename"
	echo "qsub -v arg1=<filename>"
	echo "where <filename> contains input data filenames"
        exit
fi

arg2=$(arg2:-"1")

SYSMON_CMD=/lus/gila/projects/candle_aesp_CNDA/software/tools/pti-gpu/tools/sysmon/build/sysmon
function monitor_gpus {
	while true ; do
		${SYSMON_CMD}
		sleep 10
	done
}

# This should be the directory where qsub was executed
# echo "PBS_O_WORKDIR: $PBS_O_WORKDIR"
cd $PBS_O_WORKDIR

# This file should contain the list of host names
# echo $PBS_NODEFILE
cat $PBS_NODEFILE

# This environment should get passed through mpiexec
export HTTP_PROXY=http://proxy.alcf.anl.gov:3128
export HTTPS_PROXY=http://proxy.alcf.anl.gov:3128
export http_proxy=http://proxy.alcf.anl.gov:3128
export https_proxy=http://proxy.alcf.anl.gov:3128
module load oneapi/release/2022.10.15.003
source $IDPROOT/etc/profile.d/conda.sh
conda activate candle

monitor_gpus &
CHILD_PID=$!

# passing it the file of filenames.
# mpiexec --np 12 ./gpu_tile_compact.sh python ./sunspot_reg_go2.py --infile infiles --ep 2
mpiexec -ppn 12 -n 1 $PBS_O_WORKDIR/sunspot_reg_go2.sh $arg1 $arg1

kill $CHILD_PID
