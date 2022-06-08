import socket
import sys
from sys import argv, exit
import json
import logging
import select
import argparse
import time
from collections import deque

from common.utils import Utils
from common.variables import *
import log.server_log_config
from log.decorators import log, Log

SERVER_LOGGER = logging.getLogger('server_logger')


class Server(Utils):
    def __init__(self):
        self.listen_address: str = DEFAULT_LISTEN_ADDRESS
        self.listen_port: int = DEFAULT_PORT

        self.clients = []
        self.messages = deque()

    @log
    def process_client_message(self, message: dict, messages_list: list, client: socket) -> None:
        # SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
        if (ACTION in message and
                message[ACTION] == PRESENCE and
                TIME in message and
                USER in message and
                message[USER][ACCOUNT_NAME] == ANON_ACCOUNT_NAME):
            self.send_message(client, {RESPONSE: 200})
            return
        elif ACTION in message and message[ACTION] == MESSAGE and TIME in message and MESSAGE_TEXT in message:
            messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
            return
        else:
            response = {
                RESPONSE: 400,
                ERROR: 'Bad Request',
            }
            self.send_message(client, response)
        return

    @log
    def check_port(self) -> None:
        if self.listen_port < MIN_PORT_NUMBER or self.listen_port > MAX_PORT_NUMBER:
            SERVER_LOGGER.critical(
                f'Попытка запуска сервера с указанием неподходящего порта {self.listen_port}. Допустимы адреса с {MIN_PORT_NUMBER} до {MAX_PORT_NUMBER}.')
            exit(1)

    @log
    def arguments_parser(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
        parser.add_argument('-a', default='', nargs='?')
        name_space = parser.parse_args(sys.argv[1:])
        self.listen_address = name_space.a
        self.listen_port = name_space.p
        self.check_port()

    @Log()
    def main(self):
        self.arguments_parser()

        # SERVER_LOGGER.info(
        #     f'Запущен сервер, порт для подключений: {self.listen_port}, адрес с которого принимаются подключения: '
        #     f'{self.listen_address or "любой"}. Если адрес не указан, принимаются соединения с любых адресов.')

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.listen_address, self.listen_port))
        transport.settimeout(0.5)
        transport.listen(MAX_CONNECTIONS)

        while True:
            try:
                client, client_address = transport.accept()
                # SERVER_LOGGER.info('сервер ожидает запроса')
            except OSError:
                pass
            else:
                SERVER_LOGGER.info(f'Установлено соединение с {client_address}')
                self.clients.append(client)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []

            try:
                if self.clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(self.clients, self.clients, [], 0)
            except OSError:
                pass

            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        self.process_client_message(self.get_message(client_with_message), self.messages,
                                                    client_with_message)
                    except Exception:
                        SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                        self.clients.remove(client_with_message)

            if self.messages and send_data_lst:
                message = {
                    ACTION: MESSAGE,
                    SENDER: self.messages[0][0],
                    TIME: time.time(),
                    MESSAGE_TEXT: self.messages[0][1]
                }
                self.messages.popleft()
                for waiting_client in send_data_lst:
                    try:
                        self.send_message(waiting_client, message)
                    except Exception:
                        SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                        waiting_client.close()
                        self.clients.remove(waiting_client)


if __name__ == '__main__':
    server = Server()
    server.main()
