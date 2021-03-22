#! /usr/bin/env python3
#
import sys
import pymongo

# print(sys.executable)

url = "mongodb://user002:123456@localhost:27017/db1"
myclient = pymongo.MongoClient(url)
dblist = myclient.list_database_names()
# mydb = myclient['db1']
# mycollection = mydb['users']
mycollection = myclient['db1']['users']
# print(mycollection)

# mydata = mycollection.find_one()
# mydatas = mycollection.find()

# myquery = {'name':'Nan'}
myquery = {'name':{"$regex":'^nan$', "$options":'i'}}
myview = {'_id':0, 'name':1}
myfind = mycollection.find(myquery, myview)
total = myfind.count()
print('==total==', total)
print('==data==')
for data in myfind:
    print(data)

