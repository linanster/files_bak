#! /usr/bin/env python3
#
import sys
import pymongo

print(sys.executable)

url = "mongodb://geuser:Mdb4GE@db1:27017/admin"
myclient = pymongo.MongoClient(url)
mycollection = myclient['xlink']['device']
print('==mycollection==', mycollection)

# myquery = {'extend.admin.emailAddress':{"$regex":"^zkiki0452@gmail.com$", "$options":"i"}}
myquery = {'extend.admin.emailAddress':"zkiki0452@gmail.com"}
# myview = {'_id':0, 'extend.admin.emailAddress':1, 'name':1}
myview = {'_id':0, 'extend.admin':1, 'name':1}
myfind = mycollection.find(myquery, myview)
total = myfind.count()
print('==total==', total)

print('==datas==', )
for data in myfind:
    print(data)

