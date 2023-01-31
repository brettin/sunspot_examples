from data_loader import load_data_from_parquet
from data_loader import load_data
from tensorflow import keras

from datetime import datetime as dt
import tensorflow as tf
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.models import Model, model_from_json, model_from_yaml
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.callbacks import (
    CSVLogger,
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau,
)
from tensorflow.keras import backend as K
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import tensorflow.keras as ke
import matplotlib.pyplot as plt
import argparse
import math
import os
import matplotlib
import numpy as np
import pandas as pd

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# The model should not know about rank. Refactor
# so that the specific infile is determined in bash.
PMIX_RANK = os.getenv('PMIX_RANK')

psr = argparse.ArgumentParser(description="input dataframe file")
psr.add_argument("--infile", default="infile",
                 help="a file of filenames indexed with world rank")
psr.add_argument("--ep", type=int, default=400)
args = vars(psr.parse_args())
print(args)

strategy = tf.distribute.MirroredStrategy()
print('{}: Number of devices: {}'.format(
    PMIX_RANK, strategy.num_replicas_in_sync))

EPOCH = args["ep"]
BATCH = 32
GLOBAL_BATCH_SIZE = BATCH * strategy.num_replicas_in_sync
DR = 0.1  # Dropout rate

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
print('{}: ZE_AFFINITY_MASK: {}'.format(
    PMIX_RANK, os.environ['ZE_AFFINITY_MASK']))


print('{}: using tensorflow {}'.format(PMIX_RANK, tf.__version__))


def r2(y_true, y_pred):
    SS_res = K.sum(K.square(y_true - y_pred))
    SS_tot = K.sum(K.square(y_true - K.mean(y_true)))
    return 1 - SS_res / (SS_tot + K.epsilon())


with open(args['infile']) as infile:
    lines = [line.rstrip() for line in infile]

# Add a guard on index out of bounds.
print("{}: infile={}".format(PMIX_RANK,
      lines[int(PMIX_RANK)]))

# Add a guard on index out of bounds.
X_train, Y_train, X_test, Y_test = load_data_from_parquet(
    lines[int(PMIX_RANK)])
# X_train, Y_train, X_test, Y_test = load_data(
#     lines[int(PMIX_RANK)])
input_dim = X_train.shape[1]

steps = X_train.shape[0]//GLOBAL_BATCH_SIZE
validation_steps = X_test.shape[0]//GLOBAL_BATCH_SIZE
train_ds = tf.data.Dataset.from_tensor_slices(
    (X_train, Y_train)).batch(GLOBAL_BATCH_SIZE,
                              drop_remainder=True,
                              num_parallel_calls=None,
                              deterministic=None,).repeat(EPOCH)
val_ds = tf.data.Dataset.from_tensor_slices(
    (X_test, Y_test)).batch(GLOBAL_BATCH_SIZE,
                            drop_remainder=True,
                            num_parallel_calls=None,
                            deterministic=None,).repeat(EPOCH)

options = tf.data.Options()
options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.DATA
train_ds = train_ds.with_options(options)
val_ds = val_ds.with_options(options)

# for tensorflow.distribute.MirroredStrategy
train_dist = strategy.experimental_distribute_dataset(train_ds)
val_dist = strategy.experimental_distribute_dataset(val_ds)

with strategy.scope():
    print("{}: defining and compiling model".format(PMIX_RANK))
    inputs = Input(shape=(input_dim,))
    x = Dense(250, activation="relu")(inputs)
    x = Dropout(DR)(x)
    x = Dense(125, activation="relu")(x)
    x = Dropout(DR)(x)
    x = Dense(60, activation="relu")(x)
    x = Dropout(DR)(x)
    x = Dense(30, activation="relu")(x)
    x = Dropout(DR)(x)
    outputs = Dense(1, activation="relu")(x)

    model = Model(inputs=inputs, outputs=outputs)
    model.summary()

    model.compile(
        loss="mean_squared_error",
        optimizer=SGD(lr=0.0001, momentum=0.9),
        metrics=["mae", r2],
    )


# define call backs
checkpointer = ModelCheckpoint(
    filepath="{}-reg_go.autosave.model.h5".format(PMIX_RANK),
    verbose=1,
    save_weights_only=False,
    save_best_only=True,
)
csv_logger = CSVLogger("{}-reg_go.training.log".format(PMIX_RANK))
reduce_lr = ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.75,
    patience=20,
    verbose=1,
    mode="auto",
    epsilon=0.0001,
    cooldown=3,
    min_lr=0.000000001,
)
early_stop = EarlyStopping(
    monitor="val_loss", patience=100, verbose=1, mode="auto")

# call model.fit
print("{}: {} calling model.fit".format(PMIX_RANK, dt.fromtimestamp(
    dt.timestamp(dt.now())).strftime("%D %H:%M:%S.%s")))
history = model.fit(
    train_dist,
    batch_size=GLOBAL_BATCH_SIZE,
    steps_per_epoch=int(steps),
    epochs=EPOCH,
    verbose=1,
    validation_data=val_dist,
    validation_steps=validation_steps,
    callbacks=[checkpointer, csv_logger, reduce_lr, early_stop],
)
print("{}: {} done calling model.fit".format(PMIX_RANK, dt.fromtimestamp(
    dt.timestamp(dt.now())).strftime("%D %H:%M:%S.%s")))

print("{}: {} calling model.evaluate".format(PMIX_RANK, dt.fromtimestamp(
    dt.timestamp(dt.now())).strftime("%D %H:%M:%S.%s")))

score = model.evaluate(X_test, Y_test, verbose=0)

print("{}: {} done calling model.evaluate".format(PMIX_RANK, dt.fromtimestamp(
    dt.timestamp(dt.now())).strftime("%D %H:%M:%S.%s")))

for metric_name,value in zip(model.metrics_names, score):
    print('{}: {} {}'.format(PMIX_RANK, metric_name, value))
