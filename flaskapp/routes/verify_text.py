from flask_restful import Resource, request


class VerifyText(Resource):
    # Receives
    # {
    #   text: 'TextToVerify'
    # }

    def __init__(self, es_client):
        self.es_client = es_client

    def post(self):
        args = request.get_json()

        text = args['text']

        response_get = self.es_client.get_answer_by_exact_text(text)

        # Text not registered
        if response_get['status'] == 'NOT_REGISTERED':
            response_register = self.es_client.register(text)

            if response_register['status'] == 'SUCCESS':
                return {'code': 200, 'message': 'SUCCESS_NOT_REGISTERED'}, 200

            if response_register['status'] == 'ERROR':
                return {'code': 500, 'message': 'ERROR_NOT_REGISTERED'}, 500

        # Text not answered yet
        if response_get['status'] == 'NOT_ANSWERED':
            return {'code': 200, 'message': 'SUCCESS_NOT_ANSWERED'}, 200

        return {'code': 200, 'message': 'ANSWERED', 'data': response_get}, 200
