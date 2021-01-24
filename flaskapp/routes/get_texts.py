from flask_restful import Resource, request


class GetTexts(Resource):

    def __init__(self, es_client):
        self.es_client = es_client

    def get(self):
        response_get = self.es_client.get_random_unanswered_texts()

        if response_get['status'] == 'ERROR':
            return {'code': 500, "message": "ERROR_GET_TEXTS"}, 500

        output_results = []
        for result in response_get['data']:
            row = result['_source']
            row['id'] = result['_id']
            output_results.append(row)

        return {'code': 200, 'message': 'SUCCESS', 'data': output_results}, 200