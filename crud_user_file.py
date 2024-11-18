import os.path
import pandas as pd



def add_user(user: dict) -> None:
    if os.path.exists("user_file.xlsx"):
        df = pd.read_excel('user_file.xlsx')
        user_added = pd.concat([df, pd.DataFrame([user])])
        user_added.to_excel('user_file.xlsx', index=False)
    else:
        df = pd.DataFrame(columns=user.keys())
        user_added = pd.concat([df, pd.DataFrame([user])])
        user_added.to_excel('user_file.xlsx', index=False)


def is_registered(user_id: int) -> bool:
    if os.path.exists('user_file.xlsx'):
        df = pd.read_excel('user_file.xlsx')
        return user_id in df.user_id.values
    return False


def get_user(user_id: int) -> pd.DataFrame:
    df = pd.read_excel('user_file.xlsx')
    user = df[df.user_id == user_id]
    return user

def get_user_table() -> pd.DataFrame:
    df = pd.read_excel('user_file.xlsx')
    return df

def get_user_name(user_id: int) -> tuple:
    user = get_user(user_id)
    user_last_name = user.user_last_name.values[0]
    user_name = user.user_name.values[0]
    company_name = user.company_name.values[0]
    return user_last_name, user_name, company_name


def get_user_data(user_id: int) -> tuple:
    user = get_user(user_id)
    name, last_name, company = get_user_name(user_id)
    phone = int(user.user_phone.values[0])
    email = user.user_email.values[0]
    company_name = user.company_name.values[0]
    department = user.department.values[0]
    return name, last_name, phone, email, company_name, department


def edit_profile_for_value(user_id: int, edit_key: str, value: str | int) -> str:
    table = get_user_table()
    table.loc[table['user_id'] == user_id, edit_key] = value # edit key value for user_id
    table.to_excel('user_file.xlsx', index=False) # save edited table to user_file.xlsx

    return f"Ваши данные успешно измены"


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
