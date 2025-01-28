import sys
import os

ZE_AFFINITY_MASK =os.environ.get('ZE_AFFINITY_MASK')
PMIX_RANK        =os.environ.get('PMIX_RANK')

# mount a daos container. this assumes that the pool and container
# already exists.
DAOS_CONT=os.environ.get('DAOS_CONT') or DAOS_CONT="brettin_posix"
DAOS_POOL=os.environ.get('DAOS_POOL') or DAOS_POOL="candle_aesp_CNDA"
mount_point = os.path.join("/tmp", DAOS_POOL, DAOS_CONT)  # Replace with your mount point
try:
  os.system("daos container mount --pool=DAOS_POOL --cont=DAOS_CONT /mnt/daos")
except Exception as e:
  print(e)

# read the infile from the mount. the infile arg should be relative to the
# mount point root

infile_path = os.path.join(mount_point, sys.argv[1])
with open(infile_path) as infile:
    lines = [line.rstrip() for line in infile]
infile.close()

# get the infile filename for this rank
infile=lines[int(PMIX_RANK)]

# print output to daos container mount
outfile_path = os.path.join(mount_point, f'{infile}.out')
with open(outfile_path) as o:
  print(f'ZE_AFFINITY_MASK: {ZE_AFFINITY_MASK}\tPMIX_RANK {PMIX_RANK}\tinfile: {infile_path}')
o.close()
