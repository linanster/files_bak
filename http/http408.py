# coding: utf8
#
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.30.30.101', 4000))
print(s)

req_line1 = "GET /index HTTP/1.1\r\n"
# req_line2 = "Host: 10.30.30.101:4000\r\n"
req_line2 = "Host: 47.101.215.138:4000\r\n"
req_line3 = "Connection:keep-alive\r\n"
req_line4 = "\r\n"
req_raw = req_line1 + req_line2 +req_line3 + req_line4

print(req_raw)


# time.sleep(2)

for i in range(1):
    print('=={}=='.format(i))
    s.send(req_raw.encode('utf8'))
    
    data = b''
    while True:
        d = s.recv(1024)
        if d:
            data += d
        else:
            break
    
    data = data.decode("utf-8")
    print(data)
    # html_data = data.split("\r\n\r\n")[1]
    # print(html_data)

s.close()

