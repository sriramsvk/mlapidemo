from flask import Flask
from flask_restful import Api # for linking resources with end points
from API.ImageClassapi import ImagePredictClass
from API.enrollreviewapi import enrollstatus
from API.utreviewapi import UTreviewpredict
from flask_bootstrap import Bootstrap
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='8a40d4233974a1591b2a67349642ed35'
    api = Api(app)
    # end points for About API and image classification
    api.add_resource(ImagePredictClass,'/Image')
    api.add_resource(enrollstatus,'/Enrollmentreview')
    api.add_resource(UTreviewpredict, '/Utilizationreview')
    from API.main.routes import main
    app.register_blueprint(main)
    return app

