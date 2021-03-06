import sys
sys.path.append('../')  # Must have a best solution

import os

from flask import Flask
from flask_restful import Api

from flaskapp.DAO.elasticsearch import ESClient

from flaskapp.routes.verify_text import VerifyText
from flaskapp.routes.register_answer import RegisterAnswer
from flaskapp.routes.get_texts import GetTexts
from flaskapp.routes.get_by_id import GetById
from flaskapp.routes.verify_media import VerifyMedia

user = os.getenv('user')
password = os.getenv('password')
host = os.getenv('host')

app = Flask(__name__)

es_client = ESClient(user, password, host)

api = Api(app)

api.add_resource(VerifyMedia,
                 '/receive_media',
                 resource_class_kwargs={'es_client': es_client})

api.add_resource(VerifyText,
                 '/receive_text',
                 resource_class_kwargs={'es_client': es_client})

api.add_resource(RegisterAnswer,
                 '/register_answer',
                 resource_class_kwargs={'es_client': es_client})

api.add_resource(GetTexts,
                 '/get_texts',
                 resource_class_kwargs={'es_client': es_client})

api.add_resource(GetById,
                 '/get_by_id',
                 resource_class_kwargs={'es_client': es_client})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
