from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from prediction_resource import PredictionResource
from lookup_resource import LookupResource
from webapp_resource import WebAppResource


class PredictServer:
    def __init__(self,prediction,lookup_database):

        app = Flask(__name__)
        api = Api(app)
        api.add_resource(PredictionResource,"/api/predict", resource_class_kwargs={'prediction':prediction})
        api.add_resource(LookupResource,"/api/lookup", resource_class_kwargs={'database':lookup_database})
        api.add_resource(WebAppResource,"/<path:path>")

        app.run(host= '0.0.0.0')
