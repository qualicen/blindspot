import tensorflow as tf
import numpy as np
from text_generation import generate_text

class Prediction:

    def __init__(self,model,vocabulary):
        self.buildModel(model)
        self.loadVocabulary(vocabulary)

    def buildModel(self, model_file):
        json_file = open("{}.json".format(model_file), 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = tf.keras.models.model_from_json(loaded_model_json)
        # load weights into new model
        self.model.load_weights("{}.h5".format(model_file))
#        self.model = tf.keras.models.load_model(model_file, compile=False)
      
    def loadVocabulary(self,vocabulary):
        text = open(vocabulary, 'rb').read().decode(encoding='utf-8')
        vocab = sorted(set(text))
        self.char2idx = {u:i for i, u in enumerate(vocab)}
        self.idx2char = np.array(vocab)

    def predict(self, prefix):
        return generate_text(self.model,prefix,self.char2idx,self.idx2char)
