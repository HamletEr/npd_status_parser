import os


def get_data_list_from_csv(input_file_path: str) -> list:
    """
    Функция получает список значений из CSV-файла

    Первая строка (с шапкой) отбрасывается, в список добавляются первые 2 столбца таблицы
    [['saisakaeva', '164800238917'], ['swytoi', '220409027176'], ... ]

    :param input_file_path: путь к файлу
    :return: list
    """

    normalize_path_input_file = os.path.abspath(os.path.join(input_file_path))

    with open(file=normalize_path_input_file, mode='r', encoding='utf-8') as input_file:
        lines = input_file.readlines()[1:]

    split_lines = [i_line.rstrip('\n').split(';')[:2] for i_line in lines]

    return split_lines


def add_line_to_csv(data_list: list,
                    output_file_path: str = 'output.csv',
                    separator: str = ';') -> None:
    """
    Функция дописывает данные в CSV-файл

    :param data_list: список данных, которые необходимо дописать в файл
    :param output_file_path: имя файла для записи, по умолчанию: 'output.csv'
    :param separator: разделитель, по умолчанию: ';'
    :return: None
    """

    normalize_path_output_file = os.path.abspath(os.path.join(output_file_path))

    with open(file=normalize_path_output_file, mode='a', encoding='utf-8') as output_file:
        output_file.write(separator.join(data_list) + '\n')

    print(f'Строка "{separator.join(data_list)}" добавлена в файл {output_file_path}')
