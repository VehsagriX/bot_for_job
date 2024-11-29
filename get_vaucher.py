import pandas as pd
from datetime import datetime



def get_voucher(user_id: int | str, user_name: str, description: str, voucher_path: str):
    df = pd.read_excel(voucher_path)
    used = len(df.dropna())
    #цель получения доступа к Гостевому WI-FI
    if used >= len(df):
        return 'Ваучеров не осталось!'
    df.loc[used, 'user_id'] = user_id
    df.loc[used, 'user_name'] = user_name
    df.loc[used, 'date_used'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df.to_excel(voucher_path, index=False)
    return f'Ваучер: \n{df.voucher.iloc[used]}'