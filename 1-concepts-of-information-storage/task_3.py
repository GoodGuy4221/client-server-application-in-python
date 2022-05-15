"""
Задание 3.

Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b'' (без encode decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
--- обязательно!!! усложните задачу, "отловив" и обработав исключение,
придумайте как это сделать
"""

words_list = ['attribute', 'класс', 'функция', 'type']


def is_written_byte(sequence: list | tuple) -> None:
    for item in sequence:
        try:
            print(eval(f'b"{item}"'))
        except SyntaxError:
            print(f'слово: «{item}» невозможно записать в байтовом типе с помощью маркировки «b» т.к. '
                  f'состоит не только из ascii символов')


is_written_byte(words_list)
