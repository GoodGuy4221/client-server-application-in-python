import json
from socket import socket
import sys
from pathlib import Path

sys.path.append(f'{Path(__file__).resolve().parent}')

from variables import *
from errors import NotDict, NotBytes


class Utils:
    def get_message(self, client: socket) -> dict:
        encoded_response = client.recv(MAX_PACKAGE_LENGTH)
        if isinstance(encoded_response, bytes):
            json_response = encoded_response.decode(ENCODING)
            response = json.loads(json_response)
            if isinstance(response, dict):
                return response
            raise NotDict
        raise NotBytes

    def send_message(self, sock, message: dict):
        if not isinstance(message, dict):
            raise NotDict
        json_message: str = json.dumps(message)
        encoded_message: bytes = json_message.encode(encoding=ENCODING)
        sock.send(encoded_message)
