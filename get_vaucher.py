import pandas as pd
from datetime import datetime

VOUCHERS_PATH = 'Vouchers.xlsx'


def get_voucher(user_id, user_name):
    df = pd.read_excel(VOUCHERS_PATH)
    used = len(df.dropna())
    if used >= len(df):
        return 'Ваучеров не осталось!'
    df.loc[used, 'user_id'] = user_id
    df.loc[used, 'user_name'] = user_name
    df.loc[used, 'date_used'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.to_excel(VOUCHERS_PATH, index=False)
    return f'Ваучер на 4 часа \n{df.voucher.iloc[used]}'