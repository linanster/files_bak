#! /usr/bin/env python3
#
import sys
import pymongo
import getpass

print(sys.executable)

# url = "mongodb://nan.li:m0ngoDB@10.128.224.34"
# username = 'nan.li'
# passwd = 'm0ngoDB'
# ipaddr = '10.128.224.34'
# port = '27017'
# uri = 'mongodb://{username}:{passwd}@{ipaddr}:{port}'.format(username=username, passwd=passwd, ipaddr=ipaddr, port=port)

class MongoConn(object):
    def __init__(self, username, passwd, ipaddr, port):
        self.username = username
        self.passwd = passwd
        self.ipaddr = ipaddr
        self.port = port
        self.uri = 'mongodb://{username}:{passwd}@{ipaddr}:{port}'.format(username=username, passwd=passwd, ipaddr=ipaddr, port=port)
        self.client = None
        try:
            self.client = pymongo.MongoClient(self.uri)
        except Exeption as e:
            print('**Connect issue**')
            print(e)
            sys.exit(1)
        else:
            print('**Connected**', ipaddr, ':', port)
    def __del__(self):
        print('**Disconnected**', ipaddr, ':', port)
        self.client.close()
    def get_mongo_client(self):
        return self.client

class MongoCook(object):
    def __init__(self, client, email):
        # assume all raw records are possibly multiple
        self.raw_users = None
        self.raw_devices = None
        self.raw_subs = None
        # extracted data
        # found user
        self.user = None
        # list of subscribe table user_id
        self.sub_deviceids = None
        # valid records, means the ones matching subscribe table
        self.valid_devices = []
        # mongo collections object for each table
        self.collection_user = client['xlink']['user']
        self.collection_device = client['xlink']['device']
        self.collection_subscribe = client['xlink']['subscribe']
        # find raw datas
        # raw users
        self.raw_users = self.collection_user.find({'email':email})
        count = self.raw_users.count()
        if count > 1:
            raise Exception('**Duplicated records found in user table**')
        if count == 0:
            raise Exception('**No records found in user table**')
        self.user = self.raw_users[0]
        # raw subscribes
        self.raw_subs = self.collection_subscribe.find({'user_id':self.user.get('_id')})
        # raw devices
        self.raw_devices = self.collection_device.find({'extend.admin.emailAddress':email})
        # debug
        # print(self.raw_users.count())
        # print(self.raw_devices.count())
        # print(self.raw_subs.count())

    def find_subscribed_devices(self):
        subscribed_deviceids = []
        for data in self.raw_subs:
            subscribed_deviceids.append(data.get('device_id'))
        for data in self.raw_devices:
            if data.get('_id') in subscribed_deviceids:
                self.valid_devices.append(data)
        
    def display_subscribed_devices(self):
        for data in self.valid_devices:
            print('==', data.get('name'), '==')
            bulbs = data.get('extend').get('bulbsArray')
            cameras = data.get('extend').get('standaloneDevicesArray')
            # in case: "standaloneDevicesArray": null
            if cameras is not None:
                bulbs.extend(cameras)
            for bulb in bulbs:
                print(bulb.get('displayName'), end='\t')
                print(bulb.get('deviceType'))

def get_input():
    print('==Please input following info:==\n')
    ipaddr = input('IP Address[10.128.224.34]: ') or '10.128.224.34'
    port = input('Port[27017]: ') or '27017'
    username = input('Username[nan.li]: ') or 'nan.li'
    passwd = getpass.getpass('Password: ') or 'm0ngoDB'
    return ipaddr, port, username, passwd

welcome = '''
  __  __                         _____  ____    _______          _ 
 |  \/  |                       |  __ \|  _ \  |__   __|        | |
 | \  / | ___  _ __   __ _  ___ | |  | | |_) |    | | ___   ___ | |
 | |\/| |/ _ \| '_ \ / _` |/ _ \| |  | |  _ <     | |/ _ \ / _ \| |
 | |  | | (_) | | | | (_| | (_) | |__| | |_) |    | | (_) | (_) | |
 |_|  |_|\___/|_| |_|\__, |\___/|_____/|____/     |_|\___/ \___/|_|
                      __/ |                                        
                     |___/                                         

'''

menu = '''
Menu
====
1) Query devices for specific account 
2) Todo...
3) Todo...
q) Quit
====
'''

def pop_menu():
    while True:
        print(menu)
        option = input('Enter your option:')
        try:
            func = options.get(option)
            if func is None:
                print('Wrong input, enter again...\n')
                continue
        except Exception as e:
            raise Exception('Menu error:' + str(e))
        func()
        continue

if __name__ == '__main__':

    try:
        print(welcome)
        ipaddr, port, username, passwd = get_input()

        # 1.pre-work
        conn = MongoConn(username, passwd, ipaddr, port)
        myclient = conn.get_mongo_client()
        mycook = MongoCook(myclient, 'arossoll@wowway.com')

        # 2.start transaction
        # use case1: find devices by account email
        mycook.find_subscribed_devices()
        mycook.display_subscribed_devices()

    except Exception as e:
        print(e)
        sys.exit(1)
