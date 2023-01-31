import sys
import os

ZE_AFFINITY_MASK =os.environ.get('ZE_AFFINITY_MASK')
PMIX_RANK        =os.environ.get('PMIX_RANK')

# read filenames from infile
with open(sys.argv[1]) as infile:
    lines = [line.rstrip() for line in infile]
infile.close()

# Add a guard on index out of bounds.
#if len(lines) > NUM_RANKS:
infile=lines[int(PMIX_RANK)]

print('ZE_AFFINITY_MASK: {}\tPMIX_RANK {}\tinfile: {}'.format(ZE_AFFINITY_MASK, PMIX_RANK, infile))
