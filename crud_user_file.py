import os.path

import pandas as pd


def add_user(user: dict):
    if os.path.exists("user_file.xlsx"):
        df = pd.read_excel('user_file.xlsx')
        user_added = pd.concat([df, pd.DataFrame([user])])
        user_added.to_excel('user_file.xlsx', index=False)
    else:
        df = pd.DataFrame(columns=user.keys())
        user_added = pd.concat([df, pd.DataFrame([user])])
        user_added.to_excel('user_file.xlsx', index=False)


def is_registered(user_id: int):
    if os.path.exists('user_file.xlsx'):
        df = pd.read_excel('user_file.xlsx')
        return user_id in df.user_id.values
    return False

def get_user(user_id: int):
    df = pd.read_excel('user_file.xlsx')
    user = df[df.user_id == user_id]
    return user


def get_user_name(user_id: int):
    user = get_user(user_id)
    user_last_name = user.user_last_name.values[0]
    user_name = user.user_name.values[0]
    return user_last_name, user_name


def get_user_data(user_id: int):
    user = get_user(user_id)
    name, last_name = get_user_name(user_id)
    phone = int(user.user_phone.values[0])
    email = user.user_email.values[0]
    return name, last_name, phone, email

# import wmi
#
# # Initializing the wmi constructor
# f = wmi.WMI()
#
# # Printing the header for the later columns
# print("pid   Process name")
#
# # Iterating through all the running processes
# for process in f.Win32_Process():
#     # Displaying the P_ID and P_Name of the process
#     print(f"{process.ProcessId:<10} {process.Name}")
# print(get_user_name())