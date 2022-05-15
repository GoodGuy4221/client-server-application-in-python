"""
Задание 2.

Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя!!! методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

Подсказки:
--- b'class' - используйте маркировку b''
--- используйте списки и циклы, не дублируйте функции
"""

byte_format = [b'class', b'function', b'method']


def define_type_content_length_variables(sequence: list | tuple) -> None:
    for item in sequence:
        print(f'тип: {type(item)} | содержимое: {item} | длина: {len(item)}')


define_type_content_length_variables(byte_format)
