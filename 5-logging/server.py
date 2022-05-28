import socket
from sys import argv, exit
import json
import logging

from common.utils import Utils
from common.variables import *
import log.server_log_config

SERVER_LOGGER = logging.getLogger('server_logger')


class Server(Utils):
    def __init__(self):
        self.listen_address: str = DEFAULT_LISTEN_ADDRESS
        self.listen_port: int = DEFAULT_PORT

    def process_client_message(self, message: dict) -> dict:
        SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
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
                    SERVER_LOGGER.critical(
                        f'Попытка запуска сервера с указанием неподходящего порта {self.listen_port}. Допустимы адреса с {MIN_PORT_NUMBER} до {MAX_PORT_NUMBER}.')
                    exit(1)
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

        SERVER_LOGGER.info(
            f'Запущен сервер, порт для подключений: {self.listen_port}, адрес с которого принимаются подключения: '
            f'{self.listen_address or "любой"}. Если адрес не указан, принимаются соединения с любых адресов.')

        while True:
            SERVER_LOGGER.info('сервер ожидает запроса')
            client, client_address = transport.accept()
            SERVER_LOGGER.info(f'Установлено соединение с {client_address}')
            try:
                message_from_client = self.get_message(client)
                SERVER_LOGGER.debug(f'Получено сообщение {message_from_client}')
                response = self.process_client_message(message_from_client)
                SERVER_LOGGER.info(f'Сформирован ответ клиенту {response}')
                self.send_message(client, response)
                SERVER_LOGGER.info(f'Отправлен ответ клиенту {response}')
                client.close()
                SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрылось.')
            except (ValueError, json.JSONDecodeError):
                SERVER_LOGGER.error(f'принято не корректное сообщение от клиента: {client_address}')
                client.close()


if __name__ == '__main__':
    server = Server()
    server.main()
