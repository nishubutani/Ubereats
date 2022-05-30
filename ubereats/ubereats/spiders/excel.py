def add2_1():
    import pymongo
    import pandas as pd
    import numpy as np
    import xlsxwriter
    from ubereats import  db_config as dbc

    db_name = dbc.db_name
    cur = db_name['Data_ZP']
    exec = 'Zapan_data_02_05_2022_00'
    # exec = 'newziland_data_02_05_2022_00'
    # exec = 'taiwan_data_02_05_2022_00'
    # exec = 'Australiya_data_02_05_2022_00'

    cursor = cur.find({}, no_cursor_timeout=True)

    df = pd.DataFrame(cursor)
    # df = df['tier_backup']
    # df.pop('_id')
    # df.pop('tier_backup')a
    df.index = np.arange(1, len(df) + 1)
    df.index.name = 'Id'
    # df.to_csv('Brandrep_data_30_12_2021.csv')
    writer = pd.ExcelWriter(f'D:\\new Company\\ubereats\\excel\\may\\{exec}.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})
    df.to_excel(writer, index=False)
    writer.close()
    print("Excel Genrated")


if __name__ == '__main__':
    add2_1()