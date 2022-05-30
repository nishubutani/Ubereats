#
def status_update_ott():
    import pymongo

    con = pymongo.MongoClient('mongodb://localhost:27017/')
    db = con.ubereats_april
    # link_t = db['zapan_citylink']
    link_t = db['citylink_TW']

    try:
        link_t.update_many({},{"$set": {"status": 'pending'}})
        print("link updated")
    except Exception as e:
        print(e, "error in done pending")


if __name__ == '__main__':
    status_update_ott()