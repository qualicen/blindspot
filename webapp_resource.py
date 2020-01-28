from flask_restful import Resource
from flask import send_from_directory

class WebAppResource(Resource):
    
    def get(self,path):
        return send_from_directory('./webapp/dist/webapp', path)
