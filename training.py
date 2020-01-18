# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'

from  text_generation import generate_text
import tensorflow as tf

import re
import numpy as np
import codecs
import shutil
from math import floor


# No of empocs to train
EPOCHS=150

# Batch size
BATCH_SIZE = 64

# Buffer size to shuffle the dataset
# (TF data is designed to work with possibly infinite sequences,
# so it doesn't attempt to shuffle the entire sequence in memory. Instead,
# it maintains a buffer in which it shuffles elements).
BUFFER_SIZE = 10000

class Training:

  def __init__(self,data_file,examples):
    self.data_file=data_file
    self.examples = examples

  def split_input_target(self,chunk):
      input_text = chunk[:-1]
      target_text = chunk[1:]
      return input_text, target_text


  def loss(self,labels, logits):
    return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)
    


  def build_model(self,batch_size):
    layers=[]
    layers.append(tf.keras.layers.Embedding(self.vocab_size, self.embedding_dim,batch_input_shape=[batch_size, None]))
    if self.dropout_ratio>0:
      layers.append(tf.keras.layers.Dropout(self.dropout_ratio))
    for _ in range(0,self.number_of_layers):
      layers.append(tf.keras.layers.LSTM(self.hidden_size, return_sequences=True,stateful=True,recurrent_dropout=self.recurrent_dropout_ratio))
    if self.dropout_ratio>0:
      layers.append(tf.keras.layers.Dropout(self.dropout_ratio))
    layers.append(tf.keras.layers.Dense(self.vocab_size))
    model = tf.keras.Sequential(layers)
    return model

  def prepareData(self):
    self.text = open(self.data_file, 'rb').read().decode(encoding='utf-8')
    self.vocab = sorted(set(self.text))
    self.char2idx = {u:i for i, u in enumerate(self.vocab)}
    self.idx2char = np.array(self.vocab)
    text_as_int = np.array([self.char2idx[c] for c in self.text])
    # Create training examples / targets
    char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)
    sequences = char_dataset.batch(self.seq_length+1, drop_remainder=True)
    dataset = sequences.map(self.split_input_target)
    dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)
    size = floor(floor(text_as_int.size / (self.seq_length+1)) / BATCH_SIZE)
    
    split_point = int(0.9*size)
	
    self.train_set = dataset.take(split_point)
    self.val_set = dataset.skip(split_point)

    # Length of the vocabulary in chars
    self.vocab_size = len(self.vocab)

  def train(self,id, seq_length,hidden_size,embedding_dim,number_of_layers,dropout_ratio,recurrent_dropout_ratio,optimizer):

    self.seq_length = seq_length
    self.hidden_size=hidden_size
    self.embedding_dim = embedding_dim
    self.number_of_layers=number_of_layers
    self.dropout_ratio = dropout_ratio
    self.recurrent_dropout_ratio=recurrent_dropout_ratio
    self.optimizer=optimizer
    self.id=id
    self.outputDir='./{}'.format(id)
    self.checkpointDir='{}/checkpoints'.format(self.outputDir)
    try:
      os.mkdir(self.outputDir,)
    except OSError as error:
      print('Ouptut Dir already exists.') 
    self.prepareData()

    model = self.build_model(BATCH_SIZE)
    model.compile(optimizer=self.optimizer, loss=self.loss, metrics=[tf.keras.metrics.SparseCategoricalAccuracy()])

    # Name of the checkpoint files
    checkpoint_prefix = os.path.join(self.checkpointDir, "ckpt_{epoch}")

    checkpoint_callback=tf.keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_prefix,
        save_weights_only=True,
        save_best_only=True,
        monitor='val_loss',
        verbose=1
        )
    stop_callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=4)



    history = model.fit(self.train_set, validation_data=self.val_set, epochs=EPOCHS, callbacks=[checkpoint_callback, stop_callback])
    model = self.build_model(batch_size=1)
    model.load_weights(tf.train.latest_checkpoint(self.checkpointDir))
    model.build(tf.TensorShape([1, None]))
    model.save('{}/model.h5'.format(self.outputDir))

    f=codecs.open('{}/output_examples.txt'.format(self.outputDir),"w","utf-8")

    f.write("id={},\n"
      "seq_length={},\n"
      "hidden_size={},\n"
      "embedding_dim={},\n"
      "number_of_layers={},\n"
      "dropout_ratio={},\n"
      "recurrent_dropout_ratio={},\n" 
      "optimizer={},\n"
      "history={}\n"
      "\n==============================\n\n".format(self.id,self.seq_length, self.hidden_size, 
        self.embedding_dim, self.number_of_layers, self. dropout_ratio, 
        self.recurrent_dropout_ratio,self.optimizer,history.history))


    for ex in self.examples:
      f.write(generate_text(model, ex, self.char2idx, self.idx2char))
      f.write("\n")

    f.close()
    shutil.rmtree(self.checkpointDir)


  