# 运行在电脑端

import socket
from pynput.keyboard import Key, Controller, Listener

FRONT = '前'
BACK = '后'
LEFT = '左'
RIGHT = '右'
STOP = '停'
EXIT = 'quit'
END = 'end'

IP = 'localhost'
PORT = 50007

c = socket.socket()
c.connect((IP, PORT))


def on_press(key):
    print('{0}被按下'.format(key))
    if key == Key.up:
        c.send(FRONT.encode('utf-8'))
    if key == Key.down:
        c.send(BACK.encode('utf-8'))
    if key == Key.right:
        c.send(RIGHT.encode('utf-8'))
    if key == Key.left:
        c.send(LEFT.encode('utf-8'))
    if key == Key.esc:
        c.send(EXIT.encode('utf-8'))
    if key == Key.enter:
        c.send(END.encode('utf-8'))


def on_release(key):
    c.send(STOP.encode('utf-8'))


Controller()
with Listener(on_press=on_press, on_release=on_release) as listener:
    _ = listener.join()
