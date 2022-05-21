import socket
from sys import argv, exit
import json

from common.utils import Utils


class Server(Utils):
    def __init__(self):
        self.listen_address: str = self.DEFAULT_LISTEN_ADDRESS
        self.listen_port: int = self.DEFAULT_PORT

    def process_client_message(self, message: dict) -> dict:
        if (self.ACTION in message and
                message[self.ACTION] == self.PRESENCE and
                self.TIME in message and
                self.USER in message and
                message[self.USER][self.ACCOUNT_NAME] == self.ANON_ACCOUNT_NAME):
            return {self.RESPONSE: 200}
        return {
            self.RESPONDEFAULT_IP_ADDRESSSE: 400,
            self.ERROR: 'Bad Request',
        }

    def main(self):
        if '-p' in argv:
            try:
                self.listen_port = int(argv[argv.index('-p') + 1])
                if self.listen_port < self.MIN_PORT_NUMBER or self.listen_port > self.MAX_PORT_NUMBER:
                    raise ValueError('недопустимый номер порта')
            except IndexError:
                print('После параметра -\'p\' необходимо указать номер порта.')
                exit(1)
            except ValueError:
                print(f'В качестве порта может быть указано только число в диапазоне от {self.MIN_PORT_NUMBER} до '
                      f'{self.MAX_PORT_NUMBER}.')
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

        transport.listen(self.MAX_CONNECTIONS)

        while True:
            print('сервер запущен')
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
                print('Принято не корректное сообщение от клиента.')
                client.close()


if __name__ == '__main__':
    server = Server()
    server.main()
