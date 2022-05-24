import socket
from sys import argv, exit
import json

from common.utils import Utils
from common.variables import *


class Server(Utils):
    def __init__(self):
        self.listen_address: str = DEFAULT_LISTEN_ADDRESS
        self.listen_port: int = DEFAULT_PORT

    def process_client_message(self, message: dict) -> dict:
        if (ACTION in message and
                message[ACTION] == PRESENCE and
                TIME in message and
                USER in message and
                message[USER][ACCOUNT_NAME] == ANON_ACCOUNT_NAME):
            return {RESPONSE: 200}
        return {
            RESPONDEFAULT_IP_ADDRESSSE: 400,
            ERROR: 'Bad Request',
        }

    def main(self):
        if '-p' in argv:
            try:
                self.listen_port = int(argv[argv.index('-p') + 1])
                if self.listen_port < MIN_PORT_NUMBER or self.listen_port > MAX_PORT_NUMBER:
                    raise ValueError('недопустимый номер порта')
            except IndexError:
                print('после параметра -\'p\' необходимо указать номер порта.')
                exit(1)
            except ValueError:
                print(f'в качестве порта может быть указано только число в диапазоне от {MIN_PORT_NUMBER} до '
                      f'{MAX_PORT_NUMBER}.')
                exit(1)

        if '-a' in argv:
            try:
                listen_address = argv[argv.index('-a') + 1]
            except IndexError:
                print(
                    'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
                exit(1)

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.listen_address, self.listen_port))

        transport.listen(MAX_CONNECTIONS)

        while True:
            print('сервер ожидает запроса')
            client, client_address = transport.accept()
            print(f'пришел запрос {client} от клиента с адресом {client_address}')
            try:
                message_from_client = self.get_message(client)
                print(f'получено сообщение от клиента {message_from_client}')
                response = self.process_client_message(message_from_client)
                self.send_message(client, response)
                print('отправлен ответ клиенту')
                client.close()
            except (ValueError, json.JSONDecodeError):
                print('принято не корректное сообщение от клиента.')
                client.close()


if __name__ == '__main__':
    server = Server()
    server.main()
