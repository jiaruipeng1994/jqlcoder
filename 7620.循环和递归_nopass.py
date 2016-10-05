# !/usr/bin/python
# coding: utf-8
# http://www.qlcoder.com/task/7620
# 这题的答案是f(7,7)的值的最后8位(7进制,答案是一个长度为8的7进制数)。

'''
上回说到f(7,?)的解一定落在f(3,n)的解空间上。并且由于解空间最长只有7**8，所以解一定是循环的。
这里打表，使f(3,?)的时间复杂度为O(1)
'''

def get_fn():
    '''
    当函数的解空间
    '''

#计算f3的解
dic = {}
a = 5
i = 0
n = 7 ** 8
print(n)
v3 = []
while a not in dic:
	dic[a] = i
	v3.append(a)
	a = (a * 2 + 3) % n
	i += 1

	if i % (1024 * 1024) == 0:
		print('calc {} M = {}'.format(i / 1024 / 1024, a))

print('找到循环节 f(3, {}) = f(3, {}) = {}'.format(i, dic[a], a))

recurring_start = dic[a]
recurring_len = i - recurring_start

def f3(n):
	return v3[(n - recurring_start) % recurring_len]

flist = [None, None, None, f3]

def f_generator(m):
	'一个函数生成器'
	f_low = flist[m - 1]
	v = []
	def f_by_m(n):
		if n >= len(v):
			print('请求f({}, {})，但当前只缓存了{}，填充中……'.format(m, n, len(v)))
			if 0 == len(v):
				v.append(f_low(1))
			for i in range(len(v), n + 1):
				v.append(f_low(v[i - 1]))
		return v[n]

	return f_by_m

flist.append(f_generator(4))
flist.append(f_generator(5))
flist.append(f_generator(6))
flist.append(f_generator(7))

print(flist[7](7))
