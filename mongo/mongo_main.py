from mongo_lib import MongoConn, MongoCook, MongoDish, get_conn_input
from mongo_kb import device_type_table
import sys

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

def option1():
    email = input('Please input account email: ') or 'arossoll@wowway.com'
    print('')
    if email == 'return':
        return
    mongo_cook.find_subscribed_devices_by_email(email)

def option2():
    device_type_raw = input('Input device types(seperated by comma, or null for all): ')
    print('')
    if email == 'return':
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








