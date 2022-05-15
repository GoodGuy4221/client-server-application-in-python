"""
Задание 6.

Создать НЕ программно (вручную) текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».

Принудительно программно открыть файл в формате Unicode и вывести его содержимое.
Что это значит? Это значит, что при чтении файла вы должны явно указать кодировку utf-8
и файл должен открыться у ЛЮБОГО!!! человека при запуске вашего скрипта.

При сдаче задания в папке должен лежать текстовый файл!

Это значит вы должны предусмотреть случай, что вы по дефолту записали файл в cp1251,
а прочитать пытаетесь в utf-8.

Преподаватель будет запускать ваш скрипт и ошибок НЕ ДОЛЖНО появиться!

Подсказки:
--- обратите внимание, что заполнять файл вы можете в любой кодировке
но открыть нужно ИМЕННО!!! в формате Unicode (utf-8)
--- обратите внимание на чтение файла в режиме rb
для последующей переконвертации в нужную кодировку

НАРУШЕНИЕ обозначенных условий - задание не выполнено!!!
"""

import chardet


def open_file_utf8(path_file, mode='r'):
    with open(path_file, mode=mode, encoding='utf-8') as file:
        for line in file:
            yield line.strip()


def convert_file_in_utf8(path_file):
    with open(path_file, mode='rb') as file:
        code_points = file.read()
    response = chardet.detect(code_points)
    specific_encoding = response['encoding']
    in_its_encoding = code_points.decode(encoding=specific_encoding).encode(encoding='utf-8')
    result = in_its_encoding.decode(encoding='utf-8')

    with open(path_file, mode='w', encoding='utf-8') as file:
        file.write(result)


def read_file(path_file):
    try:
        for line in open_file_utf8(path_file):
            print(line)
    except UnicodeDecodeError:
        convert_file_in_utf8(path_file)
        read_file(path_file)


read_file('test_file.txt')
