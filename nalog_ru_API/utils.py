import requests

from datetime import datetime


def check_inn(inn: str) -> dict:
    """
    Функция принимает ИНН и возвращает данные о статусе плательщика НПД

    :param inn: ИНН (str)
    :return: словарь с результатами запроса или сообщением об ошибке (dict)

    При успешном запросе получаем:
        {'response_status': 'OK',
         'data': {'status': True,
                  'message': '402809738237 является плательщиком налога на профессиональный доход'}}

        {'response_status': 'OK',
         'data': {'status': False,
                  'message': '031805161890 не является плательщиком налога на профессиональный доход'}}
    Ошибки:
        {'response_status': 'Error 422',
         'data': {'code': 'validation.failed',
                  'message': 'Указан некорректный ИНН: 402809738230'}}

        {'response_status': 'Error 422',
         'data': {'code': 'taxpayer.status.service.limited.error',
                  'message': 'Превышено количество запросов к сервису с одного '
                             'ip-адреса в единицу времени, пожалуйста, попробуйте позднее.'}}

        {'response_status': 'Error API',
         'data': {'error': 'Неизвестная ошибка при получении ответа сервера'}}
    """

    inn_data = {
        'inn': inn,
        'requestDate': str(datetime.today().date())
    }

    response = requests.post(url='https://statusnpd.nalog.ru/api/v1/tracker/taxpayer_status',
                             json=inn_data,
                             timeout=60)        # в документации требование на таймаут 60 сек
    try:
        data = response.json()

        if response.status_code == 200:
            response_status = 'OK'

        else:
            response_status = 'Error ' + str(response.status_code)

    except Exception as unknown_error:
        response_status = 'Error API'
        data = {'error': 'Неизвестная ошибка при получении ответа сервера'}

    result = {
        'response_status': response_status,
        'data': data
    }

    return result
