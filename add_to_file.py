import pandas as pd


def add_user(user: dict):
    df = pd.read_excel('user_file.xlsx')
    user_added = pd.concat([df, pd.DataFrame([user])])
    user_added.to_excel('user_file.xlsx', index=False)


def is_registered(user_id: int):
    df = pd.read_excel('user_file.xlsx')
    return user_id in df.user_id.values
