from flask import request
from flask_restful import Resource

class PredictionResource(Resource):

    def __init__(self,**kwargs):
        self.prediction=kwargs['prediction']
    
    def get(self):
        word= request.args.get("word")
        return self.prediction.predict("{}|".format(word)),200

