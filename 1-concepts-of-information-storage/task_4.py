"""
Задание 4.

Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

words_list = ['разработка', 'администрирование', 'protocol', 'standard']


def convert_words_and_reverse(sequence: list | tuple) -> None:
    for item in sequence:
        bytes_world = str.encode(item, encoding='utf-8')
        string_world = bytes.decode(bytes_world, encoding='utf-8')
        print(f'слово «{item}» в байтовом состоянии «{bytes_world}» и обратно преобразованное «{string_world}»')


convert_words_and_reverse(words_list)
