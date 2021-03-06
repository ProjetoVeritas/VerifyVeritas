from flask_restful import Resource, request


class RegisterAnswer(Resource):
    # Receives
    # {
    #   text: 'TextToVerify',
    #   answer: 'AnswerToText'
    # }

    def __init__(self, es_client):
        self.es_client = es_client

    def post(self):
        args = request.get_json()

        print(args)

        text_id = args['id']
        answer = args['answer']

        response = self.es_client.add_answer_by_id(text_id, answer)

        if response['status'] == 'ERROR':
            return {'code': 500, "message": "ERROR_ANSWER_REGISTERED"}, 500

        return {'code': 200, "message": "ANSWER_REGISTERED"}, 200
