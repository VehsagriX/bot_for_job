import pandas as pd
import os


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

def get_request_by_value(some_value: str):
    pass

