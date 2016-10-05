#!/usr/bin/python
# coding: utf-8
# http://www.qlcoder.com/task/766e

import os
import struct

url = 'http://www.qlcoder.com/download/rf.data'
filename = 'temp_76ee.data'
tempfold = 'temp_76ee'
__import__('util').loadfile(url, filename)

if os.path.isdir(tempfold):
    __import__('shutil').rmtree(tempfold)
os.mkdir(tempfold)


data = open(filename, 'rb')

index = 0

while True:
    state, = struct.unpack('B', data.read(1))
    if state == 2:
        break
    a,b,c,d = struct.unpack('BBBB', data.read(4))
    print(a,b,c,d)
    length = (a << 24) + (b << 16) + (c << 8) + d
    jpgname = '{}/pic_{}.jpg'.format(tempfold, index)
    print(jpgname,  length, ['可用', '已删除'][state])
    index += 1
    if state == 0:
        with open(jpgname, 'wb') as jpg:
            print('写入了文件？')
            jpg.write(data.read(length))
            print('写入了文件')
