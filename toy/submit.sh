#PBS -l select=1:system=sunspot
#PBS -l walltime=0:10:00
#PBS -N train
#PBS -A candle_aesp_CNDA 
#PBS -q workq

if [ -z "$arg1" ]; then
        echo "arg1 not set, it should be a filename"
	echo "qsub -v arg1=<filename>"
	echo "where <filename> contains input data filenames"
        exit
fi

arg2=${arg2:-"1"}

# This should be the directory where qsub was executed
# echo "PBS_O_WORKDIR: $PBS_O_WORKDIR"
cd $PBS_O_WORKDIR

# This file should contain the list of host names
# echo $PBS_NODEFILE
cat $PBS_NODEFILE

# General environment settings
export HTTP_PROXY=http://proxy.alcf.anl.gov:3128
export HTTPS_PROXY=http://proxy.alcf.anl.gov:3128
export http_proxy=http://proxy.alcf.anl.gov:3128
export https_proxy=http://proxy.alcf.anl.gov:3128

# Specific environment settings for the python application
module load oneapi/release/2022.10.15.003
source $IDPROOT/etc/profile.d/conda.sh
conda activate candle


# passing it the file of filenames.
echo "arg1 : $arg1"
echo "arg2 : $arg2"
mpiexec -ppn 12 -np 12 $PBS_O_WORKDIR/train.sh $arg1 $arg2

