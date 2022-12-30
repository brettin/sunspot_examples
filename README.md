# sunspot_examples
Some basic examples to get running on sunspot


# mpiexec --np 12 gpu_tile_compact.sh python ./sunspot_train.py | grep ZE | sort
 2>/dev/null

ZE_AFFINITY_MASK: 0.0
ZE_AFFINITY_MASK: 0.1
ZE_AFFINITY_MASK: 1.0
ZE_AFFINITY_MASK: 1.1
ZE_AFFINITY_MASK: 2.0
ZE_AFFINITY_MASK: 2.1
ZE_AFFINITY_MASK: 3.0
ZE_AFFINITY_MASK: 3.1
ZE_AFFINITY_MASK: 4.0
ZE_AFFINITY_MASK: 4.1
ZE_AFFINITY_MASK: 5.0                                                       ^C
ZE_AFFINITY_MASK: 5.1
  
# mpiexec --np 6 ./gpu_tile_compact.sh python ./sunspot_train.py | grep ZE | sort 2>/dev/null

ZE_AFFINITY_MASK: 0.0
ZE_AFFINITY_MASK: 0.1
ZE_AFFINITY_MASK: 1.0
ZE_AFFINITY_MASK: 1.1
ZE_AFFINITY_MASK: 2.0
ZE_AFFINITY_MASK: 2.1


mpiexec --np 6 ./gpu_tile_compact.sh python ./sunspot_train.py --infile ./infiles
WARNING:tensorflow:There are non-GPU devices in `tf.distribute.Strategy`, not using nccl allreduce.
WARNING:tensorflow:There are non-GPU devices in `tf.distribute.Strategy`, not using nccl allreduce.
WARNING:tensorflow:There are non-GPU devices in `tf.distribute.Strategy`, not using nccl allreduce.
WARNING:tensorflow:There are non-GPU devices in `tf.distribute.Strategy`, not using nccl allreduce.
WARNING:tensorflow:There are non-GPU devices in `tf.distribute.Strategy`, not using nccl allreduce.
WARNING:tensorflow:There are non-GPU devices in `tf.distribute.Strategy`, not using nccl allreduce.
{'infile': './infiles'}
0: ZE_AFFINITY_MASK: 0.0
0: using tensorflow 2.10.0
0: infile=/lus/gila/projects/candle_aesp_CNDA/brettin/sunspot_examples/ml.3CLPro_7BQY_A_1_F.Orderable_zinc_db_enaHLL.sorted.4col.descriptors.parquet.xform-smiles.csv.reg
None: Number of devices: 1
0: defining and compiling model
0: calling model.fit
0: done calling model.fit
{'infile': './infiles'}
1: ZE_AFFINITY_MASK: 0.1
1: using tensorflow 2.10.0
1: infile=/lus/gila/projects/candle_aesp_CNDA/brettin/sunspot_examples/ml.ADRP_6W02_A_1_H.Orderable_zinc_db_enaHLL.sorted.4col.descriptors.parquet.xform-smiles.csv.reg
None: Number of devices: 1
1: defining and compiling model
1: calling model.fit
1: done calling model.fit
{'infile': './infiles'}
4: ZE_AFFINITY_MASK: 2.0
4: using tensorflow 2.10.0
4: infile=/lus/gila/projects/candle_aesp_CNDA/brettin/sunspot_examples/ml.NPRBD_6VYO_BC_1_F.Orderable_zinc_db_enaHLL.sorted.4col.descriptors.parquet.xform-smiles.csv.reg
None: Number of devices: 1
4: defining and compiling model
4: calling model.fit
4: done calling model.fit
{'infile': './infiles'}
3: ZE_AFFINITY_MASK: 1.1
3: using tensorflow 2.10.0
3: infile=/lus/gila/projects/candle_aesp_CNDA/brettin/sunspot_examples/ml.NPRBD_6VYO_AB_1_F.Orderable_zinc_db_enaHLL.sorted.4col.descriptors.parquet.xform-smiles.csv.reg
None: Number of devices: 1
3: defining and compiling model
3: calling model.fit
3: done calling model.fit
{'infile': './infiles'}
2: ZE_AFFINITY_MASK: 1.0
2: using tensorflow 2.10.0
2: infile=/lus/gila/projects/candle_aesp_CNDA/brettin/sunspot_examples/ml.NPRBD_6VYO_A_1_F.Orderable_zinc_db_enaHLL.sorted.4col.descriptors.parquet.xform-smiles.csv.reg
None: Number of devices: 1
2: defining and compiling model
2: calling model.fit
2: done calling model.fit
{'infile': './infiles'}
5: ZE_AFFINITY_MASK: 2.1
5: using tensorflow 2.10.0
5: infile=/lus/gila/projects/candle_aesp_CNDA/brettin/sunspot_examples/ml.NPRBD_6VYO_CD_1_F.Orderable_zinc_db_enaHLL.sorted.4col.descriptors.parquet.xform-smiles.csv.reg
None: Number of devices: 1
5: defining and compiling model
5: calling model.fit
5: done calling model.fit
