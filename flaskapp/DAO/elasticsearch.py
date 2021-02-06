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

    def verify_registered_text_media(self, media_id):
        # This function verifies if a media id hash has a correspondent text id hash
        try:
            response = self.es.get(index='veritasmediatext', id=media_id)['_source']
            # If there's a linked text id to the media, return it
            return {
                'status': 'SUCCESS',
                'data': response['linked_text_id']}

        except exceptions.NotFoundError:
            # There's no registered text id for the media
            return {
                'status': 'NOT_REGISTERED',
                'data': None}

    def register_text_to_media(self, media_hash, text_hash):
        response = self.es.index(index='veritasmediatext', id=media_hash, body={'linked_text_id': text_hash})
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

    def get_by_id(self, id):
        response = self.es.get(index='veritasdata', id=id)

        if response['found']:
            return {'status': 'SUCCESS', 'data': response['_source']}
        return {'status': 'ERROR', 'data': None}

    def add_answer_by_id(self, text_id, answer):
        response = self.es.update(index='veritasdata', id=text_id, body={"doc": {'answer': answer}})
        if response['result'] == 'updated':
            return {'status': 'SUCCESS'}
        return {'status': 'ERROR'}

    def get_random_unanswered_texts(self):
        response = self.es.search(index='veritasdata',
                                  body={
                                    "size": 10,
                                    "query": {
                                        "function_score": {
                                            "query": {
                                                "bool": {
                                                    "must": [
                                                        {
                                                            "match_all": {
                                                                "boost": 1.0
                                                            }
                                                        }
                                                    ],
                                                    "filter": [
                                                        {
                                                            "bool": {
                                                                "must_not": {
                                                                    "exists": {
                                                                        "field": "answer"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    ]
                                                }
                                            },
                                            "random_score": {},
                                            "score_mode": "sum"
                                        }
                                    }
                                })

        if response['_shards']['failed'] == 0:
            return {'status': 'SUCCESS', 'data': response['hits']['hits']}

        return {'status': 'ERROR', 'data': None}
