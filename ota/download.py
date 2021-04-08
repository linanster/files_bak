import sys
import os
import requests
import xml.dom.minidom
from xml.dom.minidom import parse

from urllib import parse

# pre definitions
workdir = os.path.abspath(os.path.dirname(__file__))
recipe = os.path.abspath(os.path.join(workdir, 'download.txt'))
downloaddir = os.path.abspath(os.path.join(workdir, 'download'))
print('==downloaddir==', downloaddir)

def empty_dir(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if name =='.gitkeep':
                continue
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

def transform(key):
    key = key.lstrip('/')
    return key

def record_download_txt(files):
    index = 1
    recipefile = open(recipe, 'w+')
    for filename in files:
        recipefile.write('[{}]{}\n'.format(index,filename))
        index += 1
    recipefile.close()


# 1. download xml file from ota server
url = "http://34.102.144.152"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

mydata = response.content

with open('ota.xml', 'wb') as f:
    f.write(mydata)

# 2. parse file list
DOMTree = xml.dom.minidom.parse("ota.xml")
collection = DOMTree.documentElement
contents = collection.getElementsByTagName("Contents")

found_otas = []
found_jpgs = []
found_otas_dereplicas = []
found_jpgs_dereplicas = []
download_otas = []
download_jpgs = []

for content in contents:
    key = content.getElementsByTagName('Key')[0].childNodes[0].data
    key = transform(key)
    if key.endswith('jpg'):
        found_jpgs.append(key)
    else:
        found_otas.append(key)

found_otas_dereplicas = list(set(found_otas))
found_jpgs_dereplicas = list(set(found_jpgs))

len_raw_total = len(contents)
len_found_otas = len(found_otas)
len_found_jpgs = len(found_jpgs)
len_found_total = len_found_otas + len_found_jpgs
len_found_otas_dereplicas = len(found_otas_dereplicas)
len_found_jpgs_dereplicas = len(found_jpgs_dereplicas)
len_found_total_dereplicas = len_found_otas_dereplicas+len_found_jpgs_dereplicas

print('==raw total==', len_raw_total)
print('==found total (ota+jpg)==', '{} ({} + {})'.format(len_found_total, len_found_otas, len_found_jpgs))
print('==found total dereplicas (ota+jpg)==', '{} ({} + {})'.format(len_found_total_dereplicas, len_found_otas_dereplicas, len_found_jpgs_dereplicas))
print()
# print('==found otas==')
# print(otas)
# print('==fond jpgs==')
# print(jpgs)

# 3. download files
empty_dir(downloaddir)
files = found_otas_dereplicas + found_jpgs_dereplicas
recipefile = open(recipe, 'w+')

option = input('Download?(y/n)')
if option not in ['y', 'Y']:
    record_download_txt(files)
    print('exit')
    sys.exit(0)
else:
    print('Begin to download')

index = 1
percentage = '%4.2f'
for filename in files:
    # percentage = round(index/len_found_total_dereplicas, 4)*100
    percentage = '%.2f' % ((index/len_found_total_dereplicas)*100)
    print('\r', 'finished {}%, downloading [{}]{}'.format(percentage, index, filename), end='', flush=True)
    recipefile.write('[{}]{}\n'.format(index,filename))
    filepath = os.path.join(downloaddir, filename)
    download_link = parse.urljoin(url, filename)
    response = requests.request("GET", download_link, headers=headers, data=payload)
    with open(filepath, 'wb') as download_file:
        download_file.write(response.content)
    index += 1
recipefile.close()
print('Done')
