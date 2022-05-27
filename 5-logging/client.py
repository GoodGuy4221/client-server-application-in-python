import socket
import json
from sys import argv, exit
import time
import logging

from common.utils import Utils
from common.variables import *
import log.client_log_config

CLIENT_LOGGER = logging.getLogger('client_logger')


class Client(Utils):
    def __init__(self):
        self.server_address: str = DEFAULT_IP_ADDRESS
        self.server_port: int = DEFAULT_PORT

    def create_presence(self) -> dict:
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: ANON_ACCOUNT_NAME,
            },
        }
        CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {out.get(USER).get(ACCOUNT_NAME)}')
        return out

    def parse_server_message(self, message: dict) -> str:
        CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
        if RESPONSE in message:
            if message[RESPONSE] == STATUS_OK:
                return f'{STATUS_OK} OK'
            return f'{STATUS_BAD_REQUEST} {message[ERROR]}'
        raise ValueError

    def main(self):
        self.server_address = argv[1] if len(argv) > 1 else False or self.server_address
        self.server_port = int(argv[2]) if len(argv) > 2 else False or self.server_port

        if self.server_port < MIN_PORT_NUMBER or self.server_port > MAX_PORT_NUMBER:
            CLIENT_LOGGER.critical(f'Попытка запуска клиента с неподходящим номером порта: {self.server_port}!')
            exit(1)

        CLIENT_LOGGER.info(
            f'Запущен клиент с параметрами, адрес сервера: {self.server_address}, порт: {self.server_port}')

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((self.server_address, self.server_port))
        message_to_server = self.create_presence()
        self.send_message(transport, message_to_server)
        CLIENT_LOGGER.info(f'отправлено сообщение: {message_to_server} серверу')

        try:
            answer: dict = self.get_message(transport)
            CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
            status_answer: str = self.parse_server_message(answer)
        except json.JSONDecodeError:
            CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        except ConnectionRefusedError:
            CLIENT_LOGGER.critical(
                f'Не удалось подключиться к серверу {self.server_address}:{self.server_port}, конечный компьютер отверг запрос на подключение.')


if __name__ == '__main__':
    client = Client()
    client.main()
