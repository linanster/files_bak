#! /usr/bin/env python3
#
import sys
import pymongo
import getpass
import json
import prettytable as pt

print('Interpreter: {}'.format(sys.executable))

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
        self.raw_users = None
        self.raw_devices = None
        self.raw_subscribes = None
        self.user = None

    def find_raw_data_by_email(self, email):
        self.raw_users = self.collection_user.find({'email':email})
        count = self.raw_users.count()
        if count > 1:
            raise Exception('**Duplicated records found in user table**')
        if count == 0:
            raise Exception('**No records found in user table**')
        self.user = self.raw_users[0]
        self.raw_subscribes = self.collection_subscribe.find({'user_id':self.user.get('_id')})
        self.raw_devices = self.collection_device.find({'extend.admin.emailAddress':email})

    def find_subscribed_devices_by_email(self, email):
        subscribed_deviceids = []
        valid_devices = []

        self.find_raw_data_by_email(email)

        for data in self.raw_subscribes:
            subscribed_deviceids.append(data.get('device_id'))
        for data in self.raw_devices:
            if data.get('_id') in subscribed_deviceids:
                valid_devices.append(data)

        # prettytable output
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

    def aggregate_device_type(self, device_type_list):
        pipeline = [
            {"$unwind":"$extend.bulbsArray"},
            {"$project":{"bulb":"$extend.bulbsArray"}},
            {"$project":{"displayname":"$bulb.displayName", "mac":"$bulb.mac", "deviceType":"$bulb.deviceType", "firmware":"$bulb.firmwareVersion"}},
            # filter
            # {"$match":{"deviceType":{"$in":device_type_list}}},
            # eliminate bad records
            {"$match":{"mac":{"$not":{"$eq":None}}, "deviceType":{"$not":{"$eq":None}}, "firmware":{"$not":{"$eq":None}}}},
            # group aggregation by devicetype
            {"$group":{"_id":"$deviceType", "count":{"$sum":1}}},
            # sort
            {"$sort":{"count":-1}},
            {"$project":{"_id":0, "deviceType":"$_id", "count":"$count"}}
        ]
        datas = self.collection_device.aggregate(pipeline=pipeline, allowDiskUse=True)
        # prettytable output
        heads = ['#', 'DeviceType', 'Count']
        rows = []
        index = 1
        for data in datas:
            devicetype = data.get('deviceType')
            count = data.get('count')
            if device_type_list is None:
                rows.append([index, devicetype, count])
                index += 1
            elif devicetype in device_type_list:
                rows.append([index, devicetype, count])
                device_type_list.remove(devicetype)
                index += 1
            else:
                pass
        try:
            for data in device_type_list:
                rows.append([index, data, 0])
                index += 1
        except:
            pass
        pretty_table(heads, rows)

    def print_raw_data_by_email(self, email):
        self.find_raw_data_by_email(email)
        print('++++ User Table++++')
        for data in self.raw_users:
            print(data)
            print('++++')
        print('++++ Device Table ++++')
        for data in self.raw_devices:
            print(data)
            print('++++')
        print('++++ Subscribe Table ++++')
        for data in self.raw_subscribes:
            print(data)
            print('++++')



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
    passwd = getpass.getpass('  Password: ')
    return ipaddr, port, username, passwd

