import socket
import json
from sys import argv, exit
import time

from common.utils import Utils


class Client(Utils):
    def __init__(self):
        self.server_address: str = self.DEFAULT_IP_ADDRESS
        self.server_port: int = self.DEFAULT_PORT

    def create_presence(self) -> dict:
        out = {
            self.ACTION: self.PRESENCE,
            self.TIME: time.time(),
            self.USER: {
                self.ACCOUNT_NAME: self.ANON_ACCOUNT_NAME,
            },
        }
        return out

    def parse_server_message(self, message: dict) -> str:
        if self.RESPONSE in message:
            if message[self.RESPONSE] == self.STATUS_OK:
                return f'{self.STATUS_OK} OK'
            return f'{self.STATUS_BAD_REQUEST} {message[self.ERROR]}'
        raise ValueError

    def main(self):
        try:
            server_address = argv[1]
            server_port = int(argv[2])
            if server_port < self.MIN_PORT_NUMBER or server_port > self.MAX_PORT_NUMBER:
                raise ValueError('недопустимый номер порта')
        except IndexError:
            pass
        except ValueError:
            print(f'В качестве порта может быть указано только число в диапазоне от {self.MIN_PORT_NUMBER} до '
                  f'{self.MAX_PORT_NUMBER}.')
            exit(1)

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((self.server_address, self.server_port))
        message_to_server = self.create_presence()
        self.send_message(transport, message_to_server)
        print(f'отправлено сообщение {message_to_server} серверу')

        try:
            answer: dict = self.get_message(transport)
            print(f'получено сообщение от сервера {answer}')
            status_answer: str = self.parse_server_message(answer)
        except (ValueError, json.JSONDecodeError):
            print('не удалось декодировать сообщение от сервера')
        # transport.close()


if __name__ == '__main__':
    client = Client()
    client.main()
