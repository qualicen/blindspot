from flask import request
from flask_restful import Resource

class LookupResource(Resource):

    def __init__(self,**kwargs):
        self.database=kwargs['database']

    
    def get(self):
        word = request.args.get("word")
        key = word.lower()
        if key in self.database.keys():
            return self.database[key],200
        else:
            return '',200
