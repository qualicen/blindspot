from flask import Flask
from flask_restful import Api, Resource, reqparse
from prediction_resource import PredictionResource


class PredictServer:
    def __init__(self,prediction):
        app = Flask(__name__)
        api = Api(app)

        api.add_resource(PredictionResource,"/predict", resource_class_kwargs={'prediction':prediction})

        app.run()