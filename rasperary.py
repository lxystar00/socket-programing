# 运行在树莓派

import socket

FRONT = '前'
BACK = '后'
LEFT = '左'
RIGHT = '右'
STOP = '停'
EXIT = 'quit'
END = 'end'

IP = 'localhost'
PORT = 50007


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(1)
conn, address = s.accept()  # 接受TCP连接，并返回新的套接字与IP地址
print('Connected by', address)  # 输出客户端的IP地址

conn.recv(1024)
while True:
    recv_byte = conn.recv(1024)  # 把接收的数据实例化
    recv_str = recv_byte.decode('utf-8')#解码
    if recv_str == END:
        print('结束')
    elif recv_str == EXIT:
        print('结束')
    elif recv_str == FRONT:
        print('向前运动')
    elif recv_str == BACK:
        print('向后运动')
    elif recv_str == LEFT:
        print('左转')
    elif recv_str == RIGHT:
        print('右转')
    else:
        print('停止运动')

