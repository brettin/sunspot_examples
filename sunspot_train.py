import argparse
psr = argparse.ArgumentParser(description="input dataframe file")
psr.add_argument("--infile", default="infile", help="a file of filenames indexed with world rank")
args = vars(psr.parse_args())
print(args)


import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
print('{}: ZE_AFFINITY_MASK: {}'.format(os.getenv('PMIX_RANK'), os.environ['ZE_AFFINITY_MASK']))


import tensorflow as tf
from tensorflow import keras
print('{}: using tensorflow {}'.format(os.getenv('PMIX_RANK'), tf.__version__))


with open(args['infile']) as infile:
    lines = [line.rstrip() for line in infile]
print("{}: infile={}".format(os.getenv('PMIX_RANK'),lines[ int(os.getenv('PMIX_RANK')) ] ))



strategy = tf.distribute.MirroredStrategy()
print('{}: Number of devices: {}'.format(os.getenv('PMIXX_RANK'), strategy.num_replicas_in_sync))

with strategy.scope():
    print("{}: defining and compiling model".format(os.getenv('PMIX_RANK')))
    # your model is defined here
    # your model is compiled here

print("{}: calling model.fit".format(os.getenv('PMIX_RANK')))
# define call backs
# call model.fit

print("{}: done calling model.fit".format(os.getenv('PMIX_RANK')))
