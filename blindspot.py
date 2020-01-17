from training import Training
import sys
import json
import codecs

if len(sys.argv)<3:
  print("Usage blindspot data-file parameter-file test-suffix")
  exit()
  
data_file = sys.argv[1]
parameter_file = sys.argv[2]
examples_file = sys.argv[3]


with codecs.open(parameter_file,'r','utf-8') as f:
  params = json.load(f)

with codecs.open(examples_file,'r','utf-8') as f:
  examples = json.load(f)


t = Training(data_file=data_file,examples=examples)

for p in params:
  print("Trying:{}".format(p))
  t.train(**p)

