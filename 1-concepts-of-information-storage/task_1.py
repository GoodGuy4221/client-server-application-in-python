"""
Задание 1.

Каждое из слов «разработка», «сокет», «декоратор» представить
в буквенном формате и проверить тип и содержание соответствующих переменных.
Затем с помощью онлайн-конвертера преобразовать
в набор кодовых точек Unicode (НО НЕ В БАЙТЫ!!!)
и также проверить тип и содержимое переменных.

Подсказки:
--- 'разработка' - буквенный формат
--- '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430' - набор кодовых точек
--- используйте списки и циклы, не дублируйте функции
"""

letter_format = ['разработка', 'сокет', 'декоратор']
code_point_format = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
                     '\u0441\u043e\u043a\u0435\u0442',
                     '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']


def check_type_content(sequence: list | tuple) -> None:
    for item in sequence:
        print(f'тип: {type(item)} | содержание: {item}')


check_type_content(letter_format)
check_type_content(code_point_format)
