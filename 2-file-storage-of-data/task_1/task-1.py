"""
Задание 1.

1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку
определенных данных из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый
«отчетный» файл в формате CSV. Для этого:
a. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с
данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения
каждого параметра поместить в соответствующий список. Должно получиться четыре
списка — например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же
функции создать главный список для хранения данных отчета — например, main_data
— и поместить в него названия столбцов отчета в виде списка: «Изготовитель
системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data (также для
каждого файла);
b. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой
функции реализовать получение данных через вызов функции get_data(), а также
сохранение подготовленных данных в соответствующий CSV-файл;
c. Проверить работу программы через вызов функции write_to_csv().
"""

from chardet import detect
import re
import csv


def get_data(list_file_paths: list | tuple, parameter_values: list | tuple, separator: str) -> dict:
    result = {item: [] for item in parameter_values}
    pattern = f'^({"|".join(parameter_values)})'
    for file in list_file_paths:
        with open(file, mode='rb') as f:
            bytes_string = f.read()
            coding = detect(bytes_string)['encoding']
            utf8_string = bytes_string.decode(encoding=coding).encode(encoding='utf-8').decode(encoding='utf-8')
            for line in utf8_string.splitlines():
                if re.match(pattern=pattern, string=line):
                    k, v = line.split(separator)
                    result[k.strip()].append(v.strip())
    return result


def write_to_csv(data: dict, name_file: str) -> None:
    # with open(f'{name_file}.csv', 'w', encoding='utf-8') as f:
    #     write_data = [list(data.keys())]
    #     write_data.extend(list(zip(*data.values())))
    #     print(write_data)
    #     F_N_WRITER = csv.writer(f)
    #     F_N_WRITER.writerows(write_data)

    data_list = []
    i = len(tuple(data.values())[0])
    for n in range(i):
        d = {}
        for k, v in data.items():
            d[k] = v[n]
        data_list.append(d)

    with open(f'{name_file}.csv', 'w', encoding='utf-8') as f:
        F_N_WRITER = csv.DictWriter(f, fieldnames=data.keys())
        F_N_WRITER.writeheader()
        F_N_WRITER.writerows(data_list)


list_file = ('info_1.txt', 'info_2.txt', 'info_3.txt')
param_vls = ('Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы')
write_to_csv(get_data(list_file, param_vls, ':'), 'task1')
