from flask_restful import Resource, request


class GetById(Resource):

    def __init__(self, es_client):
        self.es_client = es_client

    def get(self):
        args = request.get_json()

        id = args['id']

        response_get = self.es_client.get_by_id(id)

        if response_get['status'] == 'ERROR':
            return {'code': 500, "message": "ERROR_GET_BY_ID"}, 500

        return {'code': 200, 'message': 'SUCCESS', 'data': response_get['data']}, 200