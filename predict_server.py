from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from prediction_resource import PredictionResource
from webapp_resource import WebAppResource


class PredictServer:
    def __init__(self,prediction):

        app = Flask(__name__)
        api = Api(app)
        api.add_resource(PredictionResource,"/api/predict", resource_class_kwargs={'prediction':prediction})
        api.add_resource(WebAppResource,"/<path:path>")

        app.run()