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


def get_all_request(user_id: int):
    pass

def get_request_by_id(request_id: int):
    df = pd.read_excel('request_file.xlsx')
    request = df[df.request_id == request_id]
    return request

def change_value_request(request_id: int, edit_key, value):
    request = get_request_by_id(request_id)
    request[edit_key] = value
    return request
