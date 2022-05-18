"""
Задание 2.

2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с
информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными. Для
этого:
a. Создать функцию write_order_to_json(), в которую передается 5 параметров — товар
(item), количество (quantity), цена (price), покупатель (buyer), дата (date). Функция
должна предусматривать запись данных в виде словаря в файл orders.json. При
записи данных указать величину отступа в 4 пробельных символа;
b. Проверить работу программы через вызов функции write_order_to_json() с передачей
в нее значений каждого параметра.
{"orders": []}
"""

import json


def write_order_to_json(item: str, quantity: str | int, price: str | int | float, buyer: str | int, date: str) -> None:
    data = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date,
    }

    with open('orders.json', 'r+', encoding='utf-8') as f:
        obj = json.load(f)
        f.seek(0)
        obj.get('orders').append(data)
        json.dump(obj, f, indent=4, ensure_ascii=False)


write_order_to_json('поездка в турцию', 2, 50000, 1, '2022-05-18')
