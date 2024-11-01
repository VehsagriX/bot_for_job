import pandas as pd
import numpy as np



def add_user(user: dict):
    df = pd.read_excel('user_file.xlsx')
    user_added = pd.concat([df, pd.DataFrame([user])])
    user_added.to_excel('user_file.xlsx', index=False)


def is_registered(user_id: int):
    df = pd.read_excel('user_file.xlsx')
    return user_id in df.user_id.values


def user_anketa(user_id: int):
    df = pd.read_excel('user_file.xlsx')
    user = df[df.user_id == user_id]
    return user

def get_user_name(user_id: int):
    user = user_anketa(user_id)
    user_last_name = user.user_last_name.values[0]
    user_name = user.user_name.values[0]
    return user_last_name, user_name

def get_user_data(user_id: int):
    user = user_anketa(user_id)
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
