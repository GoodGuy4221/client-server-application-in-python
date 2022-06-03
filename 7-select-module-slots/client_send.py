import argparse
import socket
import json
import sys
from sys import argv, exit
import time
import logging

from common.utils import Utils
from common.variables import *
import log.client_log_config
from log.decorators import log, Log

CLIENT_LOGGER = logging.getLogger('client_logger')


class Client(Utils):
    def __init__(self):
        self.server_address: str = DEFAULT_IP_ADDRESS
        self.server_port: int = DEFAULT_PORT
        self.client_mode: str = ''

        self.message = {}
        self.message_from_server = {}

        self.sock = socket.socket()
        self.account_name = ANON_ACCOUNT_NAME

        self.presence_request: dict = {}

    # @log
    def check_message_from_server(self):
        if (ACTION in self.message_from_server and self.message_from_server[ACTION] == MESSAGE and
                SENDER in self.message_from_server and MESSAGE_TEXT in self.message_from_server):
            CLIENT_LOGGER.info(
                f'Получено сообщение от пользователя {self.message_from_server[SENDER]}:\n{self.message_from_server[MESSAGE_TEXT]}')
        else:
            CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {self.message_from_server}')

    # @log
    def create_message(self):
        message: str = input(f'Введите сообщение для отправки или `{EXIT_CLIENT_CHAR}` для завершения работы: ')
        if message == EXIT_CLIENT_CHAR:
            self.sock.close()
            CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
            exit(0)
        message: dict = {
            ACTION: MESSAGE,
            TIME: time.time(),
            ACCOUNT_NAME: self.account_name,
            MESSAGE_TEXT: message,
        }
        CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message}')
        self.message = message

    # @log
    def create_presence(self) -> None:
        """Генерирует запрос о присутствии клиента"""
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: self.account_name,
            },
        }
        # CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {out.get(USER).get(ACCOUNT_NAME)}')
        self.presence_request = out

    # @log
    def parse_server_message(self) -> str:
        """Разбирает ответ сервера на сообщение о присутствии,
        возвращает 200 если все ОК или генерирует исключение при ошибке"""
        # CLIENT_LOGGER.debug(f'Разбор приветственного сообщения от сервера: {message}')
        if RESPONSE in self.message_from_server:
            if self.message_from_server[RESPONSE] == STATUS_OK:
                return f'{STATUS_OK} OK'
            return f'{STATUS_BAD_REQUEST} {self.message_from_server[ERROR]}'
        raise ValueError

    # @log
    def check_port(self) -> None:
        if self.server_port < MIN_PORT_NUMBER or self.server_port > MAX_PORT_NUMBER:
            CLIENT_LOGGER.critical(
                f'Попытка запуска клиента с указанием неподходящего порта {self.server_port}. Допустимы адреса с {MIN_PORT_NUMBER} до {MAX_PORT_NUMBER}.')
            exit(1)

    # @log
    def check_mode(self):
        if self.client_mode not in ACCEPTABLE_CLIENT_MODES:
            CLIENT_LOGGER.critical(
                f'Указан недопустимый режим работы {self.client_mode}, допустимые режимы: {ACCEPTABLE_CLIENT_MODES}')
            exit(1)

    # @log
    def arguments_parser(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
        parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
        parser.add_argument('-m', '--mode', default='send', nargs='?')
        name_space = parser.parse_args(sys.argv[1:])
        self.server_address = name_space.addr
        self.server_port = name_space.port
        self.client_mode = name_space.mode
        self.check_port()
        self.check_mode()

    @Log()
    def main(self):
        self.arguments_parser()

        # CLIENT_LOGGER.info(
        #     f'Запущен клиент с параметрами, адрес сервера: {self.server_address}, порт: {self.server_port}, '
        #     f'режим работы: {self.client_mode}')

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.server_address, self.server_port))
            self.create_presence()
            self.send_message(self.sock, self.presence_request)
            self.message_from_server = self.get_message(self.sock)
            answer = self.parse_server_message()
            CLIENT_LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        except json.JSONDecodeError:
            CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
            exit(1)
        except Exception:
            CLIENT_LOGGER.error('Неизвестная ошибка.')
            exit(1)
        else:
            if self.client_mode == 'send':
                print('Режим работы - отправка сообщений.')
            else:
                print('Режим работы - приём сообщений.')

        while True:
            if self.client_mode == 'send':
                try:
                    self.create_message()
                    self.send_message(self.sock, self.message)
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {self.server_address} было потеряно.')
                    exit(1)

            if self.client_mode == 'listen':
                try:
                    self.message_from_server = self.get_message(self.sock)
                    self.check_message_from_server()
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {self.server_address} было потеряно.')
                    exit(1)


if __name__ == '__main__':
    client = Client()
    client.main()
