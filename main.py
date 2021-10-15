"""
Програма для расчета по ДЗ №2
Версия 1.0
Автор: Андрей Корниенко

Домашнее задание
Работа с тестовыми данными

Цель:
Научиться работать с различными типами файлов.

Работа с тестовыми данными

Скачать файлы: https://github.com/konflic/front_example/blob/master/data/books.csv и
https://github.com/konflic/front_example/blob/master/data/users.json.
Написать скрипт, который из двух данных файлов будет читать данные и на их основании создаст
result.json файл со структурой: https://github.com/konflic/front_example/blob/master/data/reference.json.
Идея в том что нужно раздать все книги из csv файла пользователям из списка. Книги складываются
в виде словарей в массив books у каждого пользователя.
Книг изначально больше чем пользователей, поэтому раздавать нужно по принципу "максимально поровну",
т.е. если книг, например 10. а пользователей 3 то распределение будет таким - 4 3 3 (один получит
оставшуюся книгу). Итоговая структура должна соответствовать стандарту json и парситься
соответствующей библиотекой.
Критерии оценки:
Задание оформить отдельным pull-request'ом (https://www.youtube.com/watch?v=swWqJBFpaNY)
В репозитории отсутствуют лишние файлы
Соблюдается минимальный кодстайл (встроенный в PyCharm)
В личном кабинете или репозитории приложен файл result.json с итоговым результатом.
Исходные файлы копировать не нужно.
Рекомендуем сдать до: 21.07.2021
"""

import json
from csv import DictReader

with open('./data/books.csv', newline='') as csv_file:
    reader = DictReader(csv_file)

    # Итерируемся по данным делая из них список словарей
    books = []
    for row in reader:
        books.append(row)

with open("./data/users.json", "r") as json_file:
    users = json.loads(json_file.read())

filtered_users_list = []
for user in users:
    filtered_attr_dict = {key: value for key, value in user.items()
                          if key in ['name', 'gender', 'address', 'age']}
    filtered_users_list.append(filtered_attr_dict)

# Рассчитываем количество книг, которое должно быть у каждого пользователя
# (по принципу "максимально поровну")
int_books_amount_per_user = int(len(books) / len(filtered_users_list))

for user in filtered_users_list:
    # Раздаем кники поровну пользователям
    for book in range(int_books_amount_per_user):
        # Создаем у списка 'filtered_users_list' ключ 'books', в котором будет список книг,
        # и добавляем туда книги, исключая эти книги из списка книг 'books'
        user.setdefault('books', []).append(books.pop(0))  # https://www.rupython.com/4968-4968.html

# Раздаем оставшиеся книги пользователям (если количество книг не делится нацело на
# количество пользователей)
for user in filtered_users_list:
    if len(books) != 0:
        user['books'].append(books.pop(0))
    else:
        break

# Получившийся список для записи в json-файл
# print(f"filtered_users={filtered_users_list}")

# Производим запись итогового списка словарей в json-файл
with open("reference.json", "w") as json_file:
    str_ = json.dumps(filtered_users_list, indent=4)
    json_file.write(str_)
