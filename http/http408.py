# coding: utf8
#
import socket
import time

# 1. Start Connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('47.101.215.138', 4080))
print('==Connection Established==')
print(s)

# 2. Send Request
line1= "GET /index1/ HTTP/1.1\r\n"
line2 = "Host: 47.101.215.138:4080\r\n"
line3 = "Connection: close\r\n"
line4 = "User-Agent: MyShell\r\n"
endline = "\r\n"

request_lines = [line1, line2, line3, line4, endline]


print('==Http Send:==')
for line in request_lines:
    s.send(line.encode('utf8'))
    print(line, end='')
    # time.sleep(1)
    time.sleep(20)

# 3. Receive Response
print('==Http Received:==')
while True:
    response = s.recv(1024)
    if response:
        print(response.decode('utf8'))
    else:
        break

s.close()

