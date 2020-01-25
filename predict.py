import tensorflow as tf
import numpy as np
from text_generation import generate_text

class Prediction:

    def __init__(self,model,vocabulary):
        self.buildModel(model)
        self.loadVocabulary(vocabulary)

    def buildModel(self, model_file):
        self.model = tf.keras.models.load_model(model_file, compile=False)
        self.model.load_weights(model_file)

    def loadVocabulary(self,vocabulary):
        text = open(vocabulary, 'rb').read().decode(encoding='utf-8')
        vocab = sorted(set(text))
        self.char2idx = {u:i for i, u in enumerate(vocab)}
        self.idx2char = np.array(vocab)
        print(self.char2idx)

    def predict(self, prefix):
        return generate_text(self.model,prefix,self.char2idx,self.idx2char)