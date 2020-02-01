from flask import request
from flask_restful import Resource

class PredictionResource(Resource):

    def __init__(self,**kwargs):
        self.prediction=kwargs['prediction']
    
    def get(self):
        word = request.args.get("word")
	temperature = float(request.args.get("temperature",0.1))
        #print(word)
        description_raw = self.prediction.predict("\n{}|".format(word),temperature)
        #print(description_raw)
        upper = description_raw.find("\n",1)
        if upper < 0: 
            upper = len(description_raw)
        description = description_raw[description_raw.index("|")+1:upper]
        return description,200

