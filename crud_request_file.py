import pandas as pd
import os

from aiohttp import request


def add_request(request: dict):
    if os.path.exists("request_file.xlsx"):
        df = pd.read_excel('request_file.xlsx')

        user_added = pd.concat([df, pd.DataFrame([request])])
        user_added.to_excel('request_file.xlsx', index=False)
    else:
        df = pd.DataFrame(columns=request.keys())
        user_added = pd.concat([df, pd.DataFrame([request])])
        user_added.to_excel('request_file.xlsx', index=False)


def get_request_table() -> pd.DataFrame:
    df = pd.read_excel('request_file.xlsx')
    return df


def get_all_requests(user_id: int, some_value: str = 'Выполнено', status_new: str = 'В ожидании'):
    requests = get_request_table()
    requests = requests.query(f"request_status != '{some_value}' and request_creator == {str(user_id)}")

    return requests.values


def get_request_by_id(request_id: int):
    df = pd.read_excel('request_file.xlsx')
    my_request = df[df.request_id == request_id]
    return my_request


def change_value_request(request_id: int | str, edit_key, value) -> None:
    requests = get_request_table()


    requests.loc[requests['request_id'] == request_id, edit_key] = value

    requests.to_excel('request_file.xlsx', index=False)


def show_all_requests(user_id):
    list_keys = ['Тип заявки:', 'ID:', 'Создатель заявки:', 'Связаться с заявителем:', 'Заголовок:', "Описание:",
                 'Исполнитель:', 'Статус:']
    result = get_all_requests(user_id)
    request_list = []
    for i in range(len(result)):
        my_text = ''
        for j in range(len(result[i])):
            if j == 3:
                my_text += list_keys[j] + ' ' + '@' + str(result[i][j]) + '\n'
            else:
                my_text += list_keys[j] + ' ' + str(result[i][j]) + '\n'

        request_list.append(my_text)

    return request_list
