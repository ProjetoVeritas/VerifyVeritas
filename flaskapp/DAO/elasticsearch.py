from elasticsearch import Elasticsearch
from elasticsearch import exceptions

from flaskapp.support.hasher import hashtext


class ESClient:

    def __init__(self, user, password, host):
        self.es = Elasticsearch(
            [f'https://{user}:{password}@{host}'],
            verify_certs=False
        )

    def register(self, text):
        response = self.es.index(index='veritasdata', id=hashtext(text), body={'original_text': text})
        if response['result'] == 'created':
            return {'status': 'SUCCESS'}
        return {'status': 'ERROR'}

    def get_answer_by_exact_text(self, text):
        try:
            response = self.es.get(index='veritasdata', id=hashtext(text))['_source']
            if 'answer' not in response.keys():
                return {
                    'status': 'NOT_ANSWERED',
                    'data': None}
            else:
                return {
                    'status': 'SUCCESS',
                    'data': response['answer']}

        except exceptions.NotFoundError:
            return {
                'status': 'NOT_REGISTERED',
                'data': None}

    def add_answer_by_exact_text(self, text, asnwer):
        response = self.es.update(index='veritasdata', id=hashtext(text), body={"doc": {'answer': asnwer}})
        if response['result'] == 'updated':
            return {'status': 'SUCCESS'}
        return {'status': 'ERROR'}
