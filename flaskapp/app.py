import os

from flask import Flask
from flask_restful import Api

from flaskapp.DAO.elasticsearch import ESClient

from flaskapp.routes.verify_text import VerifyText
from flaskapp.routes.register_answer import RegisterAnswer

user = os.getenv('user')
password = os.getenv('password')
host = os.getenv('host')

app = Flask(__name__)

es_client = ESClient(user, password, host)

api = Api(app)

api.add_resource(VerifyText,
                 '/receive_data',
                 resource_class_kwargs={'es_client': es_client})

api.add_resource(RegisterAnswer,
                 '/register_answer',
                 resource_class_kwargs={'es_client': es_client})