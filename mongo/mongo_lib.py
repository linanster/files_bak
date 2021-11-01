#! /usr/bin/env python3
#
import sys
import pymongo
import getpass
import prettytable as pt

print(sys.executable)

# url = "mongodb://nan.li:m0ngoDB@10.128.224.34"
# username = 'nan.li'
# passwd = 'm0ngoDB'
# ipaddr = '10.128.224.34'
# port = '27017'
# uri = 'mongodb://{username}:{passwd}@{ipaddr}:{port}'.format(username=username, passwd=passwd, ipaddr=ipaddr, port=port)

def pretty_table(heads, datass):
    tb = pt.PrettyTable(field_names=heads)
    for datas in datass:
        tb.add_row(datas)
    print(tb)

class MongoConn(object):
    def __init__(self, username, passwd, ipaddr, port):
        self.username = username
        self.passwd = passwd
        self.ipaddr = ipaddr
        self.port = port
        self.uri = 'mongodb://{username}:{passwd}@{ipaddr}:{port}'.format(username=username, passwd=passwd, ipaddr=ipaddr, port=port)
        self.client = None
        try:
            client = pymongo.MongoClient(self.uri)
            db_list = client.list_database_names()
        except Exception as e:
            print('**Connect issue**')
            print(e)
            sys.exit(1)
        else:
            self.client = client
            print('\n**Connected {}:{}**'.format(self.ipaddr, self.port))
    def __del__(self):
        if self.client is not None:
            print('**Disconnected {}:{}**\n'.format(self.ipaddr, self.port))
            self.client.close()
    def get_mongo_client(self):
        return self.client

class MongoCook(object):

    def __init__(self, client):
        # mongo collections object for each table
        self.collection_user = client['xlink']['user']
        self.collection_device = client['xlink']['device']
        self.collection_subscribe = client['xlink']['subscribe']

    def find_subscribed_devices_by_email(self, email):
        raw_users = None
        raw_subscribes = None
        raw_devices = None
        user = None
        subscribed_deviceids = []
        valid_devices = []
        
        raw_users = self.collection_user.find({'email':email})
        count = raw_users.count()
        if count > 1:
            raise Exception('**Duplicated records found in user table**')
        if count == 0:
            raise Exception('**No records found in user table**')
        user = raw_users[0]
        raw_subscribes = self.collection_subscribe.find({'user_id':user.get('_id')})
        raw_devices = self.collection_device.find({'extend.admin.emailAddress':email})

        for data in raw_subscribes:
            subscribed_deviceids.append(data.get('device_id'))
        for data in raw_devices:
            if data.get('_id') in subscribed_deviceids:
                valid_devices.append(data)

        # print result
        # for data in valid_devices:
        #     print('==', data.get('name'), '==')
        #     bulbs = data.get('extend').get('bulbsArray')
        #     cameras = data.get('extend').get('standaloneDevicesArray')
        #     # in case: "standaloneDevicesArray": null
        #     if cameras is not None:
        #         bulbs.extend(cameras)
        #     for bulb in bulbs:
        #         print(bulb.get('displayName'), end='\t')
        #         print(bulb.get('deviceType'))
        for index_outer, data in enumerate(valid_devices):
            heads = ['#', 'Name', 'DeviceType']
            rows = []
            bulbs = data.get('extend').get('bulbsArray')
            cameras = data.get('extend').get('standaloneDevicesArray')
            # in case: "standaloneDevicesArray": null
            if cameras is not None:
                bulbs.extend(cameras)
            for index_inner, bulb in enumerate(bulbs):
                rows.append([index_inner+1, bulb.get('displayName'), bulb.get('deviceType')])
            
            home_name = data.get('name')
            print("{}.{}".format(index_outer+1, home_name))
            pretty_table(heads, rows)
            

class MongoDish(object):
    def __init__(self, cook):
        self.cook = cook

    def dish1(self):
        self.cook.find_subscribed_devices()
        self.cook.display_subscribed_devices()
    def dish2(self):
        pass
    def dish3(self):
        pass
        

def get_conn_input():
    print('==Please input connect info:==\n')
    ipaddr = input('  IP Address[10.128.224.34]: ') or '10.128.224.34'
    port = input('  Port[27017]: ') or '27017'
    username = input('  Username[nan.li]: ') or 'nan.li'
    passwd = getpass.getpass('  Password: ') or 'm0ngoDB'
    return ipaddr, port, username, passwd


if __name__ == '__main__':

    try:
        ipaddr, port, username, passwd = get_conn_input()

        # 1.pre-work
        mongo_conn = MongoConn(username, passwd, ipaddr, port)
        mongo_cook = MongoCook(mongo_conn.client, 'arossoll@wowway.com')
        dinner = MongoDish(mongo_cook)

        # 2.start transaction
        # use case1: find devices by account email
        dinner.dish1()

    except Exception as e:
        print(e)
        sys.exit(1)
