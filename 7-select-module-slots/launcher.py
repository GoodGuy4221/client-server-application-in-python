import subprocess


class ST:
    EXIT = 'q',
    START = 's',
    CLOSE = 'x',


process = []

while True:
    ACTION = input(
        f'Выберите действие: {ST.EXIT} - выход, {ST.START} - запустить сервер и клиенты, {ST.CLOSE} - закрыть все окна: ')

    match ACTION.lower():
        case ST.EXIT:
            break
        case ST.START:
            process.append(subprocess.Popen('py server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))

            for _ in range(2):
                process.append(subprocess.Popen('py client.py -m send', creationflags=subprocess.CREATE_NEW_CONSOLE))

            for _ in range(5):
                process.append(subprocess.Popen('py client.py -m listen', creationflags=subprocess.CREATE_NEW_CONSOLE))

        case ST.CLOSE:
            while process:
                VICTIM = process.pop()
                VICTIM.kill()
