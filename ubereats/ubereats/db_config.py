import pymongo

con = pymongo.MongoClient('localhost')
db_name = con['ubereats_may_28']

# db_name.newziland_citylink.rename('citylink_NZ')