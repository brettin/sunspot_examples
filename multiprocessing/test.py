import datetime
import os
import socket
host=socket.gethostname()

from multiprocessing import Pool
# import uno_baseline_keras2.py

def f(x):

    pals_rank = os.environ['PALS_RANKID']
    pals_local_rank = os.environ['PALS_LOCAL_RANKID']
    pals_local_size = os.environ['PALS_LOCAL_SIZE']
    #ze_affinity_mask = os.environ['ZE_AFFINITY_MASK']
    pbs_jobid = os.environ['PBS_JOBID']

    # for ZE_AFFINITY_MASK
    num_tile=2
    num_gpu=6
    tile = x % num_tile
    gpu  = int(x / num_tile) % num_gpu
    ze_affinity_mask = f'{gpu}.{tile}'
    print(f'x: {x}\t',
          f'host: {host}\t',
          f'pals_rank: {pals_rank}\t',
          f'pals_local_rank: {pals_local_rank}\t',
          f'pals_local_size: {pals_local_size}\t',
          f'pbs_jobid: {pbs_jobid}\t',
          f'ze_affinity_maks: {ze_affinity_mask}\t',
          )

    os.environ{'ZE_AFFINITY_MASK'} = ze_affinity_mask
    uno_baseline_keras2.py.main()

    return x

if __name__ == '__main__':
    with Pool(12) as p:
        for n in range(12):
            print(p.map(f, [n]))