# copy from main.py

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
MENU
====
1) Use Case 1: Query Device Info by Account 
2) Use Case 2: Caculate Total Count by Device Type
3) Use Case 3: Todo...
4) Use Case 4: Todo...
5) Use Case 5: Todo...
6) Help1: Query Raw Data by Account
7) Help2: Print Device Type Table
q) Quit
====
'''

device_type_table = '''
+------+----------+---------------------------------------+
| code | code_hex | name                                  |
+------+----------+---------------------------------------+
|    9 | 0x09     | Gen2 Tier2 C-Life Standalone          |
|   10 | 0x0A     | Gen2 Tier C-Sleep, Standalone         |
|   11 | 0x0B     | Gen2 Tier2 Sleep-BR30 Standalone      |
|   13 | 0x0D     | Gen2 TCO C-Life A19 ST                |
|   14 | 0x0E     | Gen2 TCO C-Sleep A19 ST               |
|   15 | 0x0F     | Gen2 TCO C-Sleep BR30 ST              |
|   24 | 0x18     | Gen2 Tier2 C-Life, Made for Google    |
|   25 | 0x19     | Gen2 Tier C-Sleep, Made for Google    |
|   26 | 0x1A     | Gen2 Tier Sleep-BR30, Made for Google |
|   27 | 0x1B     | Gen2 TCO C-Life A19 MFG               |
|   28 | 0x1C     | Gen2 TCO C-Sleep A19 MFG              |
|   29 | 0x1D     | Gen2 TCO C-Sleep BR30 MFG             |
|   30 | 0x1E     | Gen2 TCO Full Color A19 ST            |
|   31 | 0x1F     | Gen2 TCO Full Color A19 MFG           |
|   32 | 0x20     | Gen2 TCO Full Color BR30 ST           |
|   33 | 0x21     | Gen2 TCO Full Color BR30 MFG          |
|   34 | 0x22     | Gen2 TCO Full Color Strip ST          |
|   35 | 0x23     | Gen2 TCO Full Color Strip MFG         |
|   48 | 0x30     | Dimmer switch                         |
|   49 | 0x31     | Dimmer Switch(Premium)                |
|   51 | 0x33     | Switch Paddle                         |
|   52 | 0x34     | Switch Toggle                         |
|   53 | 0x35     | Switch Centre Button                  |
|   55 | 0x37     | Dimmer Switch                         |
|   56 | 0x38     | Dimmer Switch(Premium)                |
|   57 | 0x39     | Switch Paddle                         |
|   58 | 0x3A     | Switch Toggle                         |
|   59 | 0x3B     | Switch Centre Button                  |
|   61 | 0x3D     | Paddle switch TCO                     |
|   62 | 0x3E     | Toggle switch TCO                     |
|   63 | 0x3F     | Button switch TCO                     |
|   65 | 0x41     | GEN 1 Plug TCO                        |
|   66 | 0x42     | Indoor Plug GEN2                      |
|   67 | 0x43     | Out door Plug                         |
|   68 | 0x44     | Plug                                  |
|   81 | 0x51     | Fan Speed Switch                      |
|  128 | 0x80     | Dual mode Soft White A19              |
|  129 | 0x81     | Dual mode Tunable White A19           |
|  130 | 0x82     | Dual mode Tunable White BR30          |
|  131 | 0x83     | Dual mode Full Color A19              |
|  132 | 0x84     | Dual mode Full Color BR30             |
|  133 | 0x85     | Dual mode Full Color Strip            |
|  134 | 0x86     | Soft white A19                        |
|  135 | 0x87     | Tunable white A19                     |
|  136 | 0x88     | Tunable white BR30                    |
|  137 | 0x89     | Full color A19                        |
|  138 | 0x8A     | Full color BR30                       |
|  139 | 0x8B     | Full Color Light Strip                |
|  140 | 0x8C     | Cync Dule Mode Full color PAR38       |
|  224 | 0xE0     | Thermostat                            |
+------+----------+---------------------------------------+
'''

def option1():
    email = input('Please input account email: ') or 'arossoll@wowway.com'
    print('')
    if email == 'return':
        return
    mongo_cook.find_subscribed_devices_by_email(email)

def option2():
    device_type_raw = input('Input device types(seperated by comma, or null for all): ')
    print('')
    if device_type_raw == 'return':
        return
    if device_type_raw == '':
        device_type_list = None
    else:
        device_type_list = [int(x) for x in device_type_raw.split(',')]
    mongo_cook.aggregate_device_type(device_type_list)


def option3():
    print('todo')
def option4():
    print('todo')
def option5():
    print('todo')

def option6():
    email = input('Please input account email: ') or 'arossoll@wowway.com'
    print('')
    if email == 'return':
        return
    mongo_cook.print_raw_data_by_email(email)

def option7():
    print(device_type_table)

def option_quit():
    sys.exit(0)

options = {
    '1': option1,
    '2': option2,
    '3': option3,
    '4': option4,
    '5': option5,
    '6': option6,
    '7': option7,
    'q': option_quit
}

def pop_menu():
    while True:
        print(menu)
        option = input('Enter your option: ')
        print('')
        try:
            func = options.get(option.lower())
            if func is None:
                print('Wrong input, choose again...\n')
                continue
        except Exception as e:
            raise Exception('Menu error:' + str(e))
        func()
        continue

if __name__ == '__main__':

    try:
        print(welcome)
        ipaddr, port, username, passwd = get_conn_input()
        mongo_conn = MongoConn(username, passwd, ipaddr, port)
        mongo_cook = MongoCook(mongo_conn.client)

        pop_menu()
    
    except Exception as e:
        print(e)
        sys.exit(1)

