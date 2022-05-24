import json
from socket import socket

from .variables import *


class Utils:
    def get_message(self, client: socket) -> dict:
        encoded_response = client.recv(MAX_PACKAGE_LENGTH)
        if isinstance(encoded_response, bytes):
            json_response = encoded_response.decode(ENCODING)
            response = json.loads(json_response)
            if isinstance(response, dict):
                return response
            raise ValueError('Не dict')
        raise ValueError('Не байты')

    def send_message(self, sock, message):
        json_message = json.dumps(message)
        encoded_message = json_message.encode(encoding=ENCODING)
        sock.send(encoded_message)
