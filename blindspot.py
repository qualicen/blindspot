from training import Training
import sys
import json
import codecs
from predict import Prediction
import numpy as np
from predict_server import PredictServer

def get_database_from_file(data_file):
  db={}
  dbcontent = codecs.open(data_file,'r',encoding='utf-8')
  for line in dbcontent:
    if '|' in line:
      word,ex = line.split('|',maxsplit=1)
      db[word.lower()]=ex.strip()
  return db


np.random.seed(7)

if len(sys.argv)<3:
  print("Usage blindspot data-file parameter-file test-suffix")
  exit()
  
mode = sys.argv[1]
if mode == "train" or mode=="onlyexport":
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
    p["only_export"]=(mode=="onlyexport")
    t.train(**p)

if mode == "predict":
  vocab_file = sys.argv[2]
  model_file = sys.argv[3]
  text = sys.argv[4]
  p = Prediction(model_file,vocab_file)
  print(p.predict(text))


if mode == "predict_server":
  data_file = sys.argv[2]
  model_file = sys.argv[3]
  p = Prediction(model_file,data_file)
  db = get_database_from_file(data_file)
  PredictServer(p,db)


