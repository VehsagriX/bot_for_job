import pandas as pd


def add_user(user: dict):
    df = pd.read_excel('user_file.xlsx')
    user_added = pd.concat([df, pd.DataFrame([user])])
    user_added.to_excel('user_file.xlsx', index=False)


def is_registered(user_id: int):
    df = pd.read_excel('user_file.xlsx')
    return user_id in df.user_id.values
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