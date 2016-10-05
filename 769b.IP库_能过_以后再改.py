#!/usr/bin/python
# coding: utf-8
# http://www.qlcoder.com/task/769b

import os
dirname = 'temp_769b'
filename = dirname + '.zip'
fileurl = 'https://github.com/qlcoder-oreo/taobaoip/archive/master.zip'
if not os.path.isdir(dirname):
    if not os.path.isfile(filename):
        print('下载数据文件……')
        import requests
        r = requests.get(fileurl)
        with open(filename, 'wb') as f:
            f.write(r.content)
    print('解压缩……')
    os.system( 'unzip {} -d {}'.format(filename, dirname))
    print('数据准备完毕。')

import json
def read_arr(filename):
    '从淘宝IP的PHP文件中读取数组'
    with open(dirname + '/taobaoip-master/src/' + filename) as f:
        lines = [line.strip() for line in f]
        s = ''.join(lines[2:-1])
        s = '[' + s[:-1] + ']'
        return json.loads(s)

city = read_arr('city.php')
country = read_arr('country.php')
province = read_arr('province.php')
proxy = read_arr('proxy.php')
data = open(dirname + '/taobaoip-master/ip.data', 'rb').read()

import struct

def decode_raw(raw):
    '解析一段原始数据'
    country_index, province_index, city_index1, city_index2, proxy_index = struct.unpack('BBBBB', raw)
    city_index = city_index1 * 256 + city_index2
    return country_index, province_index, city_index, proxy_index

def ip2addr(ip):
    '将ip转化为地址'
    arr = ip.split('.')
    if len(arr) != 4:
        return
    for i in range(len(arr)):
        a = int(arr[i])
        arr[i] = a
        if a < 0 or a > 255:
            return

    loc = (1 << 16) * arr[0] + (1 << 8) * arr[1] + arr[2]
    loc *= 5

    country_index, province_index, city_index, proxy_index = decode_raw(data[loc:loc+5])
    print(country_index, province_index, city_index, proxy_index)
    return {
        'country': country[country_index],
        'province': province[province_index],
        'city': city[city_index],
        'proxy': proxy[proxy_index]
    }

print(ip2addr('106.38.42.10'))

def get_seeker(name):
    '给出一个地址，返回一个函数：该函数对于给定的5字节原始ip数据，如果其中包含指定的地址，则返回1，否则返回0'

    country_index = country.index(name) if name in country else -1
    province_index = province.index(name) if name in province else -1
    city_index = city.index(name) if name in city else -1
    proxy_index = proxy.index(name) if name in proxy else -1

    print(country_index, province_index, city_index, proxy_index)

    def ret(raw):
        a, b, c, d = decode_raw(raw)
        if a == country_index or b == province_index or c == city_index or d == proxy_index:
            # print({
            #     'country': country[a],
            #     'province': province[b],
            #     'city': city[c],
            #     'proxy': proxy[d]
            # })
            return 1
        return 0

    return ret

seekers = [get_seeker('杭州市'), get_seeker('北京市'), get_seeker('上海市'), get_seeker('深圳市')]
answer = [0] * len(seekers)
jrange = range(len(seekers))
print('共有{}个记录'.format(int(len(data) / 5)))
for i in range(0, len(data), 5):
    raw = data[i:i + 5]
    for j in jrange:
        answer[j] += seekers[j](raw) * 256
    if i % 5000000 == 0:
        print('已处理{}万个记录'.format(int(i / 50000)))

print(answer)
