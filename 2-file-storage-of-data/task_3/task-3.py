"""
Задание 3.

3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий
сохранение данных в файле YAML-формата. Для этого:
a. Подготовить данные для записи в виде словаря, в котором первому ключу
соответствует список, второму — целое число, третьему — вложенный словарь, где
значение каждого ключа — это целое число с юникод-символом, отсутствующим в
кодировке ASCII (например, €);
b. Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а
также установить возможность работы с юникодом: allow_unicode = True;
c. Реализовать считывание данных из созданного файла и проверить, совпадают ли они
с исходными
"""

import yaml

DATA = {
    '11€': ['one', 'two'],
    '22€': 21,
    '33€': {'one': 'two'},
}


def write_yaml(data: dict, name_file: str = 'file') -> None:
    with open(f'{name_file}.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, indent=4)


def read_yaml(path_file: str) -> dict:
    with open(path_file, encoding='utf-8') as f:
        return yaml.load(f, Loader=yaml.SafeLoader)


write_yaml(DATA, name_file='task3')
print(read_yaml('task3.yaml') == DATA)
