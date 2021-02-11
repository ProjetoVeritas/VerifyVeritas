import base64
import requests
from flask_restful import Resource, request

from flaskapp.support.hasher import hashtext


class VerifyMedia(Resource):
    # Receives
    # {
    #   data: 'base64image'
    #   datatype: 'image' or 'audio' or 'video'
    # }

    def __init__(self, es_client):
        self.es_client = es_client

    def post(self):
        args = request.get_json()

        # Get media encoded as base64
        mediabase64 = args['data']

        media_id = hashtext(mediabase64)

        # Verify if image data was already registered
        response_id_text_get = self.es_client.verify_registered_text_media(media_id)

        # Media is not connected to a text
        if response_id_text_get['status'] == 'NOT_REGISTERED':
            # If not registered, proceed to get text

            if args['type'] == 'image/jpeg':
                # Decode media
                mediadata = base64.b64decode(mediabase64)

                # Get text from tika
                response = requests.put('http://localhost:9998/tika', data=mediadata,
                                        headers={'Content-type': 'image/jpeg', 'X-Tika-OCRLanguage': 'por'})

                text = response.content.decode('utf8')

            if args['type'] == 'audio/ogg; codecs=opus':
                # Get audio transcription
                response = requests.post('http://localhost:3800/transcribe', json={'data': mediabase64},
                                         headers={'Content-Type': 'application/json'})
                # Decode text
                text = eval(response.content.decode('utf8'))['data']

            # Get text hash
            text_id = hashtext(text)

            # Make link between media id (hash) and text id (hash)
            response_media_text_link = self.es_client.register_text_to_media(media_id, text_id)

            # If linking was successful
            if response_media_text_link['status'] == 'SUCCESS':
                # If the link between the media and text was made, try to find if text was already answered

                # Here it finds if the text was already answered
                response_get = self.es_client.get_answer_by_exact_text(text)
                # Text not registered
                if response_get['status'] == 'NOT_REGISTERED':
                    response_register = self.es_client.register(text)
                    # Success in registration
                    if response_register['status'] == 'SUCCESS':
                        return {'code': 200, 'message': 'SUCCESS_NOT_REGISTERED'}, 200
                    # Error in registration
                    if response_register['status'] == 'ERROR':
                        return {'code': 500, 'message': 'ERROR_NOT_REGISTERED'}, 500

                # Text not answered yet
                if response_get['status'] == 'NOT_ANSWERED':
                    return {'code': 200, 'message': 'SUCCESS_NOT_ANSWERED'}, 200

                # Text answered, return response
                return {'code': 200, 'message': 'ANSWERED', 'data': response_get}, 200

            # Error in link registration
            if response_media_text_link['status'] == 'ERROR':
                return {'code': 500, 'message': 'ERROR_NOT_REGISTERED'}, 500

        # Media is connected to a text
        # Get id of linked text
        id_text = response_id_text_get['data']

        answer_get_by_id = self.es_client.get_by_id(id_text)

        # If there's error when getting
        if answer_get_by_id['status'] == 'ERROR':
            return {'code': 500, 'message': 'ERROR_GET_BY_ID'}, 500

        # If there's an entry but it's not answered
        if 'answer' not in answer_get_by_id['data'].keys():
            return {'code': 200, 'message': 'SUCCESS_NOT_ANSWERED'}, 200

        # If there's an entry and it was already answered
        response_get = answer_get_by_id['data']['answer']

        return {'code': 200, 'message': 'ANSWERED', 'data': response_get}, 200
