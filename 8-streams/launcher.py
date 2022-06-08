import subprocess
import sys


class ST:
    __slots__ = ('exit', 'start', 'close')

    def __init__(self, exit: str, start: str, close: str) -> None:
        self.exit = exit
        self.start = start
        self.close = close


st = ST(exit='q', start='s', close='x')

process = []

while True:
    ACTION = input(
        f'Выберите действие: {st.exit} - выход, {st.start} - запустить сервер и клиенты, {st.close} - закрыть все окна: ').lower()

    match ACTION:
        case st.exit:
            sys.exit(0)
        case st.start:
            process.append(subprocess.Popen('py server.py', creationflags=subprocess.CREATE_NEW_CONSOLE))

            for n in range(1, 4):
                process.append(
                    subprocess.Popen(f'py client.py -n CLIENT{n}', creationflags=subprocess.CREATE_NEW_CONSOLE))

        case st.close:
            while process:
                VICTIM = process.pop()
                VICTIM.kill()
