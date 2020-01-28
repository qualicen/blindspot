# -*- coding: utf-8 -*-

from __future__ import print_function

import tensorflow as tf
import numpy as np

data_path = './data/wordMeanings.txt'

batch_size = 64  # Batch size for training.
epochs = 20  # Number of epochs to train for.
latent_dim = 1024  # Latent dimensionality of the encoding space.
num_samples = 20000  # Number of samples to train on.
embedding_dim = 256

class TrainingEncDec:

    
    def loss(self,labels, logits):
        return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)

    def prepareTexts(self):
        # Vectorize the data.
        self.input_texts = []
        self.target_texts = []
        characters = set()
        with open(data_path, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
        for line in lines[: min(num_samples, len(lines) - 1)]:
            #print(line)
            input_text, target_text= line.split('|',maxsplit=1)
            # We use "tab" as the "start sequence" character
            # for the targets, and "\n" as "end sequence" character.
            target_text = '|' + target_text + '\n'
            self.input_texts.append(input_text)
            self.target_texts.append(target_text)
            for char in input_text:
                if char not in characters:
                    characters.add(char)
            for char in target_text:
                if char not in characters:
                    characters.add(char)

        self.characters = sorted(list(characters))
        self.num_tokens = len(characters)
        self.max_encoder_seq_length = max([len(txt) for txt in self.input_texts])
        self.max_decoder_seq_length = max([len(txt) for txt in self.target_texts])

        print('Number of samples:', len(self.input_texts))
        print('Number of unique tokens:', self.num_tokens)
        print('Max sequence length for inputs:', self.max_encoder_seq_length)
        print('Max sequence length for outputs:', self.max_decoder_seq_length)

        self.token_index = dict(
            [(char, i) for i, char in enumerate(characters)])

    def prepareInput(self):
        self.encoder_input_data = np.zeros(
            (len(self.input_texts), self.max_encoder_seq_length),
            dtype='float32')
        self.decoder_input_data = np.zeros(
            (len(self.input_texts), self.max_decoder_seq_length),
            dtype='float32')
        self.decoder_target_data = np.zeros(
            (len(self.input_texts), self.max_decoder_seq_length),
            dtype='float32')

        for i, (input_text, target_text) in enumerate(zip(self.input_texts, self.target_texts)):
            for t, char in enumerate(input_text):
                self.encoder_input_data[i, t] = self.token_index[char]
            self.encoder_input_data[i, t + 1:] = self.token_index[' ']
            for t, char in enumerate(target_text):
                # decoder_target_data is ahead of decoder_input_data by one timestep
                self.decoder_input_data[i, t]  = self.token_index[char]
                if t > 0:
                    # decoder_target_data will be ahead by one timestep
                    # and will not include the start character.
                    self.decoder_target_data[i, t - 1] = self.token_index[char]
            self.decoder_input_data[i, t + 1:] = self.token_index[' ']
            self.decoder_target_data[i, t:] = self.token_index[' ']
    
    def buildModel(self):

        # Define an input sequence and process it.
        encoder_inputs = tf.keras.Input(shape=(None,))
        embedding = tf.keras.layers.Embedding(self.num_tokens, embedding_dim,batch_input_shape=[batch_size, None])
        encoder = tf.keras.layers.LSTM(latent_dim, return_state=True)
        encoder_outputs, state_h, state_c = encoder(embedding(encoder_inputs))
        # We discard `encoder_outputs` and only keep the states.
        encoder_states = [state_h, state_c]

        # Set up the decoder, using `encoder_states` as initial state.
        decoder_inputs = tf.keras.Input(shape=(None,))
        # We set up our decoder to return full output sequences,
        # and to return internal states as well. We don't use the
        # return states in the training model, but we will use them in inference.
        decoder_lstm = tf.keras.layers.LSTM(latent_dim, return_sequences=True, return_state=True)
        decoder_outputs, _, _ = decoder_lstm(embedding(decoder_inputs),
                                            initial_state=encoder_states)
        decoder_dense = tf.keras.layers.Dense(self.num_tokens, activation='softmax')
        decoder_outputs = decoder_dense(decoder_outputs)

        # Define the model that will turn
        # `encoder_input_data` & `decoder_input_data` into `decoder_target_data`
        model = tf.keras.Model([encoder_inputs, decoder_inputs], decoder_outputs)

        # Run training
        model.compile(optimizer='rmsprop', loss=tf.keras.losses.categorical_crossentropy,
                    metrics=['accuracy'])
        model.fit([self.encoder_input_data, self.decoder_input_data], self.decoder_target_data,
                batch_size=batch_size,
                epochs=epochs,
                validation_split=0.2)
        # Save model
        model.save('s2s.h5')


training=TrainingEncDec()
training.prepareTexts()
training.prepareInput()
training.buildModel()

# Next: inference mode (sampling).
# Here's the drill:
# 1) encode input and retrieve initial decoder state
# 2) run one step of decoder with this initial state
# and a "start of sequence" token as target.
# Output will be the next target token
# 3) Repeat with the current target token and current states

# Define sampling models
