from training import Training
import sys
import json
import codecs
from predict import Prediction
import numpy as np
from predict_server import PredictServer

np.random.seed(7)

if len(sys.argv)<3:
  print("Usage blindspot data-file parameter-file test-suffix")
  exit()
  
mode = sys.argv[1]
if mode == "train":
  data_file = sys.argv[2]
  parameter_file = sys.argv[3]
  examples_file = sys.argv[4]

  with codecs.open(parameter_file,'r','utf-8') as f:
    params = json.load(f)

  with codecs.open(examples_file,'r','utf-8') as f:
    examples = json.load(f)


  t = Training(data_file=data_file,examples=examples)

  for p in params:
    print("Trying:{}".format(p))
    t.train(**p)

if mode == "predict":
  vocab_file = sys.argv[2]
  model_file = sys.argv[3]
  text = sys.argv[4]
  p = Prediction(model_file,vocab_file)
  print(p.predict(text))


if mode == "predict_server":
  vocab_file = sys.argv[2]
  model_file = sys.argv[3]
  p = Prediction(model_file,vocab_file)
  PredictServer(p)
