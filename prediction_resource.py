from flask import request
from flask_restful import Resource

class PredictionResource(Resource):

    def __init__(self,**kwargs):
        self.prediction=kwargs['prediction']
    
    def get(self):
        word = request.args.get("word")
        description_raw = self.prediction.predict("\n{}|".format(word))
        description = description_raw[description_raw.index("|")+1:description_raw.index("\n",1)]
        return description,200

