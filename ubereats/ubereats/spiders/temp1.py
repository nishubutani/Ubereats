import pandas as pd
import pymongo


def insert_data():
    con = pymongo.MongoClient('localhost')
    db_name = con['ubereats_april']
    cur = db_name['link_ZP']

    df = pd.read_excel('D:\\new Company\\ubereats\\excel\\april\\Book1.xlsx')
    # print(df)
    for link in df['link']:
        print(link)

        try:
            item = {}
            item['link'] = link
            item['status'] = 'Pending'
            cur.insert(dict(item))
        except Exception as e:
            pass



if __name__ == '__main__':
    insert_data()