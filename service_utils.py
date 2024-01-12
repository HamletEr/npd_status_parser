import os
import time

from typing import Optional

from CSV_handler.utils import get_data_list_from_csv, add_line_to_csv
from nalog_ru_API.utils import check_inn


def get_start_position_for_parsing(input_data_list,
                                   output_file_path,
                                   separator) -> int:
    """
    Функция возвращает индекс строки, с которой нужно начать парсинг
    """
    start_position_for_parsing = 0

    if os.path.isfile(os.path.abspath(output_file_path)):  # если выходной файл уже существует

        with open(file=os.path.abspath(output_file_path), mode='r', encoding='utf-8') as output_file:
            last_line = output_file.readlines()[-1].rstrip('\n').split(separator)

        for index_elem, elem in enumerate(input_data_list):
            if elem[0] == last_line[0]:
                start_position_for_parsing = index_elem + 1
                print(f'Последняя строка в выходном файле: {last_line}')
                break

    return start_position_for_parsing


def start_parsing(actual_data_list: list,
                  output_file_path: Optional[str] = None,
                  separator: str = ';',
                  pause_between_requests: int = 30):
    """
    Функция запускает парсинг: циклично отправляет запросы и записывает результаты в файл

    :param actual_data_list:
    :param output_file_path:
    :param separator:
    :param pause_between_requests:
    :return:
    """

    for index_elem, elem in enumerate(actual_data_list):

        response: dict = check_inn(elem[1])

        if response['response_status'] == 'OK':
            result = [elem[0], elem[1], str(response['data']['status']), response['data']['message']]

            add_line_to_csv(result,
                            output_file_path,
                            separator)

            time_to_completion = (len(actual_data_list) - index_elem) * pause_between_requests

            print(f'Обработан {elem[0]}, ИНН: {elem[1]} - {index_elem + 1} из {len(actual_data_list)}.'
                  f'Время до полного завершения парсинга: {round(time_to_completion / 60)} минут\n')

            time.sleep(pause_between_requests)

        else:
            print(f'Ошибка: {response["response_status"]}: {response["data"]}')
            print('Парсинг прерван')
            break


def start_work(input_file_path: str,
               output_file_path: Optional[str] = None,
               separator: str = ';',
               pause_between_requests: int = 30):

    """
    Основная функция программы.
    Принимает на вход пути к входному и выходному файлам,
    разделитель который используется в файлах,
    длительность паузы в секундах.
    Запускает парсер.

    При неуспешной обработке запроса на сервер прерывает работу, выводит соответствующее сообщение в консоль.

    :param input_file_path: str
    :param output_file_path: str
    :param separator: str
    :param pause_between_requests: int
    """

    if not os.path.isfile(os.path.abspath(input_file_path)):
        print('Путь к входному файлу задан не верно')
        return False

    input_data_list = get_data_list_from_csv(input_file_path)
    start_position_for_parsing = 0

    # проверяем с какой строки нужно начинать парсинг
    if output_file_path:
        start_position_for_parsing = get_start_position_for_parsing(input_data_list,
                                                                    output_file_path,
                                                                    separator)

    if len(input_data_list) < start_position_for_parsing + 1:
        print('Во входном файле нет необработанных строк или последняя строка не уникальна')
        return

    print(f'Начинаем парсинг со строки: {input_data_list[start_position_for_parsing]}')

    actual_data_list = input_data_list[start_position_for_parsing:]

    start_parsing(actual_data_list,
                  output_file_path,
                  separator,
                  pause_between_requests)
